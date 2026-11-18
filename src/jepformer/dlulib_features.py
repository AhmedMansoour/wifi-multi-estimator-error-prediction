"""Externally frozen DLULIB diagnostic feature adapter.

Derived from the independently published ESWA source `src/wifi_integrity/reliability/indicators.py`
and the original JEPFormer Stage9 `make_geometry` and `map_features` functions.
Only training-map RSS and inference-only query RSS are permitted inputs. Ground truth
and physical test point coordinates MUST NOT enter this file.
"""
from __future__ import annotations
import numpy as np
from scipy.spatial import cKDTree, distance

RSS_MISSING = -100.
RSS_FLOOR = -110.
K_NEIGHBORS = 20
K_GEOMETRY = 10
K_LOCAL = 12
EST = ('CatBoost','Extra Trees','Gradient Boosting','KNN','Random Forest','WKNN')

def observed_and_diagnostic_rss(a):
    a=np.asarray(a,dtype=np.float32)
    if a.ndim!=2 or a.shape[1]!=17:raise ValueError('17 AP RSS columns required')
    present=np.isfinite(a)&(a>RSS_MISSING)
    return np.where(present,a,RSS_FLOOR).astype(np.float32), present

def template_rss(train_rss,train_xy):
    a,obs=observed_and_diagnostic_rss(train_rss)
    xy=np.asarray(train_xy,dtype=np.float64)
    key,inv=np.unique(np.round(xy,3),axis=0,return_inverse=True)
    n=len(key)
    cnt=np.bincount(inv,minlength=n).astype(np.float64)
    s=np.zeros((n,a.shape[1]),dtype=np.float64)
    np.add.at(s,inv,a.astype(np.float64))
    template=(s/cnt[:,None]).astype(np.float32)
    o=np.zeros((n,17),dtype=np.int32);np.add.at(o,inv,obs.astype(np.int32))
    xy_sum=np.zeros((n,2),dtype=np.float64);np.add.at(xy_sum,inv,xy)
    return template,o>0,xy_sum/cnt[:,None]

def _adaptive_density_radius(xy):
    if len(xy)<5:return 5.
    vals=cKDTree(xy).query(xy,k=2)[0][:,1]
    vals=vals[np.isfinite(vals)&(vals>0)]
    return float(np.clip(np.median(vals)*3.,2.,25.)) if len(vals) else 5.

def scan14(train_rss,train_xy,query_rss,batch=256):
    """Return (n,14) in original F order and (n,2) training-only anchor."""
    tr,to,xy=template_rss(train_rss,train_xy)
    q,qo=observed_and_diagnostic_rss(query_rss)
    n=len(q);out=np.full((n,14),np.nan,dtype=np.float32)
    anchor=np.zeros((n,2),dtype=np.float64)
    unique_xy=np.unique(xy,axis=0)
    denradius=_adaptive_density_radius(unique_xy)
    tree=cKDTree(unique_xy)
    k=min(K_NEIGHBORS,len(tr));kg=min(K_GEOMETRY,k)
    if k<10:raise ValueError('at least ten training templates required')
    # Source uses normalized Euclidean RSS distance with filled -110 absent APs.
    for lo in range(0,n,batch):
        hi=min(n,lo+batch)
        sub=q[lo:hi]
        dst=np.maximum(distance.cdist(sub.astype('float32'),tr.astype('float32'),metric='sqeuclidean'),0.0)
        ix=np.argsort(dst,axis=1,kind='stable')[:,:k]
        vals=np.sqrt(np.take_along_axis(dst,ix,axis=1))/np.sqrt(q.shape[1])
        for rel in range(hi-lo):
            rid=lo+rel
            cand=ix[rel];dd=vals[rel]
            pts=xy[cand[:kg]]
            centroid=pts.mean(axis=0);anchor[rid]=centroid
            spread=float(np.sqrt(np.mean(np.sum((pts-centroid)**2,axis=-1))))
            dia=float(np.max(distance.pdist(pts))) if len(pts)>1 else 0.
            cum=np.cumsum(pts,axis=0)/np.arange(1,kg+1)[:,None]
            instability=float(np.max(np.linalg.norm(cum-cum[-1],axis=-1)))
            minrss=float(dd[0]);second=float(dd[1]);kth=float(dd[kg-1])
            isolation=max(second-minrss,0)/(second+1e-6)
            grad=spread/max(kth-minrss,1e-6)
            overlap=(to[cand[:kg]]&qo[rid]).sum(axis=1)
            union=(to[cand[:kg]]|qo[rid]).sum(axis=1)
            jacc=overlap/np.maximum(union,1)
            maxjac=float(jacc.max());meanjac=float(jacc.mean())
            a=q[rid].astype(float)-RSS_FLOOR;b=tr[cand[0]].astype(float)-RSS_FLOOR
            den=np.linalg.norm(a)*np.linalg.norm(b)
            cosine=float(np.dot(a,b)/den) if den>0 else np.nan
            density=float(len(tree.query_ball_point(centroid,r=denradius)))
            rvals=np.asarray(query_rss[rid],dtype=float)[qo[rid]]
            sd=float(np.std(rvals)) if len(rvals) else np.nan
            span=float(np.max(rvals)-np.min(rvals)) if len(rvals) else np.nan
            out[rid]=[minrss,isolation,cosine,spread,dia,instability,grad,maxjac,meanjac,
                      1-maxjac,density,int(qo[rid].sum()),sd,span]
    return out,anchor

def geometry12(xy,anchor):
    xy=np.asarray(xy,dtype='float64');anc=np.asarray(anchor,dtype='float64')
    if xy.ndim!=3 or xy.shape[1:]!=(6,2) or anc.shape!=(len(xy),2):raise ValueError('bad candidate/anchor dimensions')
    d=np.linalg.norm(xy[:,:,None,:]-xy[:,None,:,:],axis=-1)
    ds=np.sort(d+np.eye(6)[None,:,:]*1e7,axis=-1)
    med=np.median(xy,axis=1,keepdims=True)
    cm=np.linalg.norm(xy-med,axis=-1)
    ad=np.linalg.norm(xy-anc[:,None,:],axis=-1)
    n=len(xy);tile=lambda v:np.broadcast_to(v[:,None],(n,6))
    return np.stack([cm,ad,d[:,:,5],d[:,:,3],ds[:,:,0],ds[:,:,:3].mean(axis=-1),
                     d.sum(axis=-1)/5.,ds[:,:,-2],tile(np.median(cm,axis=1)),
                     tile(np.max(cm,axis=1)),tile(np.median(ad,axis=1)),tile(np.max(ad,axis=1))],axis=-1).astype('float32')

def candidate_local7(train_rss,train_xy,query_rss,xy,batch=500):
    """Exact Stage9 candidate-local radio-map features from 12 training *scans*."""
    train,to=observed_and_diagnostic_rss(train_rss)
    q,qo=observed_and_diagnostic_rss(query_rss)
    n=len(q);nn=K_LOCAL
    tree=cKDTree(np.asarray(train_xy,dtype=float))
    idx=tree.query(np.asarray(xy).reshape(-1,2),k=nn)[1]
    loc=np.full((n*6,7),np.nan,dtype='float32')
    for st in range(0,len(loc),batch):
        en=min(st+batch,len(loc));nb=idx[st:en];jj=np.arange(st,en)//6
        shared=qo[jj,None,:]&to[nb]
        numer=shared.sum(-1)
        union=(qo[jj,None,:]|to[nb]).sum(-1)
        dd=np.abs(q[jj,None,:]-train[nb]);rss=np.where(numer>0,(dd*shared).sum(-1)/np.maximum(numer,1),50.)
        jac=numer/np.maximum(union,1);pen=rss+35*(1-jac);best=pen.argmin(-1)
        row=np.arange(len(jj))
        loc[st:en]=np.column_stack([rss.min(-1),np.median(rss,axis=-1),jac[row,best],jac.mean(-1),
              numer[row,best],(numer/np.maximum(qo[jj].sum(-1)[:,None],1))[row,best],pen.min(-1)])
    return loc.reshape(n,6,7)

def assemble33(scan,geom,local):
    n=len(scan)
    if scan.shape!=(n,14) or geom.shape!=(n,6,12) or local.shape!=(n,6,7):raise ValueError('33-feature block shape mismatch')
    return np.concatenate([np.broadcast_to(scan[:,None,:],(n,6,14)),geom,local],axis=-1).astype('float32')

def source_normalize(raw,scaler_path):
    raw=np.asarray(raw,dtype='float32')
    with np.load(scaler_path,allow_pickle=False) as z:s={k:z[k] for k in z.files}
    bad=~np.isfinite(raw)
    val=np.where(bad,s['median'],raw)
    return np.concatenate([np.clip((np.clip(val,s['lo'],s['hi'])-s['mean'])/s['std'],-8,8).astype('float32'),bad.astype('float32')],axis=-1)
