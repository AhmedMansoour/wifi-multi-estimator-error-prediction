"""Research-only candidate availability adapter, no empirical data bundled.

The original trained six-estimator models are NOT validated variable-set predictors.
This module reconstructs available-candidate geometry without inventing missing
coordinates. Numeric features are *raw* (before the development-fitted scaler).
"""
import numpy as np

ORDER = ("CatBoost", "Extra Trees", "Gradient Boosting", "KNN", "Random Forest", "WKNN")
KNN_INDEX = 3
WKNN_INDEX = 5


def rebuild_for_available(raw33, candidate_xy, available):
    """Return (n,6,33), NaNs for absent tokens and undefined references.

    Parameters
    ----------
    raw33 : (n,6,33) original observable descriptors, not normalized
    candidate_xy : (n,6,2) estimator output coordinates in a metric frame
    available : (6,) boolean availability mask, at least 2 True

    Descriptor order matches the archived Stage9/13 14+12+7 scheme.
    Feature 15 (zero-based) is the observed diagnostic-anchor distance.
    It does not depend on a missing candidate and is retained unchanged.
    Missing candidate positions are NOT accessed. True query coordinates
    and observed position errors are never used.
    """
    x=np.asarray(raw33,dtype=np.float32)
    xy=np.asarray(candidate_xy,dtype=np.float64)
    mask=np.asarray(available,dtype=bool)
    if x.ndim!=3 or x.shape[1:]!=(6,33):raise ValueError('raw33 shape must be (n,6,33)')
    if xy.shape!=(len(x),6,2):raise ValueError('candidate_xy shape must be (n,6,2)')
    if mask.shape!=(6,) or mask.sum()<2:raise ValueError('At least two available estimators required')
    ix=np.flatnonzero(mask);m=len(ix);n=len(x)
    coords=xy[:,ix,:]
    if not np.isfinite(coords).all():raise ValueError('Available candidate coordinates must be finite')
    o=x.copy();o[:,~mask,:]=np.nan
    dist=np.linalg.norm(coords[:,:,None,:]-coords[:,None,:,:],axis=-1)
    sorted_dist=np.sort(dist+np.eye(m)[None,:,:]*1e7,axis=-1)
    med=np.median(coords,axis=1,keepdims=True)
    cm=np.linalg.norm(coords-med,axis=-1)
    ad=x[:,ix,15].astype('float64')
    tile=lambda a: np.broadcast_to(a[:,None],(n,m))
    g=np.full((n,m,12),np.nan,dtype=np.float64)
    g[:,:,0]=cm
    g[:,:,1]=ad
    if mask[WKNN_INDEX]:g[:,:,2]=dist[:,:,np.flatnonzero(ix==WKNN_INDEX)[0]]
    if mask[KNN_INDEX]:g[:,:,3]=dist[:,:,np.flatnonzero(ix==KNN_INDEX)[0]]
    g[:,:,4]=sorted_dist[:,:,0]
    g[:,:,5]=sorted_dist[:,:,:min(3,m-1)].mean(axis=-1)
    g[:,:,6]=dist.sum(axis=-1)/(m-1)
    g[:,:,7]=sorted_dist[:,:,-2]
    g[:,:,8]=tile(np.median(cm,axis=1))
    g[:,:,9]=tile(np.max(cm,axis=1))
    g[:,:,10]=tile(np.median(ad,axis=1))
    g[:,:,11]=tile(np.max(ad,axis=1))
    o[:,ix,14:26]=g.astype('float32')
    return o
