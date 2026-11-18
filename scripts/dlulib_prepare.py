#!/usr/bin/env python3
"""DLULIB archive -> separately preserved training arrays and sealed external labels.

Do not use, inspect or load `sealed_labels` from model-fitting or inference scripts.
This script is the only intake path that handles the original external test XY;
the numeric GT does not appear in logs, model features, or public outputs.
"""
from pathlib import Path
import argparse,hashlib,json,zipfile
import numpy as np
from io import BytesIO
from openpyxl import load_workbook

MD5='e30071a2f4bf14ed96f5f46f20468ac3'

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def sheet_rows(binary,temporary,stop=15000):
    # Portable read-only implementation of the original artifact_tool sheet parse.
    # This code returns numeric values, without exposing any test XY in logs.
    wb=load_workbook(BytesIO(binary),read_only=True,data_only=True)
    ws=wb.worksheets[0]
    rows=ws.iter_rows(min_row=1,max_row=stop,max_col=26,values_only=True)
    head=[str(x) if x is not None else '' for x in next(rows)]
    ap=[head.index(f'AP{k}') for k in range(1,18)]
    for label in ('X','Y','ID_RP','FloorID'):
        if label not in head:raise ValueError('Missing field '+label)
    values=[r for r in rows if r[ap[0]] is not None]
    wb.close()
    rss=np.asarray([[float(r[t]) for t in ap] for r in values],dtype=np.float32)
    xy=np.asarray([[float(r[head.index('X')]),float(r[head.index('Y')])] for r in values],dtype=np.float64)
    rp=np.asarray([int(r[head.index('ID_RP')]) for r in values],dtype=np.int32)
    fl=np.asarray([int(r[head.index('FloorID')]) for r in values],dtype=np.int16)
    if not (np.isfinite(rss).all() and np.isfinite(xy).all() and ((rss>=-100)&(rss<0)).all()):
        raise ValueError('Invalid RSS/XY or AP missing sentinel')
    return rss,xy,rp,fl

def main():
    p=argparse.ArgumentParser();p.add_argument('--zip',required=True,type=Path)
    p.add_argument('--workspace',required=True,type=Path);a=p.parse_args()
    a.workspace.mkdir(parents=True,exist_ok=True)
    if hashlib.md5(a.zip.read_bytes()).hexdigest()!=MD5:raise ValueError('DLULIB original MD5 mismatch')
    z=zipfile.ZipFile(a.zip)
    if z.testzip() is not None:raise ValueError('Corrupt ZIP')
    audit=[]
    for floor in (1,2,3):
        with_={}
        for role in ('All_20','Mean'):
            fn=next(s for s in z.namelist() if s.endswith(f'Training_DLULIB_Floor{floor}_{role}.xlsx'))
            rss,xy,rp,fl=sheet_rows(z.read(fn),None)
            assert (fl==floor).all()
            out=a.workspace/'ingest'/'train_arrays';out.mkdir(parents=True,exist_ok=True)
            np.savez_compressed(out/f'floor{floor}_{role}_TRAIN_ONLY.npz',rss=rss,xy=xy,rp=rp,floor=fl)
            with_[role]=(rss,xy,rp)
            audit.append({'floor':floor,'role':'training_'+role,'n':len(rss),'RPs':len(np.unique(rp))})
        if not (set(with_['All_20'][2])==set(with_['Mean'][2])):
            raise ValueError('Inconsistent training RPs')
        fn=next(s for s in z.namelist() if s.endswith(f'Testing_DLULIB_Floor{floor}.xlsx'))
        rss,xy,rp,fl=sheet_rows(z.read(fn),None,stop=7600)
        assert (fl==floor).all()
        sid=np.asarray([f'F{floor}-Q{i:05d}' for i in range(len(rss))])
        public=a.workspace/'inference_only';sealed=a.workspace/'sealed_labels'
        public.mkdir(exist_ok=True);sealed.mkdir(exist_ok=True)
        ip=public/f'floor{floor}_INFERENCE_ONLY.npz';sp=sealed/f'floor{floor}_SEALED_GT.npz'
        np.savez_compressed(ip,rss=rss,scan_id=sid,floor_context=fl)
        np.savez_compressed(sp,scan_id=sid,xy=xy,rp_id=rp,floor_id=fl)
        audit.append({'floor':floor,'role':'test inputs and sealed labels','n':len(rss),
                      'input_SHA256':digest(ip),'sealed_GT_SHA256':digest(sp)})
    (a.workspace/'sealed_labels'/'INTAKE_AUDIT.json').write_text(json.dumps(audit,indent=2))
    (a.workspace/'inference_only'/'INFERENCE_AND_SEALED_GT_HASHES.json').write_text(json.dumps([r for r in audit if r['role']=='test inputs and sealed labels'],indent=2))
    print('Original DLULIB archive verified; split training/input/sealed-label files created; numeric test XY not printed')
if __name__=='__main__':main()
