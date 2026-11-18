#!/usr/bin/env python3
"""Fits the six DLULIB position estimators on external TRAINING observations only."""
from pathlib import Path
import argparse,hashlib,pickle,json,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from jepformer.dlulib_stage10_models import positioning_models,ESTIMATORS

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    p=argparse.ArgumentParser();p.add_argument('--workspace',required=True,type=Path)
    a=p.parse_args();tr=a.workspace/'ingest/train_arrays';out=a.workspace/'frozen_models';out.mkdir(exist_ok=True)
    assert not (out/'POSITION_MODELS_FROZEN_BEFORE_TEST_INPUT.json').exists(),'Locked model inventory exists'
    done=[]
    for floor in (1,2,3):
        training=tr/f'floor{floor}_All_20_TRAIN_ONLY.npz'
        with np.load(training,allow_pickle=False) as z:rss=z['rss'];xy=z['xy']
        X=np.where(rss>-100,rss,0.).astype(np.float32)
        for name,mdl in positioning_models().items():
            if name in ('KNN','WKNN'):mdl.fit(X)
            else:mdl.fit(X,xy)
            path=out/f'floor{floor}__{name.replace(" ","_")}.pkl'
            with path.open('wb') as f:pickle.dump(mdl,f,protocol=4)
            done.append({'floor':floor,'estimator':name,'position_model_sha256':sha(path),
                         'training_n':len(X),'training_file_sha256':sha(training)})
    (out/'POSITION_MODELS_FROZEN_BEFORE_TEST_INPUT.json').write_text(json.dumps({'train_only':True,'models':done},indent=2))
    print('Frozen',len(done),'training-only position models')
if __name__=='__main__':main()
