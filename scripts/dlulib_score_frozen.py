#!/usr/bin/env python3
"""External evaluation. Load sealed test GT *after* verifying immutable forecasts.

Report aggregate-only CSV/JSON. No private RP positions/scan-level arrays are saved.
"""
import argparse,csv,hashlib,json
from pathlib import Path
import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score,average_precision_score

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def metrics(p,y):
    d=p-y;ae=np.abs(d);high=y>=10
    r={'n':int(y.size),'forecast_mae_m':float(np.mean(ae)),
       'forecast_rmse_m':float(np.sqrt(np.mean(d*d))),
       'forecast_bias_m':float(np.mean(d)),
       'realized_position_error_mean_m':float(np.mean(y)),
       'spearman_forecast_actual':float(spearmanr(p,y).statistic),
       'severe_n':int(high.sum()),'severe_share':float(high.mean())}
    if high.any():
        r.update({'severe_forecast_mae_m':float(np.mean(ae[high])),
                  'severe_underpredict_fraction':float(np.mean(d[high]<0)),
                  'mean_severe_true_error_m':float(np.mean(y[high]))})
    if high.any() and (~high).any():
        r.update({'severe_auroc':float(roc_auc_score(high,p)),
                  'severe_average_precision':float(average_precision_score(high,p))})
    return r

def write_csv(path,rows):
    cols=sorted(set().union(*(r.keys() for r in rows)))
    with path.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)

def main():
    pa=argparse.ArgumentParser();pa.add_argument('--workspace',required=True,type=Path)
    a=pa.parse_args();r=a.workspace;dirp=r/'predictions_frozen';seal=r/'sealed_labels'
    frozen=json.loads((dirp/'PREDICTIONS_FROZEN_BEFORE_GT.json').read_text())
    if frozen['original_GT_accessed'] is not False or frozen['source_error_models_retrained_on_DLULIB'] is not False:
        raise RuntimeError('Invalid freeze manifest flags')
    if len(frozen['files'])!=3:raise ValueError('Expected all three floors')
    sealed_audit=json.loads((r/'inference_only/INFERENCE_AND_SEALED_GT_HASHES.json').read_text())
    if len(sealed_audit)!=3:raise ValueError('Expected sealed-input hash manifest for three floors')
    for rec in sealed_audit:
        if sha(seal/f"floor{rec['floor']}_SEALED_GT.npz")!=rec['sealed_GT_SHA256']:
            raise RuntimeError('Sealed ground-truth file changed after intake')
    for record in frozen['files']:
        floor=record['floor'];p=dirp/f'floor{floor}_FROZEN_PREDICTIONS_NO_GT.npz'
        if sha(p)!=record['predictions_sha256'] or sha(r/f'inference_only/floor{floor}_INFERENCE_ONLY.npz')!=record['inference_only_sha256']:
            raise RuntimeError('Prediction/input hash changed before scoring')
    print('PREDICTIONS VERIFIED BEFORE OPENING SEALED GT')
    allp=[];floor_rows=[];method_rows=[];clusters=[]
    method_names=('CatBoost','Extra Trees','Gradient Boosting','KNN','Random Forest','WKNN')
    for floor in (1,2,3):
        with np.load(dirp/f'floor{floor}_FROZEN_PREDICTIONS_NO_GT.npz',allow_pickle=False) as z:
            x=z['candidate_xy'];cp=z['predicted_catboost'];jp=z['predicted_jepformer'];sid=z['scan_id']
        with np.load(seal/f'floor{floor}_SEALED_GT.npz',allow_pickle=False) as z:
            if not np.array_equal(z['scan_id'],sid) or not np.all(z['floor_id']==floor):
                raise ValueError('GT alignment / floor error')
            gt=z['xy'];rp=z['rp_id']
        e=np.linalg.norm(x-gt[:,None,:],axis=-1)
        if e.shape!=(len(gt),6) or jp.shape!=(3,len(gt),6):raise ValueError('Shape mismatch')
        allp.append((e,cp,jp))
        for label,pred in [('CatBoost',cp)]+[(f'JEPFormer_seed{s}',jp[k]) for k,s in enumerate((11,21,31))]:
            floor_rows.append({'floor':floor,'learner':label,**metrics(pred.ravel(),e.ravel())})
            for idx,name in enumerate(method_names):
                method_rows.append({'floor':floor,'estimator':name,'learner':label,**metrics(pred[:,idx],e[:,idx])})
        for rpid in np.unique(rp):
            mask=rp==rpid
            clusters.append(float(np.abs(jp[:,mask]-e[None,mask]).mean()-np.abs(cp[mask]-e[mask]).mean()))
    y=np.concatenate([d[0] for d in allp]);c=np.concatenate([d[1] for d in allp]);j=np.concatenate([d[2] for d in allp],axis=1)
    per_seed=[{'learner':'JEPFormer','seed':seed,**metrics(j[k].ravel(),y.ravel())} for k,seed in enumerate((11,21,31))]
    per_seed.insert(0,{'learner':'CatBoost','seed':'fixed2026',**metrics(c.ravel(),y.ravel())})
    est=np.array(clusters);rng=np.random.default_rng(241119)
    boot=est[rng.integers(0,len(est),size=(4000,len(est)))].mean(axis=1)
    stats={'scope':'DLULIB one building, three floors, repeat collection same physical training RP XY',
           'n_scans':int(len(y)),'n_candidate_targets':int(y.size),'n_RPs':len(est),
           'CatBoost':per_seed[0],
           'JEPFormer_3seed_mean':{k:float(np.mean([s[k] for s in per_seed[1:]])) if k not in ('n','severe_n','seed','learner') else per_seed[1][k] for k in per_seed[1] if k!='learner'},
           'JEP_minus_Cat_MAE_diff_m':float(est.mean()),
           'RP_bootstrap95_descriptive':list(np.quantile(boot,[.025,.975])),
           'prospective_first_use':True,'subsequent_tuning_on_this_dataset_prohibited':True}
    dest=r/'results_aggregate_only';dest.mkdir(exist_ok=True)
    write_csv(dest/'by_floor.csv',floor_rows);write_csv(dest/'by_estimator_and_floor.csv',method_rows)
    write_csv(dest/'pooled_seeds.csv',per_seed)
    (dest/'summary.json').write_text(json.dumps(stats,indent=2))
    print('External aggregate-only scoring completed: scans',len(y),'MAE',stats['JEPFormer_3seed_mean']['forecast_mae_m'],stats['CatBoost']['forecast_mae_m'])
if __name__=='__main__':main()
