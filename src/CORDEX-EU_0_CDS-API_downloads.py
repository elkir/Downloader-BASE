# -*- coding: utf-8 -*-
"""
Spyder Editor

Created on Tue 05 Jan 2021 17:34

@author: Laurens Stoop - l.p.stoop@uu.nl
"""

# to unpack all files after download use: for z in ./origin/*.zip; do unzip "$z" -d ./unpack/; done
    


#%%
# =============================================================================
# Dependencies
# =============================================================================

# Get the dependencies
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
# file_path = '/media/DataGate1/CORDEX-EU/origin_CM_RACMO/'
file_path = '/home/orage/Code/ai4er/phd/ph4/1_Downloader-BASE/data/CORDEX-EU/origin_CM_RACMO/'

# Specific sub-experiment
experiment ='historical' # 'historical' 'rcp_2_6' 'rcp_4_5' 'rcp_8_5'

# The year definitions
# - range(N_0,N_I+1)

# years = [str(i) for i in range(1950,2101)]  # full
years=[str(i) for i in range(2004,2005)]  # single year 2004
"""
# years = [   
            # '1950',
            # '1951', '1952', '1953',
            # '1954', '1955', '1956',
            # '1957', '1958', '1959',
            # '1960', '1961', '1962',
            # '1963', '1964', '1965',
            # '1966', '1967', '1968',
            # '1969', 
            # '1970', '1971',
            # '1972', '1973', '1974',
            # '1975', '1976', '1977',
            # '1978', '1979', '1980',
            # '1981', '1982', '1983',
            # '1984', '1985', '1986',
            # '1987', '1988', '1989',
            # '1990', '1991', '1992',
            # '1993', '1994', '1995',
            # '1996', '1997', '1998',
            # '1999', '2000', '2001',
            # '2002', '2003', '2004',
            # '2005'
            # '2006', '2007', '2008',
            # '2009', '2010', '2011',
            # '2012', '2013', '2014',
            # '2015', '2016', '2017',
            # '2018', '2019', '2020',
            # '2021', '2022', '2023',
            # '2024', '2025', '2026',
            # '2027', '2028', '2029',
            # '2030', '2031', '2032',
            # '2033', '2034', '2035',
            # '2036', '2037', '2038',
            # '2039', '2040', '2041',
            # '2042', '2043', '2044',
            # '2045', '2046', '2047',
            # '2048', '2049', '2050',
            # '2051', '2052', '2053',
            # '2054', '2055', '2056',
            # '2057', '2058', '2059',
            # '2060', '2061', '2062',
            # '2063', '2064', '2065',
            # '2066', '2067', '2068',
            # '2069', '2070', '2071',
            # '2072', '2073', '2074',
            # '2075', '2076', '2077',
            # '2078', '2079', '2080',
            # '2081', '2082', '2083',
            # '2084', '2085', '2086',
            # '2087', '2088', '2089',
            # '2090', '2091', '2092',
            # '2093', '2094', '2095',
            # '2096', '2097', '2098',
            # '2099', '2100'
            # ] 
"""




#%%
# =============================================================================
# Download loop
# =============================================================================

# Make a shortcut for the CDS download client
c = cdsapi.Client()

# Run over the years
for year in years:

    # Let's notify our terminal where we are!
    print(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')+' NOTIFY: Starting to retrieve '+year)
    
    
    
    # Retrieve SSRD
    file=file_path+'CORDEX-EU_'+experiment+'_ssrd_'+year+'.zip'
    
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

    # Retrieve temperature
    file=file_path+'CORDEX-EU_'+experiment+'_t2m_'+year+'.zip'
    
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
                'variable': '2m_air_temperature',
                'gcm_model': GCM_model,
                'rcm_model': RCM_model,
                'ensemble_member': ENSEMBLE_member,
                'start_year': year,
                'end_year': year,
                'format': 'zip',
            },
            file)
    
    # Retrieve windspeed
    file=file_path+'CORDEX-EU_'+experiment+'_wspd_'+year+'.zip'
    
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
                'variable': '10m_wind_speed',
                'gcm_model': GCM_model,
                'rcm_model': RCM_model,
                'ensemble_member': ENSEMBLE_member,
                'start_year': year,
                'end_year': year,
                'format': 'zip',
            },
            file)
# %%
