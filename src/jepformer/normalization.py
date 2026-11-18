"""Train-only descriptor normalization (public reference implementation)."""
import numpy as np
class DescriptorScaler:
    def fit(self,x):
        a=np.asarray(x,dtype=float)
        if a.ndim!=3 or a.shape[1:]!=(6,33):raise ValueError("Expected (n,6,33)")
        self.median=np.nanmedian(np.where(np.isfinite(a),a,np.nan),axis=(0,1))
        self.median=np.where(np.isfinite(self.median),self.median,0)
        b=np.where(np.isfinite(a),a,self.median)
        self.lo=np.quantile(b,.005,axis=(0,1));self.hi=np.quantile(b,.995,axis=(0,1))
        b=np.clip(b,self.lo,self.hi)
        self.mean=np.mean(b,axis=(0,1));self.std=np.std(b,axis=(0,1))
        self.std=np.where(self.std>1e-8,self.std,1)
        return self
    def transform(self,x):
        a=np.asarray(x,dtype=float)
        if a.ndim!=3 or a.shape[1:]!=(6,33):raise ValueError("Expected (n,6,33)")
        missing=(~np.isfinite(a)).astype("float32")
        b=np.where(np.isfinite(a),a,self.median)
        b=np.clip(b,self.lo,self.hi)
        b=np.clip((b-self.mean)/self.std,-8,8).astype("float32")
        return np.concatenate((b,missing),axis=-1)
    def fit_transform(self,x):return self.fit(x).transform(x)
