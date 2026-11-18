"""Stage8 model availability augmentation and masked multitask training utilities.

These methods operate on user-provided inputs. This module contains NO private
empirical measurements, weights, true coordinates or site identifiers.
The real-data experiments must be reproduced with separately authorized source
splits, original Stage13 normalizer, model weights and reference datasets.
"""
from itertools import combinations
import numpy as np
import torch
from torch.nn import functional as F
from .availability import rebuild_for_available

N_ESTIMATORS = 6
REFERENCE_INDEX = 5
OTHER_INDICES = tuple(range(5))


def augmentation_masks(n_scans: int, seed: int) -> np.ndarray:
    """Deterministic four versions per scan: full, 1-, 2-, and 3-outage.

    Shape: (4*n_scans, 6). Pattern draws do not depend on reference labels.
    There is always at least one full input per original scan.
    """
    if n_scans <= 0: raise ValueError("n_scans must be positive")
    rng = np.random.default_rng(seed)
    blocks = [np.ones((n_scans, 6), dtype=bool)]
    for n_missing in (1, 2, 3):
        patterns = list(combinations(range(6), n_missing))
        choices = rng.integers(len(patterns), size=n_scans)
        mask = np.ones((n_scans, 6), dtype=bool)
        for p_index, pat in enumerate(patterns):
            idx = (choices == p_index)
            mask[np.ix_(idx, np.asarray(pat))] = False
        blocks.append(mask)
    return np.concatenate(blocks)


def augment_six_estimator_scans(raw33, candidate_xy, targets, scaler, seed):
    """Create the exact Stage8 mask design for a generic development split.

    raw33 (n,6,33), candidate_xy (n,6,2), targets (n,6).
    Scaler is already fitted strictly on the development split. Missing
    geometry uses only available candidate coordinates. Training labels are
    duplicated but NOT consulted when constructing the masks/features.
    """
    x=np.asarray(raw33, dtype="float32")
    xy=np.asarray(candidate_xy, dtype="float64")
    y=np.asarray(targets, dtype="float32")
    if x.ndim != 3 or x.shape[1:] != (6,33) or xy.shape != (len(x),6,2) or y.shape!=(len(x),6):
        raise ValueError("Expected raw33 (n,6,33), candidate_xy (n,6,2), targets (n,6)")
    masks=augmentation_masks(len(x), seed)
    xs = [scaler.transform(x)]
    for idx in range(1,4):
        mode = masks[len(x)*idx:len(x)*(idx+1)]
        modified=np.full(x.shape, np.nan, dtype="float32")
        for bits in np.unique(mode, axis=0):
            which=np.all(mode==bits,axis=1)
            if which.any():
                modified[which]=rebuild_for_available(x[which],xy[which],bits)
        xs.append(scaler.transform(modified))
    return np.concatenate(xs), np.tile(y,(4,1)), masks


def masked_multitask_loss(outputs, target_errors, available):
    """Stage8 three-head loss scored only on available candidates.

    Win-target is active only if both the candidate and original WKNN are
    available. With all six available, this reduces to the original Stage13
    three-component multitask loss exactly.
    """
    error,tail_logits,win_logits=outputs
    y=target_errors
    a=available.bool()
    if y.shape!=a.shape or y.shape[1]!=6:raise ValueError("Expected (batch,6) labels and availability")
    w=a.to(error.dtype)
    denom=w.sum().clamp_min(1)
    regression=(F.smooth_l1_loss(error,y,beta=5,reduction="none")*w).sum()/denom
    severe=(F.binary_cross_entropy_with_logits(tail_logits,(y>7).float(),reduction="none")*w).sum()/denom
    win_valid=a[:,:5]&a[:,5:6]
    pairs=win_valid.to(error.dtype)
    # Multiplying by zero disables WKNN comparison when WKNN is unavailable.
    win_target=(y[:,:5]+.25<y[:,5:6]).float()
    win=(F.binary_cross_entropy_with_logits(win_logits,win_target,reduction="none")*pairs).sum()/pairs.sum().clamp_min(1)
    return .25*regression+.20*severe+.30*win


def forward_masked_jepformer(model, inputs, available):
    """Use original six slots, blocking unavailable keys and values in attention.

    Outputs for unavailable slots are NOT meaningful and must not be scored.
    Not a variable-cardinality attention architecture or integrity guarantee.
    """
    if inputs.ndim!=3 or inputs.shape[1]!=6 or available.shape!=inputs.shape[:2]:
        raise ValueError("Expected inputs (batch,6,channels), available (batch,6)")
    if not torch.all(available.sum(dim=1)>=2):
        raise ValueError("At least two candidates must be available")
    embeddings=model.proj(inputs)+model.estimator_id(torch.arange(6,device=inputs.device))[None]
    h=model.encoder(embeddings,src_key_padding_mask=~available.bool())
    return model.head(model.norm(h))
