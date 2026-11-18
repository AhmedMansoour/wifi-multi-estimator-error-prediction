"""Exact archived Stage13/Stage8 six-slot forecast architecture and external position models.

The research checkpoints are NOT distributed in this repository. This module
supplies an auditable source-compatible loader, not pre-trained model weights.
"""
import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from sklearn.neighbors import NearestNeighbors
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from catboost import CatBoostRegressor

ESTIMATORS=('CatBoost','Extra Trees','Gradient Boosting','KNN','Random Forest','WKNN')
SEEDS=(11,21,31)

class Head(nn.Module):
    def __init__(self,d):
        super().__init__()
        self.error=nn.Linear(d,1)
        self.tail=nn.Linear(d,1)
        self.win=nn.Sequential(nn.Linear(d*2,48),nn.GELU(),nn.Linear(48,1))
        nn.init.constant_(self.error.bias,3.)

    def forward(self,z):
        w=z[:,5:6].expand(-1,5,-1)
        other=(0,1,2,3,4)
        return (F.softplus(self.error(z)).squeeze(-1),
                self.tail(z).squeeze(-1),
                self.win(torch.cat((z[:,other],w),-1)).squeeze(-1))

class Transformer(nn.Module):
    def __init__(self,din=66):
        super().__init__()
        self.proj=nn.Linear(din,64)
        self.id=nn.Embedding(6,64)
        layer=nn.TransformerEncoderLayer(64,4,128,dropout=.10,activation='gelu',
                                         batch_first=True,norm_first=True)
        self.enc=nn.TransformerEncoder(layer,2,enable_nested_tensor=False)
        self.norm=nn.LayerNorm(64)
        self.head=Head(64)

    def forward(self,x):
        if x.ndim!=3 or x.shape[1:]!=(6,66):
            raise ValueError('Expected x shape (batch,6,66)')
        pos=self.proj(x)+self.id(torch.arange(6,device=x.device))[None]
        return self.head(self.norm(self.enc(pos)))


def positioning_models():
    """Fixed DLULIB new-site training settings, locked before test scoring."""
    return {
      'CatBoost': CatBoostRegressor(loss_function='MultiRMSE',eval_metric='MultiRMSE',
                 iterations=800,depth=6,learning_rate=.05,l2_leaf_reg=3.,random_seed=42,
                 od_type='Iter',od_wait=80,bootstrap_type='Bayesian',rsm=.9,
                 thread_count=3,allow_writing_files=False,verbose=False),
      'Extra Trees': ExtraTreesRegressor(n_estimators=250,max_features='sqrt',
                 min_samples_leaf=2,random_state=42,n_jobs=3),
      'Gradient Boosting': MultiOutputRegressor(HistGradientBoostingRegressor(
                 max_iter=120,learning_rate=.08,max_leaf_nodes=31,
                 l2_regularization=.05,early_stopping=True,random_state=42)),
      'Random Forest': RandomForestRegressor(n_estimators=80,max_depth=18,
                 min_samples_leaf=2,max_features='sqrt',n_jobs=3,random_state=42),
      'KNN': NearestNeighbors(n_neighbors=6,metric='euclidean',n_jobs=3),
      'WKNN': NearestNeighbors(n_neighbors=6,metric='euclidean',n_jobs=3),
    }


def candidate_coordinates(models,train_rss,train_xy,query_rss):
    """Source-compatible candidate outputs from six training-only position methods."""
    X=np.where(np.asarray(query_rss)>-100,query_rss,0.).astype('float32')
    coords=np.zeros((len(X),6,2),dtype='float64')
    for j,name in enumerate(ESTIMATORS):
        mdl=models[name]
        if name in ('KNN','WKNN'):
            dist,idx=mdl.kneighbors(X)
            p=np.asarray(train_xy)[idx]
            if name=='KNN':coords[:,j]=p.mean(axis=1)
            else:
                w=np.power(dist+1e-6,-2)
                w/=w.sum(axis=-1,keepdims=True)
                coords[:,j]=(p*w[:,:,None]).sum(axis=1)
        else:
            coords[:,j]=mdl.predict(X)
    if not np.isfinite(coords).all():
        raise ValueError('Nonfinite candidate position')
    return coords
