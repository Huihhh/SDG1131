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

BP_DATA = [GHS_BUILT_30m, GHS_BUILT_38m,  WSFevo_30m, WSF1519_10m, GAIA_10m] # GHS_BUILT_250m, WSF_30m
PG_DATA = [WORLD_POP_100m, GHS_POP_250m, GPWV4_30arc]
CD_DATA = [GHS_POP_1km, GPWV4_30arc, WORLD_POP_1km]


DATASET = {
    ## Builtup data
    GAIA_10m['name']: GAIA,
    GHS_BUILT_38m['name']: GHSbp38,
    GHS_BUILT_30m['name']: GHSbp30,
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



CITY_CONFIGS = {
    'Stockholm': 
        {'coords': [[18.0686, 59.3293]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[17.400493920898423,58.94749180894966],[18.757305444335923,58.94749180894966],[18.757305444335923,59.69578042028937],[17.400493920898423,59.69578042028937],[17.400493920898423,58.94749180894966]]
        },
    'Dubai': 
        {'coords': [[55.2708, 25.2048]], 'zoom': 9, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 100000,
          'bound': [[54.80330159446275,24.804296697483124],[55.67671468040025,24.804296697483124],[55.67671468040025,25.5326363418963],[54.80330159446275,25.5326363418963],[54.80330159446275,24.804296697483124]]
        },
    'Guangzhou': 
        {'coords': [[113.2644, 23.1291]], 'zoom': 9, 'adminLevel': 2,  'cellTH':600, 'clusterTH': 500000,
        'useAdmin': True
        },
    'Beijing': 
        {'coords': [[116.4074, 39.9042]], 'zoom': 9, 'adminLevel': 1,  'cellTH':800, 'clusterTH': 6000000,
          'bound': [[115.32929677308456,39.09516239807244],[117.72431630433456,39.09516239807244],[117.72431630433456,40.78807897238751],[115.32929677308456,40.78807897238751],[115.32929677308456,39.09516239807244]]
        },
    'Mumbai': 
        {'coords': [[72.8217, 18.9756], [72.8423, 19.2027]], 'zoom': 11, 'adminLevel': 2,  'cellTH':1000, 'clusterTH': 1000000,
          'bound': [[72.68642408811122,18.815319934878328],[73.39641554318935,18.815319934878328],[73.39641554318935,19.379820478734626],[72.68642408811122,19.379820478734626],[72.68642408811122,18.815319934878328]]
        },
    'Nairobi': 
        {'coords': [[36.8219, -1.2921]], 'zoom': 11, 'adminLevel': 2,  'cellTH':800, 'clusterTH': 500000,
          'bound': [[36.45729123535158,-1.526861546675646],[37.21122800292971,-1.526861546675646],[37.21122800292971,-0.9708129799204578],[36.45729123535158,-0.9708129799204578],[36.45729123535158,-1.526861546675646]]
        },
    'Kigali': 
        {'coords': [[30.0619, -1.9441]], 'zoom': 11, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 200000,
          'bound': [[29.78089458570884,-2.229897856299046],[30.460673638443215,-2.229897856299046],[30.460673638443215,-1.6973757586356715],[29.78089458570884,-1.6973757586356715],[29.78089458570884,-2.229897856299046]]
        },
    'Lagos': 
        {'coords': [[3.3792, 6.5244]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 1000000,
          'bound': [[2.7818184082031205,6.209126727788072],[4.0370063964843705,6.209126727788072],[4.0370063964843705,7.18840600868222],[2.7818184082031205,7.18840600868222], [2.7818184082031205,6.209126727788072]]
        }, 
    'Mexico City': 
        {'coords': [[-99.1332, 19.4326]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 5000000,
          'bound': [[-99.63033134765625,19.0234978035092],[-98.36690361328125,19.0234978035092],[-98.36690361328125,19.963345143184398],[-99.63033134765625,19.963345143184398],[-99.63033134765625,19.0234978035092]]
        },
    'Rio de Janeiro': 
        {'coords': [[-43.1729, -22.906]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 5000000,
          'bound': [[-44.084765234375,-23.217462625880668],[-42.4093501953125,-23.217462625880668],[-42.4093501953125,-22.125177167758494],[-44.084765234375,-22.125177167758494],[-44.084765234375,-23.217462625880668]]
        },
    'New York': 
        {'coords': [[-74.1572, 40.5657], [-73.9526, 40.6273], [-73.9883, 40.7377], [-73.8475, 40.8581], [-73.8003, 40.7891]], 'zoom': 10, 'adminLevel': 2,  'cellTH':300, 'clusterTH': 8000000,
          'bound': [[-75.61927015560583,39.533835124095305],[-71.51038343685583,39.533835124095305],[-71.51038343685583,42.02085986029484],[-75.61927015560583,42.02085986029484],[-75.61927015560583,39.533835124095305]]
        },
    'Shanghai': 
        {'coords': [[121.4737, 31.2304]], 'zoom': 9, 'adminLevel': 1,  'cellTH':940, 'clusterTH': 8000000,
          'bound': [[120.00977177734374,30.24718703499592],[122.33887333984374,30.24718703499592],[122.33887333984374,32.14536834012482],[120.00977177734374,32.14536834012482],[120.00977177734374,30.24718703499592]]
        },
    'Detroit': 
        {'coords': [[-83.0458, 42.3314]], 'zoom': 11, 'adminLevel': 2,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[-83.94232161503948,41.91887983331317],[-83.74456770878948,41.91070447694334],[-83.12384016972698,41.96382557351805],[-83.12246687871135,42.13412670806511],[-83.11046053633859,42.207032816758336],
          [-83.10428072676828,42.25126669585713],[-83.08986117110422,42.26498814863147],[-83.08711458907297,42.29293002013866],[-83.06788851485422,42.311720307658916],[-83.04866244063547,42.32238257078272],
          [-83.01913668379953,42.325936257036936],[-82.98617769942453,42.329997366963134],[-82.95459200606516,42.339641452253595],[-82.92781283126047,42.34471669259423],[-82.52315617412692,42.35832621168559],
          [-82.52040959209567,42.87574819804801],[-83.85799504131442,42.87574819804801],[-83.94232161503948,41.91887983331317]]
        },
    'Charleston': 
        {'coords': [[-79.9311, 32.7765]], 'zoom': 10, 'adminLevel': 2,  'cellTH':300, 'clusterTH': 50000,
          'bound': [[-80.41312514648438,32.541798221430774],[-79.55344497070313,32.541798221430774],[-79.55344497070313,33.19464780569893],[-80.41312514648438,33.19464780569893],[-80.41312514648438,32.541798221430774]]
        },
    'Cairo': 
        {'coords': [[31.2604, 30.0425]], 'zoom': 12, 'adminLevel': 1,  'cellTH':800, 'clusterTH': 8000000,
          'bound': [[29.525310029864478,29.195871546468858],[32.67838620173948,29.195871546468858],[32.67838620173948,31.7754066846399],[29.525310029864478,31.7754066846399],[29.525310029864478,29.195871546468858]]
        },
    'Dar Es Salaam': 
        {'coords': [[39.2618, -6.7917]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 200000,
          'bound': [[38.745442578125015,-7.173368859796176],[39.51585883789064,-7.173368859796176],[39.51585883789064,-6.512070773564517],[38.745442578125015,-6.512070773564517],[38.745442578125015,-7.173368859796176]]
        },
    'Heidelberg': 
        {'coords': [[8.68, 49.3895]], 'zoom': 11, 'adminLevel': 2,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[7.9285040009157814,49.14109958938425],[9.164465914978281,49.14109958938425],[9.164465914978281,49.95014720282214],[7.9285040009157814,49.95014720282214],[7.9285040009157814,49.14109958938425]]
        },
    'La Paz': 
        {'coords': [[-68.1449, -16.5083]], 'zoom': 11, 'adminLevel': 2,  'cellTH':300, 'clusterTH': 50000,
          'bound': [[-68.40170541992188,-16.716881035796593],[-67.91487375488282,-16.716881035796593],[-67.91487375488282,-16.350892650531843],[-68.40170541992188,-16.350892650531843],[-68.40170541992188,-16.716881035796593]]
        },
    'Nouakchott': 
        {'coords': [[-15.9677, 18.0713]], 'zoom': 11, 'adminLevel': 2,  'cellTH':300, 'clusterTH': 50000,
          'bound': [[-16.07481669921876,17.912604420359113],[-15.800158496093761,17.912604420359113],[-15.800158496093761,18.218764835347468],[-16.07481669921876,18.218764835347468],[-16.07481669921876,17.912604420359113]]
        },
    'Sydney': 
        {'coords': [[151.2023, -33.8913]], 'zoom': 9, 'adminLevel': 2,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[150.3261403320313,-34.19399082371624],[151.4467458007813,-34.19399082371624],[151.4467458007813,-33.39053750846424],[150.3261403320313,-33.39053750846424],[150.3261403320313,-34.19399082371624]]
        },
    'Tianjin': 
        {'coords': [[117.3104, 39.3015]], 'zoom': 9, 'adminLevel': 1,  'cellTH':700, 'clusterTH': 2000000,
          'bound': [[116.73361777343752,38.59447337084954],[118.03549765625002,38.59447337084954],[118.03549765625002,40.005664477974655],[116.73361777343752,40.005664477974655],[116.73361777343752,38.59447337084954]]
        }, 
    'Karachi': 
        {'coords': [[67.0432, 24.8866]], 'zoom': 9, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[66.67936480923676,24.52037238357918],[67.58299029751801,24.52037238357918],[67.58299029751801,25.183303464065972],[66.67936480923676,25.183303464065972],[66.67936480923676,24.52037238357918]]
        },             
    'Islamabad': 
        {'coords': [[73.0556, 33.6826]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 1000000,
          'bound': [[72.88848291023113,33.74916712711723],[72.73604760749676,33.671485449599835],[72.73879418952801,33.342850322770865],[73.47213159187176,33.33826123169303],[73.46938500984051,33.88722090750841]]
        }, 
    'Tehran': 
        {'coords': [[51.3801, 35.7081]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 5000000,
          'bound': [[50.53967751421384,35.20244603017056],[52.17114724077634,35.20244603017056],[52.17114724077634,36.115153277081106],[50.53967751421384,36.115153277081106],[50.53967751421384,35.20244603017056]]
        }, 
    'Gombe': 
        {'coords': [[11.17253, 10.27883]], 'zoom': 13, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 50000,
          'bound': [[11.044988160580012,10.350265802912173],[11.044988160580012,10.201964762828007],[11.296987061947199,10.201964762828007],[11.296987061947199,10.350265802912173]]
        }, 
    'Johannesburg': 
        {'coords': [[28.0411, -26.205]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 1000000,
          'bound': [[27.14518473797641,-25.44960415129584],[27.14518473797641,-27.006653366250344],[29.19688151532016,-27.006653366250344],[29.19688151532016,-25.44960415129584]]
        }, 
    'Kampala': 
        {'coords': [[32.5792, 0.3305]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[32.253742791085706,0.6127404597266303],[32.253742791085706,-0.057413866216391926],[33.00767955866383,-0.057413866216391926],[33.00767955866383,0.6127404597266303]]
        }, 
    'Buenos Aires': 
        {'coords': [[-58.4882, -34.6678]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 1000000,
          'bound': [[-59.333613876771025,-34.245727220566536],[-59.333613876771025,-35.249968877788284],[-57.614253525208525,-35.249968877788284],[-57.614253525208525,-34.245727220566536]]
        }, 
    'Quito': 
        {'coords': [[-78.4855, -0.1804]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[-78.7972069001661,0.11484139239947104],[-78.7972069001661,-0.5498229434413068],[-78.07897569899423,-0.5498229434413068],[-78.07897569899423,0.11484139239947104]]
        }, 
    'Kolkata': 
        {'coords': [[88.3654, 22.5579]], 'zoom': 9, 'adminLevel': 1,  'cellTH':1000, 'clusterTH': 5000000,
          'bound': [[87.2777878289244,23.510760508350234],[87.2777878289244,21.6187806189979],[89.6123825554869,21.6187806189979],[89.6123825554869,23.510760508350234]]
        }, 
    'Accra': 
        {'coords': [[-0.2044, 5.5955]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 500000,
          'bound': [[-0.690593725995452,6.013556412131616],[-0.690593725995452,5.316603081362905],[0.347614281817048,5.316603081362905],[0.347614281817048,6.013556412131616]]
        }, 
    'Halle': 
        {'coords': [[11.9683, 51.4866]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 100000,
          'bound': [[11.697714856441053,51.62345293570917],[11.697714856441053,51.20634655080848],[12.266257336909803,51.20634655080848],[12.266257336909803,51.62345293570917]]
        }, 
    'Abu Dhabi': 
        {'coords': [[54.3844, 24.4499]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 80000,
          'bound': [[54.03694167204494,24.698405129458216],[54.03694167204494,24.04292600581922],[55.189132834154314,24.04292600581922],[55.189132834154314,24.698405129458216]]
        }, 
    'Manama': 
        {'coords': [[50.5803, 26.2218]], 'zoom': 11, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 100000,
          'bound': [[50.371909935953155,26.327740214687832],[50.371909935953155,25.996788893665112],[50.78321059513284,25.996788893665112],[50.78321059513284,26.327740214687832]]
        }, 
    'Kitchener': 
        {'coords': [[-80.4839, 43.4522]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 100000,
          'bound': [[-80.77981238973942,43.61942392944039],[-80.77981238973942,43.281453337873046],[-80.22225623739567,43.281453337873046],[-80.22225623739567,43.61942392944039]]
        }, 
    'Batam': 
        {'coords': [[104.0504, 1.127]], 'zoom': 11, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 20000,
          'bound': [[103.82652352142473,1.2217245831903083],[103.82652352142473,0.9203402170341837],[104.18220589447161,0.9203402170341837],[104.18220589447161,1.2217245831903083]]
        }, 
    'Mogadishu': 
        {'coords': [[45.3372, 2.0583]], 'zoom': 11, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 100000,
          'bound': [[45.12024063589507,2.1756805242832535],[45.12024063589507,1.9320781519749863],[45.50682205679351,1.9320781519749863],[45.50682205679351,2.1756805242832535]]
        }, 
    'Ouagadougou': 
        {'coords': [[-1.5334, 12.3649]], 'zoom': 11, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 100000,
          'bound': [[-1.7009516013015036,12.51507726178265],[-1.7009516013015036,12.185737051039142],[-1.3301630270827536,12.185737051039142],[-1.3301630270827536,12.51507726178265]]
        }, 
    'Xiamen': 
        {'coords': [[118.1229, 24.4845]], 'zoom': 10, 'adminLevel': 1,  'cellTH':600, 'clusterTH': 80000,
          'bound': [[117.85746794065894,24.621284371917103],[117.77507047972144,24.555099908071615],[118.00715666136206,24.32255382720681],[118.28044157347144,24.33631847285569],[118.29417448362769,24.566341244652957],[118.31202726683081,24.63751295157156],[118.31614713987769,24.66497189927815],[118.33537321409644,24.674955473490975],[118.32164030394019,24.739829216119045],[118.44660978636206,24.863245274883088],[117.52305716940833,25.180541408229626],[116.85838431784583,24.697389607771427]]
        }, 
    'Yinchuan': 
        {'coords': [[106.2882, 38.4793]], 'zoom': 10, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 200000,
          'bound': [[105.88142398085938,38.75897727091424],[105.88142398085938,38.03356557918476],[106.83723452773438,38.03356557918476],[106.83723452773438,38.75897727091424]]
        }, 
    'Niamey': 
        {'coords': [[2.1238, 13.531]], 'zoom': 11, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 200000,
          'bound': [[1.9748370894080125,13.643098658917308],[1.9748370894080125,13.406767164110828],[2.29000737749395,13.406767164110828],[2.29000737749395,13.643098658917308]]
        }, 
    'Dodoma': 
        {'coords': [[35.7426, -6.1697]], 'zoom': 11, 'adminLevel': 1,  'cellTH':300, 'clusterTH': 80000,
          'bound': [[35.63959763322801,-6.060471779745126],[35.63959763322801,-6.276195424552673],[35.88953659807176,-6.276195424552673],[35.88953659807176,-6.060471779745126]]
        }, 
    'Lilongwe': 
        {'coords': [[33.7926, -13.9962]], 'zoom': 9, 'adminLevel': 1,  'cellTH':400, 'clusterTH': 100000,
          'bound': [[33.32976973259878,-13.564054261557082],[33.32976973259878,-14.432839733817472],[34.17297041619253,-14.432839733817472],[34.17297041619253,-13.564054261557082]]
        }, 
}
CITIES = CITY_CONFIGS.keys()

