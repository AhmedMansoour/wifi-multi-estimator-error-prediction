"""Six-candidate Transformer structure; no empirical weights bundled."""
import torch
from torch import nn
from torch.nn import functional as F
WKNN_INDEX=5
OTHER=(0,1,2,3,4)

class PredictionHead(nn.Module):
    def __init__(self,width=64):
        super().__init__()
        self.error=nn.Linear(width,1)
        self.tail=nn.Linear(width,1)
        self.win=nn.Sequential(nn.Linear(width*2,48),nn.GELU(),nn.Linear(48,1))
        nn.init.constant_(self.error.bias,3.)
    def forward(self,h):
        ref=h[:,5:6].expand(-1,5,-1)
        return F.softplus(self.error(h)).squeeze(-1),self.tail(h).squeeze(-1),self.win(torch.cat((h[:,OTHER],ref),-1)).squeeze(-1)

class JEPFormer(nn.Module):
    def __init__(self,input_dim=66,mask_cross_token_attention=False):
        super().__init__()
        self.input_dim=input_dim
        self.mask_cross_token_attention=mask_cross_token_attention
        self.proj=nn.Linear(input_dim,64)
        self.estimator_id=nn.Embedding(6,64)
        layer=nn.TransformerEncoderLayer(64,4,128,dropout=.10,activation="gelu",batch_first=True,norm_first=True)
        self.encoder=nn.TransformerEncoder(layer,2,enable_nested_tensor=False)
        self.norm=nn.LayerNorm(64)
        self.head=PredictionHead()
    def forward(self,x):
        if x.ndim!=3 or x.shape[1:]!=(6,self.input_dim):
            raise ValueError("Expected (batch,6,input_dim)")
        h=self.proj(x)+self.estimator_id(torch.arange(6,device=x.device))[None]
        mask=None
        if self.mask_cross_token_attention:
            mask=torch.ones(6,6,device=x.device,dtype=torch.bool)
            mask.fill_diagonal_(False)
        return self.head(self.norm(self.encoder(h,mask=mask)))

def stage13_multitask_loss(out,errors):
    err,tail,win=out
    return (.25*F.smooth_l1_loss(err,errors,beta=5)
           +.20*F.binary_cross_entropy_with_logits(tail,(errors>7).float())
           +.30*F.binary_cross_entropy_with_logits(win,(errors[:,OTHER]+.25<errors[:,5:6]).float()))
