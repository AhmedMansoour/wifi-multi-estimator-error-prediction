"""Synthetic-safe six-estimator geometry descriptors, matching the archived G1--G12."""
import numpy as np
ESTIMATORS=("CatBoost","Extra Trees","Gradient Boosting","KNN","Random Forest","WKNN")

def geometry_descriptors(candidate_xy, diagnostic_anchor_xy):
    """Candidate XY: (n,6,2), anchor: (n,2), in one metric coordinate frame.

    Anchor must come from observed scan/training map, never query ground truth.
    G9--G12 are common to all candidates; G1--G8 are position specific.
    """
    xy=np.asarray(candidate_xy,dtype=float)
    anchor=np.asarray(diagnostic_anchor_xy,dtype=float)
    if xy.ndim!=3 or xy.shape[1:]!=(6,2) or anchor.shape!=(len(xy),2):
        raise ValueError("Expected candidate_xy (n,6,2) and anchor (n,2)")
    if not (np.isfinite(xy).all() and np.isfinite(anchor).all()):
        raise ValueError("Nonfinite coordinates")
    n=len(xy);k=6
    d=np.linalg.norm(xy[:,:,None,:]-xy[:,None,:,:],axis=-1)
    near=np.sort(d+np.eye(k)[None,:,:]*1e7,axis=-1)
    med=np.median(xy,axis=1,keepdims=True)
    cm=np.linalg.norm(xy-med,axis=-1)
    ad=np.linalg.norm(xy-anchor[:,None,:],axis=-1)
    tile=lambda v:np.broadcast_to(v[:,None],(n,k))
    return np.stack([cm,ad,d[:,:,5],d[:,:,3],near[:,:,0],near[:,:,:3].mean(-1),
                     d.sum(-1)/(k-1),near[:,:,-2],tile(np.median(cm,axis=1)),
                     tile(np.max(cm,axis=1)),tile(np.median(ad,axis=1)),
                     tile(np.max(ad,axis=1))],axis=-1).astype("float32")

def assemble_33(scan14,geometry12,candidate_local7):
    s=np.asarray(scan14,dtype="float32")
    g=np.asarray(geometry12,dtype="float32")
    l=np.asarray(candidate_local7,dtype="float32")
    if s.ndim!=2 or s.shape[1]!=14 or g.shape!=(len(s),6,12) or l.shape!=(len(s),6,7):
        raise ValueError("Expected (n,14), (n,6,12), (n,6,7)")
    return np.concatenate([np.broadcast_to(s[:,None,:],(len(s),6,14)),g,l],axis=-1)
