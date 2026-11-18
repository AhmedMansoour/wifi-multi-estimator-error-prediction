#!/usr/bin/env python3
"""Train JEPFormer and CatBoost on artificial examples only; metrics not scientific."""
import argparse,json,sys
from pathlib import Path
import numpy as np,torch
from catboost import CatBoostRegressor
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from jepformer.normalization import DescriptorScaler
from jepformer.models import JEPFormer,stage13_multitask_loss

def load(path,name):
    with np.load(path/(name+".npz")) as data:return data["features"],data["true_errors"]

def main():
    p=argparse.ArgumentParser();p.add_argument("--data",default="examples/synthetic");p.add_argument("--epochs",type=int,default=4);a=p.parse_args()
    path=Path(a.data)
    tr,ytr=load(path,"development");ca,yca=load(path,"calibration");te,yte=load(path,"test")
    scaler=DescriptorScaler().fit(tr)
    xtr,xca,xte=[scaler.transform(z) for z in [tr,ca,te]]
    def flat(x):
        n=len(x);return np.column_stack([x.reshape(n*6,-1),np.tile(np.arange(6),n)])
    cb=CatBoostRegressor(iterations=40,depth=4,learning_rate=.08,random_seed=12,verbose=False,allow_writing_files=False)
    cb.fit(flat(xtr),ytr.ravel(),eval_set=(flat(xca),yca.ravel()),verbose=False)
    pcat=np.maximum(0,cb.predict(flat(xte)).reshape(-1,6))
    torch.set_num_threads(2);torch.manual_seed(12)
    net=JEPFormer();opt=torch.optim.AdamW(net.parameters(),lr=.0012)
    for _ in range(a.epochs):
        net.train();opt.zero_grad();loss=stage13_multitask_loss(net(torch.from_numpy(xtr)),torch.from_numpy(ytr));loss.backward();opt.step()
    net.eval()
    with torch.no_grad():pnet=net(torch.from_numpy(xte))[0].numpy()
    print(json.dumps({"type":"synthetic engineering smoke test only", "test_scans":len(te),
      "CatBoost_toy_mae":float(np.abs(pcat-yte).mean()),"JEPFormer_toy_mae":float(np.abs(pnet-yte).mean())},indent=2))
if __name__=="__main__":main()
