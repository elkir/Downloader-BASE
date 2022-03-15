#%%
# =============================================================================
# Dependencies
# =============================================================================

# Get the dependencies
from distutils.command.config import config
from fileinput import filename
from re import I
import cdsapi
import datetime as dt
import os.path
import cordex as cx
from fontTools import configLogger
import xarray as xr
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import seaborn as se

from cdo import Cdo
from pathlib import Path


# %%

# define the storage location
dir_root = Path('/home/orage/Code/ai4er/phd/ph4/1_downloader_weather_data/')
dir_data = dir_root / 'data/CORDEX-EU/origin_CM_RACMO/'

#TODO: open files on the go 

GCM_model = 'cnrm_cerfacs_cm5'  # ichec_ec_earth, mohc_hadgem2_es, cnrm_cerfacs_cm5, mpi_esm_lr, ncc_noresm1_m
RCM_model = 'knmi_racmo22e' # smhi_rca4, knmi_racmo22e, dmi_hirham5, gerics_remo2015
ENSEMBLE_member = 'r1i1p1'

experiment ='historical' # 'historical' 'rcp_2_6' 'rcp_4_5' 'rcp_8_5'

# The year definitions
# - range(N_0,N_I+1)

# years = [str(i) for i in range(1950,2101)]  # full
years=[str(i) for i in range(2004,2005)]  # single year 2004


# %%
# filename = "sfcWind_EUR-11_CNRM-CERFACS-CNRM-CM5_rcp45_r1i1p1_KNMI-RACMO22E_v2_3hr_2056010100-2056123121.nc"

# ds = xr.open_dataset(dir_data/filename)
# ds
# %%
filenames = [
    "sfcWind_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_3hr_1956010100-1956123121.nc",
    "sfcWind_EUR-11_CNRM-CERFACS-CNRM-CM5_rcp45_r1i1p1_KNMI-RACMO22E_v2_3hr_2056010100-2056123121.nc"
]
dsets = [xr.open_dataset(dir_data/filename) for filename in filenames]

# %%

spatial_means = [
    dset.sfcWind.mean(dim=('rlat','rlon'))
    for dset in dsets]
#%%
merged = xr.merge([
        dset
        .rename(f"y{dset.time.dt.year.min().item()}")
        .rolling(time=8*3).mean()
        .groupby("time.dayofyear").mean()
        for dset in spatial_means])
# %%
plt.figure()
merged.y1956.plot()
merged.y2056.plot()
plt.show()
# %%
plt.figure()
merged.y1956.plot.hist()
merged.y2056.plot.hist()
plt.show()