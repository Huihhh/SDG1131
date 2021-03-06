import pandas as pd
import ee
import os
import time
import logging

from model.eeModel import *
from dataset import *
from model.update_gspread import Gspread
from model.export_city_definition import ExportModel
from client.constants import *

""" Google Earth Engine Service Account Auth """
PRIVATE_KEY = os.environ['PRIVATE_KEY']
SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT')
credentials = ee.ServiceAccountCredentials(SERVICE_ACCOUNT, key_data=PRIVATE_KEY)


# ee.Authenticate()
ee.Initialize(credentials)


BP_DATA = {
    GAIA_10m['name']: GAIA,
    GHS_BUILT_38m['name']: GHSbp38,
    GHS_BUILT_30m['name']: GHSbp30,
    GHS_BUILT_250m['name']: GHSbp250,
    WSFevo_30m['name']: WSF_evolution,
    GHS_BUILT_S2_10m['name']: GHS_S2}
    
POP_DATA = {
    GHS_POP_1km['name']: GHSpop1k,
    GPWV4_30arc['name']: GPWv4,
    GHS_POP_250m['name']: GHSpop250,
    WORLD_POP_1km['name']: WorldPop1k,
    WORLD_POP_100m['name']: WorldPop100,
    SCB_POP['name']: SCBpop
}
add_cities = {
    'Kampala': 
        {'coords': [[32.5785, 0.3151]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Buenos Aires': 
        {'coords': [[-58.399, -34.5978]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Quito': 
        {'coords': [[-78.48, -0.1838]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Kolkata': 
        {'coords': [[88.3599, 22.5953]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Accra': 
        {'coords': [[-0.2065, 5.5827]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Halle': 
        {'coords': [[11.9676, 51.4858]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Abu Dhabi': 
        {'coords': [[54.3705, 24.4583]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Manama': 
        {'coords': [[50.58419, 26.22262]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Kitchener-Cambridge-Waterloo': 
        {'coords': [[-80.4857, 43.4427]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Batam': 
        {'coords': [[104.0395, 1.1183]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Mogadishu': 
        {'coords': [[45.3242, 2.0414]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Ouagadougou': 
        {'coords': [[-1.5217, 12.3538]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Xiamen': 
        {'coords': [[118.1305, 24.4874]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Yinchuan': 
        {'coords': [[106.2275, 38.4676]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Niamey': 
        {'coords': [[2.1232, 13.5168]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Dodoma': 
        {'coords': [[35.7471, -6.1753]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Lilongwe': 
        {'coords': [[33.7665, -13.9639]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
}

cities = {
    'Stockholm': 
        {'coords': [[18.0686, 59.3293]], 'adminLevel': 1, 'bp_density_th': 56, 'cellTH':300, 'clusterTH': 500000},
    'Dubai': 
        {'coords': [[55.2708, 25.2048]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Guangzhou': 
        {'coords': [[113.2644, 23.1291]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Beijing': 
        {'coords': [[116.4074, 39.9042]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000000},
    'Mumbai': 
        {'coords': [[72.8217, 18.9756], [72.8423, 19.2027]], 'adminLevel': 2, 'bp_density_th': 55, 'cellTH':300, 'clusterTH': 5000},
    'Nairobi': 
        {'coords': [[36.8219, -1.2921]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Kigali': 
        {'coords': [[30.0619, -1.9441]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':800, 'clusterTH': 100000}, 
    'Lagos': 
        {'coords': [[3.3792, 6.5244]], 'adminLevel': 1, 'bp_density_th': 50, 'cellTH':800, 'clusterTH': 100000}, #10000000
    'Mexico City': 
        {'coords': [[-99.1332, 19.4326]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':800, 'clusterTH': 7000},
    'Rio de Janeiro': 
        {'coords': [[-43.1729, -22.906]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':800, 'clusterTH': 1000000},
    'New York': 
        {'coords': [[-74.1572, 40.5657], [-73.9526, 40.6273], [-73.9883, 40.7377], [-73.8475, 40.8581], [-73.8003, 40.7891]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Shanghai': 
        {'coords': [[121.4737, 31.2304]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Detroit': 
        {'coords': [[-83.0458, 42.3314]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Charleston': 
        {'coords': [[-79.9311, 32.7765]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},         #!wsf image is all 0
    'Cairo': 
        {'coords': [[31.2604, 30.0425]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 1000000},
    'Dar Es Salaam': 
        {'coords': [[39.2618, -6.7917]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 1500},
    'Heidelberg': 
        {'coords': [[8.68, 49.3895]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'La Paz': 
        {'coords': [[-68.1449, -16.5083]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Nouakchott': 
        {'coords': [[-15.9677, 18.0713]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Sydney': 
        {'coords': [[151.2023, -33.8913]], 'adminLevel': 2, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},
    'Tianjin': 
        {'coords': [[117.3104, 39.3015]], 'adminLevel': 1, 'bp_density_th': 50, 'cellTH':300, 'clusterTH': 100000}, 
    'Karachi': 
        {'coords': [[67.0432, 24.8866]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000},             
    'Islamabad': 
        {'coords': [[73.0556, 33.6826]], 'adminLevel': 1, 'bp_density_th': 40, 'cellTH':300, 'clusterTH': 5000}, 

}


def main(CFG):

    popData = POP_DATA[CFG['popData']]() 
    pop4def = POP_DATA[CFG['pop4def']](cellTH=450, clusterTH=150000)

    periods = [[2000, 2015], [2005, 2010],[2010, 2015]] if CFG['pop4def'] in ['GPWv4', 'WorldPop1k'] else [ [1990,2000], [2000, 2015]] #[1975, 1990], [1990,2000],
    statsList = []
    assetConfis = []

    for name, geo in add_cities.items():
        print(f'========================= {name} =======================')
        bpData = BP_DATA[CFG['bp']](th=geo['bp_density_th'])
        for idx, p in enumerate(periods):

            # ====== Get SDG ======
            if CFG['computeSDG']:
                # cdAsset = f"projects/gisproject-1/assets/CityDefinition_GHSpop1km/{name.replace(' ', '_')}{p[1]}"
                # # cdAsset = f"projects/gisproject-1/assets/CityDefinition_{CFG['pop4def'].replace(' ', '')}/{name.replace(' ', '_')}{p[1]}"
                # try:
                #     cityDef = ee.FeatureCollection(cdAsset)
                #     # model.cityDef[pop4def.name + str(model.endYear)] = ee.FeatureCollection(f"users/omegazhanghui/CityDefinition_GHSpop1k/{name.replace(' ', '_')}{p[1]}")
                #     # model.cityDef[model.endYear] = ee.FeatureCollection(f'users/clarahuebinger/DUG/Dubai_{p[1]}')
                #     mask = cityDef.getInfo()
                # except Exception as e:
                #     print(e)
                #     raise Exception(f"City Definition not found: {cdAsset}")
                city, cityCoords, cityBounds = update_city(name, geo, True)
                cityDef = define_city(pop4def, p[1], cityCoords, city, useAdmin=True, cellTH=geo['cellTH'], clusterTH=geo['clusterTH'])
                cityDefT1 = define_city(pop4def, p[0], cityCoords, city, useAdmin=True, cellTH=geo['cellTH'], clusterTH=geo['clusterTH'])
                stats = computeSDG(bpData, popData, *p, cityDef, cityDefT1).getInfo()
                statsList.append(['EE App', *p, name, 0, pop4def.name, popData.name, bpData.name] + stats)

            # ====== Get city definitions ======
            if CFG['exportDef']:
                def2 = define_city(p[-1])
                feature = def2[-2]['eeObject']
                assetConfis.append({'feature': feature, 'name': name, 'year': p[-1]})

    if CFG['computeSDG']:
        df = pd.DataFrame(statsList, columns=COLUMNS)
        print(df)
        df.to_csv('stats.csv')
        # gspread = Gspread(sheet_id='1AmMWSf3tcgVofAGqH0H0jJVWLSnnX2A60RFzvJlYXgU', sheet_name='SDG11.3.1_Calculations')
        # gspread.update_gspread(df)

    if CFG['exportDef']:
        exportModel = ExportModel(asset_base=f"projects/gisproject-1/assets/CityDefinition_{CFG['pop4def']}")
        exportModel.run_export(assetConfis)

if __name__ == '__main__':
    CFG = {
        'popData': GHS_POP_250m['name'],
        'pop4def': GHS_POP_1km['name'],
        'bp': GHS_BUILT_30m['name'],

        'computeSDG': True,
        'exportDef': False,
    }
    main(CFG)
    # compareBp = False
    # if compareBp:
    #     for bp in [GHS_BUILT_38m['name'], GAIA_10m['name'], WSFevo_30m['name']]: #GHS_BUILT_38m['name'], GAIA_10m['name'],
    #         CFG['bp'] = bp
    #         main(CFG)
    # else:
    #     for pop in [WORLD_POP_100m['name'], GPWV4_30arc['name']]: #GHS_POP_250m['name']
    #         CFG['popData'] = pop
    #         main(CFG) 
