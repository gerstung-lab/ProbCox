'''
Compute concordance index
'''

# Modules
# =======================================================================================================================

import os
import sys
import glob
import subprocess
import tqdm
import importlib
os.chdir('/nfs/research1/gerstung/sds/sds-ukb-cancer/projects/ProbCox/')

import pandas as pd
import numpy as np

from multiprocessing import Pool

import torch
from torch.distributions import constraints
from torch.utils.data import Dataset, DataLoader, Sampler

import pyro
import pyro.distributions as dist

from pyro.optim import Adam
from pyro.infer import SVI, Trace_ELBO
from pyro.infer.mcmc import MCMC, NUTS

import matplotlib.pyplot as plt

import probcox

import warnings
warnings.filterwarnings("ignore")

dtype = torch.FloatTensor

np.random.seed(87)
torch.manual_seed(34)

ROOT_DIR = '/nfs/research1/gerstung/sds/sds-ukb-cancer/'

# Concordance
# =======================================================================================================================
#train
dd = torch.load(ROOT_DIR + 'projects/ProbCox/output/prediction_train')
ci_train = pcox.metrics(surv=dd['Surv'], linpred=dd['Pred'],processes=12).concordance()

# valid
dd = torch.load(ROOT_DIR + 'projects/ProbCox/output/prediction_valid')
ci_valid = pcox.metrics(surv=dd['Surv'], linpred=dd['Pred'],processes=12).concordance()

# test
dd = torch.load(ROOT_DIR + 'projects/ProbCox/output/prediction_test')
ci_test = pcox.metrics(surv=dd['Surv'], linpred=dd['Pred'],processes=12).concordance()

torch.save({'ci_train': ci_train, 'ci_valid': ci_valid, 'ci_test': ci_test}, ROOT_DIR + 'projects/ProbCox/output/concordance')
