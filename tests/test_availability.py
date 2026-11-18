import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import pytest
from jepformer.availability import rebuild_for_available


def test_dropped_coordinates_are_not_read():
    rng=np.random.default_rng(123)
    x=rng.normal(size=(20,6,33)).astype('float32')
    xy=rng.normal(size=(20,6,2))
    mask=np.array([True,False,True,True,True,True])
    a=rebuild_for_available(x,xy,mask)
    bxy=xy.copy();bxy[:,1,:]+=1e7
    b=rebuild_for_available(x,bxy,mask)
    np.testing.assert_array_equal(np.isnan(a),np.isnan(b))
    np.testing.assert_array_equal(np.nan_to_num(a),np.nan_to_num(b))
    assert np.isnan(a[:,1]).all()
    assert a.shape==(20,6,33)


def test_missing_geometry_anchor_is_flagged():
    x=np.ones((4,6,33),dtype='float32')
    xy=np.arange(48,dtype='float64').reshape(4,6,2)
    mask=np.array([True,True,True,False,True,False])
    out=rebuild_for_available(x,xy,mask)
    assert np.isnan(out[:,mask,16]).all() # WKNN anchor absent (G3)
    assert np.isnan(out[:,mask,17]).all() # KNN anchor absent (G4)
    assert np.isfinite(out[:,mask,18]).all() # nearest-neighbor distance remains defined


def test_shapes_and_minimum_available():
    with pytest.raises(ValueError):
        rebuild_for_available(np.ones((2,6,33),dtype='float32'),np.ones((2,6,2)),np.array([True,False,False,False,False,False]))
