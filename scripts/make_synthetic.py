#!/usr/bin/env python3
"""Artificial six-estimator benchmark. Synthetic outputs are NOT paper validation."""
import argparse,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from jepformer.features import geometry_descriptors,assemble_33

def generate(n,seed):
    rng=np.random.default_rng(seed)
    true=rng.uniform(0,60,(n,2))
    scan=rng.normal(size=(n,14)).astype("float32")
    anchor=true+rng.normal(0,5,(n,2))
    cand=true[:,None,:]+rng.normal(size=(n,6,2))*np.asarray([2,3,4,5,6,4])[None,:,None]
    common=rng.random(n)<.10
    cand[common]+=rng.normal(0,12,(common.sum(),1,2))
    loc=rng.normal(size=(n,6,7)).astype("float32")
    x=assemble_33(scan,geometry_descriptors(cand,anchor),loc)
    y=np.linalg.norm(cand-true[:,None,:],axis=-1).astype("float32")
    return x,y

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",default="examples/synthetic");p.add_argument("--seed",type=int,default=123);a=p.parse_args()
    out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
    for idx,(name,n) in enumerate([("development",240),("calibration",80),("test",80)]):
        x,y=generate(n,a.seed+idx)
        np.savez_compressed(out/(name+".npz"),features=x,true_errors=y)
    print("Created synthetic-only examples in",out)
if __name__=="__main__":main()
