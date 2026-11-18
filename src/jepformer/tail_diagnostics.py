"""Deterministic, ground-truth-dependent offline evaluation of error forecasts.

This module does not produce deployment safety decisions or calibrated bounds.
It aggregates predictions only for candidates explicitly flagged as available.
No training or fitting occurs here.
"""
from __future__ import annotations
import numpy as np


def _validate(predicted, actual, available):
    p = np.asarray(predicted, dtype=float)
    y = np.asarray(actual, dtype=float)
    a = np.asarray(available, dtype=bool)
    if p.ndim != 2 or p.shape != y.shape or p.shape != a.shape:
        raise ValueError('predicted, actual, available must be identically shaped (n_scans,n_estimators)')
    if not np.isfinite(y[a]).all() or not np.isfinite(p[a]).all():
        raise ValueError('All evaluated predictions/targets must be finite')
    if (p[a] < 0).any() or (y[a] < 0).any():
        raise ValueError('Positioning errors must be nonnegative')
    if not a.any():
        raise ValueError('At least one candidate must be available')
    return p[a], y[a]


def tail_metrics(predicted, actual, available, tail_threshold=10.0):
    """Score one fixed model/pattern; no test-driven thresholds or calibration.

    AP prevalence depends on the target and is therefore separately reported.
    Recall at 5% FPR uses an empirical retrospective threshold, *not* a
    predefined deployment decision rule. Do not call it operational detection.
    """
    from sklearn.metrics import roc_auc_score, average_precision_score, roc_curve
    p, y = _validate(predicted, actual, available)
    err = p-y
    t = y >= float(tail_threshold)
    result = {
        'targets': int(len(y)),
        'mae_m': float(np.abs(err).mean()),
        'bias_pred_minus_true_m': float(err.mean()),
        'true_tail_rate': float(t.mean()),
        'true_tail_count': int(t.sum()),
        'conditional_tail_mae_m': None,
        'conditional_tail_signed_bias_m': None,
        'tail_underprediction_fraction': None,
        'tail_auc': None,
        'tail_average_precision': None,
        'tail_recall_at_empirical_5pct_fpr': None,
    }
    if t.any():
        result['conditional_tail_mae_m']=float(np.abs(err[t]).mean())
        result['conditional_tail_signed_bias_m']=float(err[t].mean())
        result['tail_underprediction_fraction']=float((err[t]<0).mean())
    if t.any() and (~t).any():
        result['tail_auc']=float(roc_auc_score(t,p))
        result['tail_average_precision']=float(average_precision_score(t,p))
        fpr,tpr,_=roc_curve(t,p)
        # conservative step evaluation at <= 5% of observed FPR grid
        result['tail_recall_at_empirical_5pct_fpr']=float(np.max(tpr[fpr<=.05]))
    return result


def summarize_patterns(per_pattern):
    """Arithmetic (not scan-weighted) mean over distinct outage combinations.

    All models must be evaluated on identical patterns and target masks before
    using paired differences. Unavailable metrics are left as None.
    """
    if not per_pattern:
        raise ValueError('No pattern results')
    keys=('mae_m','bias_pred_minus_true_m','true_tail_rate','conditional_tail_mae_m',
          'conditional_tail_signed_bias_m','tail_underprediction_fraction',
          'tail_auc','tail_average_precision','tail_recall_at_empirical_5pct_fpr')
    o={'n_patterns':len(per_pattern)}
    for k in keys:
        v=[float(x[k]) for x in per_pattern if x[k] is not None]
        o[k]=float(np.mean(v)) if v else None
        o['patterns_with_'+k]=len(v)
    return o


def pattern_mask(n_scans, n_estimators, absent):
    a=np.ones((n_scans,n_estimators),dtype=bool)
    for j in absent:
        if j<0 or j>=n_estimators:raise IndexError('Absent estimator index out of range')
        a[:,j]=False
    return a
