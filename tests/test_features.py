import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
import numpy as np
from jepformer.features import geometry_descriptors,assemble_33
from jepformer.normalization import DescriptorScaler

def test_geometry_shared():
    rng=np.random.default_rng(1)
    xy=rng.normal(size=(9,6,2));anchor=rng.normal(size=(9,2))
    g=geometry_descriptors(xy,anchor)
    assert g.shape==(9,6,12)
    assert np.allclose(g[:,:,8:],g[:,0:1,8:])

def test_feature_schema_and_missing_flags():
    rng=np.random.default_rng(3)
    s=rng.normal(size=(4,14));xy=rng.normal(size=(4,6,2));a=rng.normal(size=(4,2));loc=rng.normal(size=(4,6,7))
    x=assemble_33(s,geometry_descriptors(xy,a),loc)
    x[0,0,22]=np.nan
    norm=DescriptorScaler().fit(x)
    y=norm.transform(x)
    assert y.shape==(4,6,66) and np.isfinite(y).all()
    assert y[0,0,55]==1
