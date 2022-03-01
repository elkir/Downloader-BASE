#%%
# =============================================================================
# Dependencies
# =============================================================================

# Get the dependencies
from re import I
import cdsapi
import datetime as dt
import os.path
import cordex as cx
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt

from cdo import Cdo
from pathlib import Path
#%%
# =============================================================================
# Run definitions
# =============================================================================

"""
Combo's used (only used combo's that have all scenario's available in one experiment)

EC-Earth: 
    RACMO   [r12i1p1]   (1950 -- 2100)
    RCA     [r12i1p1]   (1970 -- 2100)
    HIRHAM  [r3i1p1]    (1951 -- 2100)

HadGEM2-ES:
    RACMO   [r1i1p1]    (1951 -- 2100)
    RCA     [r1i1p1]    (1970 -- 2100)

CNRM-CERFACS-CM5:
    RACMO   [r1i1p1]    (1951 -- 2100) 

MPI-ESM-LR:
    RCA     [r1i1p1]    (1970 -- 2100)

NCC-NorESM1-M:
    REMO    [r1i1p1]    (1950 -- 2100)
    RCA     [r1i1p1]    (1970 -- 2100)

"""

GCM_model = 'cnrm_cerfacs_cm5'  # ichec_ec_earth, mohc_hadgem2_es, cnrm_cerfacs_cm5, mpi_esm_lr, ncc_noresm1_m
RCM_model = 'knmi_racmo22e' # smhi_rca4, knmi_racmo22e, dmi_hirham5, gerics_remo2015
ENSEMBLE_member = 'r1i1p1'


# define the storage location
dir_root = Path('/home/orage/Code/ai4er/phd/ph4/1_downloader_weather_data/')
dir_data = dir_root / 'data/CORDEX-EU/origin_CM_RACMO/'

# Specific sub-experiment
experiment ='historical' # 'historical' 'rcp_2_6' 'rcp_4_5' 'rcp_8_5'

# The year definitions
# - range(N_0,N_I+1)

# years = [str(i) for i in range(1950,2101)]  # full
years=[str(i) for i in range(2004,2005)]  # single year 2004

year = '2004'

# %%

ds = xr.open_dataset(dir_data+"rsds_EUR-11_CNRM-CERFACS-CNRM-CM5_historical_r1i1p1_KNMI-RACMO22E_v2_3hr_2004010100-2005010100.nc")
ds


#%% Get inforamtion about a certain domain
cx.domain_info('EUR-11')

# %% Main functions that create a dataset from grid
eur11 = cx.cordex_domain('EUR-11', dummy = "topo")


# %% Plot with cartopy
def plot(da, pole, borders=True, title=None,**kwargs):
    """Plot a domain using the right projection with cartopy."""
    plt.figure(figsize=(20,10))
    projection = ccrs.PlateCarree()
    transform = ccrs.RotatedPole(pole_latitude=pole[1], pole_longitude=pole[0])
    ax = plt.axes(projection=transform)
    
    return plot_subroutine(da,ax,transform,borders,title,**kwargs)

def plot_subroutine(da,ax,transform,borders,title,**kwargs):
    ax.gridlines(draw_labels = True, linewidth =0.5, color="gray",
                 xlocs=range(-180,180,10), ylocs=range(-90,90,5))
    da.plot(ax=ax, transform=transform, 
            x='rlon',y='rlat',**kwargs)
    ax.coastlines(resolution='50m', color='black', linewidth=1)
    if borders: ax.add_feature(cf.BORDERS)
    if title is not None:
        ax.set_title(title)
    return ax

# %%
pole= eur11.rotated_latitude_longitude.grid_north_pole_longitude, eur11.rotated_latitude_longitude.grid_north_pole_latitude
# %% Plot using the functions above
plot(eur11.topo, pole,cmap="terrain")


# %%
ds_1d = ds.isel(rlon=0,rlat=0,bnds=1)
ds_1d.rsds.isel(time=slice(None,100)).plot()

# %%
ds_1d.rsds.resample(time='1D').max().plot()

#%% 
solar_kwargs=dict(cmap='inferno',vmin=0, vmax=600)

# %%
plot(ds.isel(time=1, bnds=0).rsds,pole , **solar_kwargs)

# %%
plot(ds.isel(time=4, bnds=0).rsds,pole , **solar_kwargs)

# %%
plot(ds.isel(time=3, bnds=0).rsds,pole , **solar_kwargs)



# %%

# from matplotlib.animation import FuncAnimation
# fig = plt.figure(figsize=(20,10))

# def draw(i):
#     plot(ds.isel(time=i, bnds=0).rsds,pole, **solar_kwargs)

# anim = FuncAnimation(fig,draw,frames=8)
# plt.draw()
# plt.show()
# # %%
# anim.save("day_ssrd.mp4")
# # %%
