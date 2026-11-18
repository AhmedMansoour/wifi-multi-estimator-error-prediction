import sys
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from jepformer.tail_diagnostics import tail_metrics,summarize_patterns,pattern_mask


def test_unavailable_candidates_have_no_effect():
    truth=np.array([[1.,12.,22.],[4.,5.,8.],[13.,2.,11.]],dtype=float)
    pred=np.array([[2.,7.,12.],[3.,4.,7.],[8.,3.,6.]],dtype=float)
    active=pattern_mask(3,3,[1])
    a=tail_metrics(pred,truth,active)
    pred[:,1]=1e9;truth[:,1]=1e9
    b=tail_metrics(pred,truth,active)
    assert a==b
    assert a['targets']==6


def test_tail_bias_and_severe_denominators():
    y=np.array([[2,10,14],[3,9,20]],float)
    p=np.array([[2,6,16],[5,10,12]],float)
    m=tail_metrics(p,y,np.ones_like(y,dtype=bool))
    assert m['true_tail_count']==3
    assert m['tail_underprediction_fraction']==pytest.approx(2/3)
    assert m['conditional_tail_mae_m']==pytest.approx((4+2+8)/3)


def test_constant_label_auroc_is_unavailable():
    y=np.array([[1.,2.],[2.,3.]])
    p=y+0.5
    m=tail_metrics(p,y,np.ones_like(y,dtype=bool))
    assert m['tail_auc'] is None and m['tail_average_precision'] is None


def test_pattern_means_are_unweighted():
    a={'mae_m':1.,'bias_pred_minus_true_m':0.,'true_tail_rate':0.1,'conditional_tail_mae_m':None,
       'conditional_tail_signed_bias_m':None,'tail_underprediction_fraction':None,
       'tail_auc':None,'tail_average_precision':None,'tail_recall_at_empirical_5pct_fpr':None}
    b=a.copy();b['mae_m']=3.;b['bias_pred_minus_true_m']=2.
    c=summarize_patterns([a,b]); assert c['mae_m']==2. and c['n_patterns']==2
