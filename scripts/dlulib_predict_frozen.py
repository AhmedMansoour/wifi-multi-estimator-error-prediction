#!/usr/bin/env python3
"""DLULIB inference ONLY: source-trained error predictors are never fitted on DLULIB.

REQUIRES user-supplied restricted original source checkpoints. Nothing in this
script reads the sealed test coordinates. Never rerun after predictions are frozen.
"""
from pathlib import Path
import argparse,json,hashlib,pickle,sys
import numpy as np
import torch
from catboost import CatBoostRegressor
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from jepformer.dlulib_features import scan14,geometry12,candidate_local7,assemble33,source_normalize
from jepformer.dlulib_stage10_models import Transformer,ESTIMATORS,SEEDS,candidate_coordinates

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--workspace',required=True,type=Path)
    parser.add_argument('--source-models',required=True,type=Path,help='Restricted frozen Stage8 source checkpoint folder')
    parser.add_argument('--source-scaler',required=True,type=Path,help='Unchanged original source-only normalizer')
    a=parser.parse_args()
    root=a.workspace
    out=root/'predictions_frozen';out.mkdir(exist_ok=True)
    lock=out/'PREDICTIONS_FROZEN_BEFORE_GT.json'
    if lock.exists():raise RuntimeError('Predictions already frozen; no rerun/overwrite permitted')
    if not (root/'frozen_models/POSITION_MODELS_FROZEN_BEFORE_TEST_INPUT.json').exists():
        raise RuntimeError('Position estimators must be frozen first')
    cb=CatBoostRegressor();cb.load_model(str(a.source_models/'stage8_availability_aware_catboost_PRIVATE.cbm'))
    nets={}
    for seed in SEEDS:
        ckpt=torch.load(a.source_models/f'stage8_availability_aware_transformer_seed{seed}_PRIVATE.pt',
                        map_location='cpu',weights_only=True)
        net=Transformer(66);net.load_state_dict(ckpt['model_state']);net.eval();nets[seed]=net
    freeze={'study':'DLULIB first-use external prediction','original_GT_accessed':False,
            'source_checkpoint_SHA256':{'CatBoost':sha(a.source_models/'stage8_availability_aware_catboost_PRIVATE.cbm'),
                                      **{str(seed):sha(a.source_models/f'stage8_availability_aware_transformer_seed{seed}_PRIVATE.pt') for seed in SEEDS}},
            'scaler_sha256':sha(a.source_scaler),'source_error_models_retrained_on_DLULIB':False,
            'files':[],'estimator_order':ESTIMATORS,'JEPFormer_seeds':SEEDS}
    for floor in (1,2,3):
        with np.load(root/f'inference_only/floor{floor}_INFERENCE_ONLY.npz',allow_pickle=False) as z:
            rss=z['rss'];scan_id=z['scan_id'];floor_labels=z['floor_context']
        assert np.all(floor_labels==floor)
        with np.load(root/f'ingest/train_arrays/floor{floor}_All_20_TRAIN_ONLY.npz',allow_pickle=False) as z:
            tr=z['rss'];trxy=z['xy']
        mdl={}
        for name in ESTIMATORS:
            with (root/'frozen_models'/f'floor{floor}__{name.replace(" ","_")}.pkl').open('rb') as f:
                mdl[name]=pickle.load(f)
        cand=candidate_coordinates(mdl,tr,trxy,rss)
        f,anchor=scan14(tr,trxy,rss)
        raw=assemble33(f,geometry12(cand,anchor),candidate_local7(tr,trxy,rss,cand))
        x=source_normalize(raw,a.source_scaler)
        if not np.isfinite(x).all():raise ValueError('Nonfinite normalized features')
        flat=np.column_stack((x.reshape(-1,66),np.tile(np.arange(6,dtype='float32'),len(x))))
        cat=np.maximum(0,cb.predict(flat).reshape(-1,6)).astype('float32')
        ps=[]
        for seed in SEEDS:
            net=nets[seed];v=[]
            with torch.no_grad():
                for i in range(0,len(x),256):v.append(net(torch.from_numpy(x[i:i+256]))[0].numpy())
            ps.append(np.concatenate(v).astype('float32'))
        path=out/f'floor{floor}_FROZEN_PREDICTIONS_NO_GT.npz'
        np.savez_compressed(path,scan_id=scan_id,known_floor=floor_labels,
            candidate_xy=cand,predicted_catboost=cat,predicted_jepformer=np.stack(ps),
            diagnostic_scan14=f,features_full33=raw)
        freeze['files'].append({'floor':floor,'n_scans':len(x),'predictions_sha256':sha(path),
                                'inference_only_sha256':sha(root/f'inference_only/floor{floor}_INFERENCE_ONLY.npz')})
        print('Frozen external forecasts floor',floor,'n',len(x),'sha256',sha(path))
    lock.write_text(json.dumps(freeze,indent=2))
    print('FROZEN BEFORE SCORING',sha(lock))
if __name__=='__main__':main()
