import pandas as pd
import ee
from apiConfig.eeAuth import credentials
import time
import logging
from IPython.display import Image

from model.eeModel import *
from dataset import *
from model.update_gspread import Gspread
from model.export_city_definition import ExportModel
from client.constants import *

# ee.Authenticate()
ee.Initialize(credentials)

BP_DATA = {
    GAIA_10m['name']: GAIA,
    GHS_BUILT_38m['name']: GHSbp38,
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

cities = {
    'Stockholm': 
        {'coords': [[18.0686, 59.3293]], 'adminLevel': 1, 'bp_density_th': 56, 'visMin':800, 'visMax': 7000},
    # 'Dubai': 
    #     {'coords': [[55.2708, 25.2048]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Guangzhou': 
    #     {'coords': [[113.2644, 23.1291]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Beijing': 
    #     {'coords': [[116.4074, 39.9042]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Mumbai': 
    #     {'coords': [[72.8217, 18.9756], [72.8423, 19.2027]], 'adminLevel': 2, 'bp_density_th': 55, 'visMin':800, 'visMax': 7000},
    # 'Nairobi': 
    #     {'coords': [[36.8219, -1.2921]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Kigali': 
    #     {'coords': [[30.0619, -1.9441]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Lagos': 
    #     {'coords': [[3.3792, 6.5244]], 'adminLevel': 1, 'bp_density_th': 50, 'visMin':800, 'visMax': 7000}, 
    # 'Mexico City': 
    #     {'coords': [[-99.1332, 19.4326]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Rio de Janeiro': 
    #     {'coords': [[-43.1729, -22.906]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'New York': 
    #     {'coords': [[-74.1572, 40.5657], [-73.9526, 40.6273], [-73.9883, 40.7377], [-73.8475, 40.8581], [-73.8003, 40.7891]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Shanghai': 
    #     {'coords': [[121.4737, 31.2304]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Detroit': 
    #     {'coords': [[-83.0458, 42.3314]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Charleston': 
    #     {'coords': [[-79.9311, 32.7765]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},         #!wsf image is all 0
    # 'Cairo': 
    #     {'coords': [[31.2604, 30.0425]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},
    # 'Dar Es Salaam': 
    #     {'coords': [[39.2618, -6.7917]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    # 'Heidelberg': 
    #     {'coords': [[8.68, 49.3895]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    # 'La Paz': 
    #     {'coords': [[-68.1449, -16.5083]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    # 'Nouakchott': 
    #     {'coords': [[-15.9677, 18.0713]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    # 'Sydney': 
    #     {'coords': [[151.2023, -33.8913]], 'adminLevel': 2, 'bp_density_th': 40, 'visMin':300, 'visMax': 1500},
    # 'Tianjin': 
    #     {'coords': [[117.3104, 39.3015]], 'adminLevel': 1, 'bp_density_th': 50, 'visMin':800, 'visMax': 7000}, 
    # 'Karachi': 
    #     {'coords': [[67.0432, 24.8866]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000},             
    # 'Islamabad': 
    #     {'coords': [[73.0556, 33.6826]], 'adminLevel': 1, 'bp_density_th': 40, 'visMin':800, 'visMax': 7000}, 

}


def main(CFG):

    popData = POP_DATA[CFG['popData']]() 
    pop4def = POP_DATA[CFG['pop4def']](cellTH=450, clusterTH=150000)

    periods = [[2000, 2015], [2005, 2010],[2010, 2015]] if CFG['pop4def'] in ['GPWv4', 'WorldPop1k'] else [ [1990,2000], [2000, 2015]] #[1975, 1990], [1990,2000],
    statsList = []
    assetConfis = []

    for name, geo in cities.items():
        print(f'========================= {name} =======================')
        bpData = BP_DATA[CFG['bp']](th=geo['bp_density_th'])
        for idx, p in enumerate(periods):

            # ====== Get SDG ======
            if CFG['computeSDG']:
                cdAsset = f"projects/gisproject-1/assets/CityDefinition_GHSpop1km/{name.replace(' ', '_')}{p[1]}"
                # cdAsset = f"projects/gisproject-1/assets/CityDefinition_{CFG['pop4def'].replace(' ', '')}/{name.replace(' ', '_')}{p[1]}"
                try:
                    cityDef = ee.FeatureCollection(cdAsset)
                    # model.cityDef[pop4def.name + str(model.endYear)] = ee.FeatureCollection(f"users/omegazhanghui/CityDefinition_GHSpop1k/{name.replace(' ', '_')}{p[1]}")
                    # model.cityDef[model.endYear] = ee.FeatureCollection(f'users/clarahuebinger/DUG/Dubai_{p[1]}')
                    mask = cityDef.getInfo()
                except Exception as e:
                    print(e)
                    raise Exception(f"City Definition not found: {cdAsset}")
                stats = computeSDG(bpData, popData, *p, cityDef).getInfo()
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
        'bp': GHS_BUILT_38m['name'],

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
