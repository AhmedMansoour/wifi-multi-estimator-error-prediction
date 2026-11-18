import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import numpy as np
import torch
from jepformer.availability_training import augmentation_masks,augment_six_estimator_scans,masked_multitask_loss,forward_masked_jepformer
from jepformer.normalization import DescriptorScaler
from jepformer.models import JEPFormer,stage13_multitask_loss

def test_fixed_patterns_and_mask_counts():
    a=augmentation_masks(42,81026);b=augmentation_masks(42,81026)
    assert a.shape==(168,6) and np.array_equal(a,b)
    assert [np.unique((~chunk).sum(-1)).tolist() for chunk in np.split(a,4)]==[[0],[1],[2],[3]]

def test_labels_do_not_determine_feature_masks():
    rng=np.random.default_rng(18)
    x=rng.normal(size=(16,6,33)).astype('float32');xy=rng.normal(size=(16,6,2));y=rng.normal(size=(16,6)).astype('float32')
    scaler=DescriptorScaler().fit(x)
    a,ya,ma=augment_six_estimator_scans(x,xy,y,scaler,81026)
    b,yb,mb=augment_six_estimator_scans(x,xy,y+30,scaler,81026)
    assert a.shape==(64,6,66) and np.array_equal(a,b) and np.array_equal(ma,mb)
    assert not np.array_equal(ya,yb)

def test_masked_loss_original_when_all_available():
    torch.manual_seed(16)
    out=(torch.rand(8,6,requires_grad=True),torch.randn(8,6,requires_grad=True),torch.randn(8,5,requires_grad=True))
    y=torch.rand(8,6)*15
    a=masked_multitask_loss(out,y,torch.ones(8,6,dtype=torch.bool))
    b=stage13_multitask_loss(out,y)
    torch.testing.assert_close(a,b)
    a.backward()
    assert all(z.grad is not None for z in out)

def test_wknn_absent_and_transformer_mask_backprop():
    torch.manual_seed(42)
    net=JEPFormer()
    inp=torch.randn(4,6,66)
    av=torch.tensor([[True,True,True,True,True,False]]*4)
    y=torch.rand(4,6)
    outputs=forward_masked_jepformer(net,inp,av)
    loss=masked_multitask_loss(outputs,y,av)
    assert bool(torch.isfinite(loss))
    loss.backward()
    assert net.proj.weight.grad is not None
