"""Source-only DLULIB archive identity and file-layout gate (no label parsing).

Public dataset source: DOI 10.5281/zenodo.19434712, DLULIB.zip.
This is an intake audit, NOT a numerical validation or feature adapter.
The reader never opens any Excel file content or test position.
"""
import hashlib
import re
import zipfile
from pathlib import Path

PINNED_MD5 = 'e30071a2f4bf14ed96f5f46f20468ac3'
DOI='10.5281/zenodo.19434712'


def audit_archive(archive_path, enforce_pinned_md5=True):
    path=Path(archive_path)
    h=hashlib.md5();s=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(2<<20),b''):
            h.update(chunk);s.update(chunk)
    digest=h.hexdigest()
    if enforce_pinned_md5 and digest!=PINNED_MD5:
        raise ValueError('DLULIB archive MD5 disagrees with official Zenodo file listing')
    found={f'{floor}:{role}':[] for floor in (1,2,3)
           for role in ('train_all','train_mean','test')}
    zip_entries=[]
    with zipfile.ZipFile(path) as z:
        bad=z.testzip()
        if bad is not None:raise ValueError('ZIP CRC failure: '+bad)
        for meta in z.infolist():
            if meta.is_dir():continue
            # No decompression of XLSX/test worksheet bytes; file listing only.
            name=meta.filename
            zip_entries.append({'path':name,'bytes_uncompressed':int(meta.file_size)})
            short=Path(name).name.lower()
            m=re.search(r'floor[_\s-]*([123])',name.lower())
            if not short.endswith(('.xlsx','.xls')) or not m:continue
            floor=int(m.group(1))
            if 'testing' in short or re.search(r'(^|_)test',short):role='test'
            elif 'training' in short and ('mean' in short or 'average' in short):role='train_mean'
            elif 'training' in short:role='train_all'
            else:continue
            found[f'{floor}:{role}'].append(name)
    missing=[role for role,files in found.items() if len(files)!=1]
    return {'dataset':'DLULIB','doi':DOI,'archive_md5':digest,'archive_sha256':s.hexdigest(),
            'md5_matches_official':digest==PINNED_MD5,
            'expected_tables_present':not missing,'missing_or_ambiguous_roles':missing,
            'roles':found,'file_count':len(zip_entries),
            'GT_accessed':False,'test_tables_opened':False,
            'validation_completed':False,
            'warning':'File listing only: neither feature construction nor empirical scoring performed'}


if __name__ == '__main__':
    import argparse, json
    parser=argparse.ArgumentParser(description='Inspect official DLULIB ZIP identity and file names only; never parse test labels')
    parser.add_argument('zip_path')
    args=parser.parse_args()
    print(json.dumps(audit_archive(args.zip_path),indent=2))
