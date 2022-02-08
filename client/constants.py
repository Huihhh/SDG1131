from dataset import *
# bp data
GAIA_10m = {
    'name': 'GAIA 30m', 
    'url': 'https://ghsl.jrc.ec.europa.eu/download.php?ds=bu', 
    'info': 'Coverage: global, Available years:1985-2018 yearly'
}
GHS_BUILT_38m = {
    'name': 'GHS-Built 38m', 
    'url': 'https://ghsl.jrc.ec.europa.eu/download.php?ds=bu', 
    'info': 'Coverage: global, Available years: 1975, 1990, 2000, 2015'
}

GHS_BUILT_30m = {
    'name': 'GHS-Built 30m', 
    'url': 'https://ghsl.jrc.ec.europa.eu/download.php?ds=bu', 
    'info': 'Coverage: global, Available years: 1975, 1990, 2000, 2015'
}

GHS_BUILT_250m = {
    'name': 'GHS-Built 250m', 
    'url': 'https://ghsl.jrc.ec.europa.eu/download.php?ds=bu', 
    'info': 'Coverage: source global, 21 cities currently, Available years: 1975, 1990, 2000, 2015'
} #TODO: coverage to be double checked

WSFevo_30m = {
    'name': 'WSF evolution 30m', 
    'url': 'https://www.esa.int/Applications/Observing_the_Earth/Mapping_our_human_footprint_from_space', 
    'info': 'Coverage: source global, 21 cities currently, Available years: 1985-2015 yearly'
}

WSF1519_10m = {
    'name': 'WSF2015 10m & WSF2019 10m',
    'url': 'https://developers.google.com/earth-engine/datasets/catalog/DLR_WSF_WSF2015_v1',
    'info': 'WSF 2015: global coverage, WSF 2019: for cities in the list except for Rio de Janeiro. Visit the link of WSF evolution 30m for more info about WSF 2019.'
}

GHS_BUILT_S2_10m = {
    'name': 'GHS-Built-S2 10m', 
    'url': 'https://ghsl.jrc.ec.europa.eu/download.php?ds=pop', 
    'info': 'Coverage: global, Available years: 2018'
}

# pop data
GHS_POP_1km = {
    'name': 'GHS-Pop 1km', 
    'url': 'https://ghsl.jrc.ec.europa.eu/download.php?ds=pop', 
    'info': 'Coverage: global, Available years: 1975, 1990, 2000, 2015'
}
GPWV4_30arc = {
    'name': 'GPWv4 30 arc-second', 
    'url': 'https://developers.google.com/earth-engine/datasets/catalog/CIESIN_GPWv411_GPW_Population_Count', 
    'info': 'Coverage: global, Available years: 2000, 2005, 2010, 2015, 2020'
}
GHS_POP_250m = {
    'name': 'GHS-Pop 250m', 
    'url': 'https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2016_POP_GPW_GLOBE_V1', 
    'info': 'Coverage: global, Available years: 1975, 1990, 2000, 2015'
}
WORLD_POP_100m = {
    'name': 'WorldPop 100m', 
    'url': 'https://www.worldpop.org/geodata/listing?id=69', 
    'info': 'Coverage: source global, 21 cities currently, Available years: 2000, 2015, source 2000-2020 yearly'
}

WORLD_POP_1km = {
    'name': 'WorldPop 1km', 
    'url': 'https://www.worldpop.org/geodata/listing?id=75', 
    'info': 'Coverage: source global 2000-2020 yearl, China currently for 2000, 2005, 2010, 2015, 2018,  '
}

SCB_POP = {
    'name': 'SCB-Pop',
    'url': '',
    'info': ''
}

BP_DATA = [GHS_BUILT_38m,  WSFevo_30m, WSF1519_10m, GAIA_10m] # GHS_BUILT_250m, WSF_30m
PG_DATA = [WORLD_POP_100m, GHS_POP_250m, GPWV4_30arc]
CD_DATA = [GHS_POP_1km, GPWV4_30arc, WORLD_POP_1km]


DATASET = {
    ## Builtup data
    GAIA_10m['name']: GAIA,
    GHS_BUILT_38m['name']: GHSbp38,
    # GHS_BUILT_250m['name']: GHSbp250,
    WSFevo_30m['name']: WSF_evolution,
    WSF1519_10m['name']: WSF1519,
    GHS_BUILT_S2_10m['name']: GHS_S2,
    ## Pop for city definition
    GHS_POP_1km['name']: GHSpop1k,
    GPWV4_30arc['name']: GPWv4,
    ## Pop for pop growth
    GHS_POP_250m['name']: GHSpop250,
    WORLD_POP_100m['name']: WorldPop100,
    WORLD_POP_1km['name']: WorldPop1k,

}

COMPARE = [  
    {
        'label': 'Compare Population Growth data', 
        'colName': 'Population', 
        'value': PG_DATA, 
        'xtitle': '<br>'.join(['City', 'City Definition: GHS-Pop 1km', 'Land Consumption: GHS-built 38m']),
        'radioItems': {'City Definition': CD_DATA, 'Land Consumption': BP_DATA}
    },
    {
        'label': 'Compare Builtup data', 
        'colName': 'Built-Up', 
        'value': BP_DATA, 
        'xtitle': '<br>'.join(['Time Intervals (Year)', 'City Definition: GHS-Pop 1km', 'Population Growth: GHS-Pop 250m']),
        'radioItems': {'City Definition': CD_DATA, 'Population Growth': PG_DATA}
    },
    
    # {'label': 'Compare City Definition data', 'colName': 'City Definition',  'value': CD_DATA, 'radioItems': {'Land Consumption': BP_DATA, 'Population Growth': PG_DATA}},
    {
        'label': 'Compare Tools', 
        'colName': 'Tool', 
        'value': ['QGIS', 'EE App'], 
        'xtitle': '<br>'.join(['Time Intervals (Year)', 'City Definition: GHS-Pop 1km', 'Population Growth: GHS-Pop 250m', 'Land Consumption: GHS-built 38m']),
        'radioItems': {'City Definition': CD_DATA, 'Population Growth': PG_DATA, 'Land Consumption': BP_DATA}
    },
]

ADMIN_LEVEL = [
  {'label': 'Province/County/State level', 'value': '1'}, 
  {'label': 'City level', 'value': '2'}
]

COLUMNS = ['Tool', 'T1', 'T2', 'AOI', 'FAO Level', 'City Definition', 'Population', 'Built-Up', 'SDG 11.3.1', 'Built/Capita - T1', 'Built/Capita - T2', 'Delta Built Up', 'SUM BU T1', 'SUM BU T2', 'pop - T1', 'pop - T2', 'landComRate', 'popGrowthRate']
CITIES = ['Stockholm', 'Dubai', 'Guangzhou', 'Beijing', 'Mumbai', 'Nairobi', 'Kigali', 'Lagos', 'Mexico City', 'Rio de Janeiro', 'New York', 'Shanghai', 'Detroit', 'Charleston', 'Cairo', 'Dar Es Salaam', 'Heidelberg', 'La Paz', 'Nouakchott', 'Sydney', 'Tianjin', 'Karachi', 'Islamabad']


CITY_CONFIGS = {
    'Stockholm': 
        {'coords': [[18.0686, 59.3293]], 'adminLevel': 1, 'bp_density_th': 56, 'visMin':800, 'visMax': 7000},
    'Dubai': 
        {'coords': [[55.2708, 25.2048]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Guangzhou': 
        {'coords': [[113.2644, 23.1291]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Beijing': 
        {'coords': [[116.4074, 39.9042]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Mumbai': 
        {'coords': [[72.8217, 18.9756], [72.8423, 19.2027]], 'adminLevel': 2, 'bp_density_th': 55, 'visMin':800, 'visMax': 7000},
    'Nairobi': 
        {'coords': [[36.8219, -1.2921]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Kigali': 
        {'coords': [[30.0619, -1.9441]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Lagos': 
        {'coords': [[3.3792, 6.5244]], 'adminLevel': 1, 'bp_density_th': 50, 'visMin':800, 'visMax': 7000}, 
    'Mexico City': 
        {'coords': [[-99.1332, 19.4326]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Rio de Janeiro': 
        {'coords': [[-43.1729, -22.906]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'New York': 
        {'coords': [[-74.1572, 40.5657], [-73.9526, 40.6273], [-73.9883, 40.7377], [-73.8475, 40.8581], [-73.8003, 40.7891]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Shanghai': 
        {'coords': [[121.4737, 31.2304]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Detroit': 
        {'coords': [[-83.0458, 42.3314]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Charleston': 
        {'coords': [[-79.9311, 32.7765]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},         #!empty geometry (no city definition)
    'Cairo': 
        {'coords': [[31.2604, 30.0425]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    'Dar Es Salaam': 
        {'coords': [[39.2618, -6.7917]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    'Heidelberg': 
        {'coords': [[8.68, 49.3895]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    'La Paz': 
        {'coords': [[-68.1449, -16.5083]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    'Nouakchott': 
        {'coords': [[-15.9677, 18.0713]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    'Sydney': 
        {'coords': [[151.2023, -33.8913]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},

     # currently not available for WSF   
    'Tianjin': 
        {'coords': [[117.3104, 39.3015]], 'adminLevel': 1, 'bp_density_th': 50, 'visMin':800, 'visMax': 7000}, 
    'Karachi': 
        {'coords': [[67.0432, 24.8866]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},             
    'Islamabad': 
        {'coords': [[73.0556, 33.6826]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000}, 

}


