#%%
# =============================================================================
# Dependencies
# =============================================================================

# Get the dependencies
from re import I
import cdsapi
import datetime as dt
import os.path

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

# Make a shortcut for the CDS download client
c = cdsapi.Client()

# %%
print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' NOTIFY: Starting to retrieve '+year)

# %% Surface Solar Radiation
file=dir_data+'CORDEX-EU_'+experiment+'_ssrd_'+year+'.zip'
# Check if file exist to allow for easy redo

if os.path.isfile(file) == True:
    # Tell us the file exist
    print('NOTIFY: this file was allready done! '+file)
# if file doesn't exist, we download it
elif os.path.isfile(file) == False:
    c.retrieve(
        'projections-cordex-domains-single-levels',
        {
            'domain': 'europe',
            'experiment': experiment,
            'horizontal_resolution': '0_11_degree_x_0_11_degree',
            'temporal_resolution': '3_hours',
            'variable': 'surface_solar_radiation_downwards',
            'gcm_model': GCM_model,
            'rcm_model': RCM_model,
            'ensemble_member': ENSEMBLE_member,
            'start_year': year,
            'end_year': str(int(year)+1),
            'format': 'zip',
        },
        file)
