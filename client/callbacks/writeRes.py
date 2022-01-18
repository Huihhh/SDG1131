from client.user import User
from dash.dependencies import Input, Output, State
import pandas as pd
from dash import dcc, callback_context
from dash.exceptions import PreventUpdate
from flask_login import current_user

from ..app import app
from ..constants import CITY_CONFIGS, COLUMNS, DATASET
from model.eeModel import *
from model.export_city_definition import ExportModel
from model.update_gspread import Gspread

gspread = Gspread(sheet_name='City_Definition_SDG11.3.1_Calculations') #TODO: SQL/firebase

# ================================= Update SDG results =============================
@app.callback(
    Output('sdg-res', 'children'),
    Output('result-df', 'data'),
    Input('compute-sdg', 'n_clicks'),
    State('start-year-select', 'value'),
    State('year-dropdown-select', 'value'),
    State("adminlevel-radioItem", 'value'),
    State("map-center", 'data'),
    State('built-radioItem', 'value'),
    State('pop-radioItem', 'value'),
    State('pop4def-radioItem', 'value'),
    State('cityDef-obj', 'data'),
    prevent_initial_call=True, 
)
def update_sdg_results(n_click, startYear, endYear, adminLevel, ROIdata, bpName, popName, pop4defName, cityDefs):
    bpData = DATASET[bpName]()
    popData = DATASET[popName]()
    cityDef = cityDefs[pop4defName+str(endYear)]#TODO add error message
    res = computeSDG(bpData, popData, startYear, endYear, cityDef).getInfo()
    resList = dcc.Markdown(f'''
    * **SDG 11.3.1**: {res[0]}
    * **LCPCStartYear**: {res[1]}
    * **LCPCEndYear**: {res[2]}
    * **TotalChangeInBuiltUp**: {res[3]}
    * **bpStartYear**: {res[4]}
    * **bpEndYear**: {res[5]}
    * **popStartYear**: {res[6]}
    * **popEndYear**: {res[7]}
    * **landComRate**: {res[8]}
    * **popGrowthRate**: {res[9]}
    ''')

    return resList, res

@app.callback(
    Output('alert-result-status', 'message'),
    Input('result-df', 'data'),
    State('start-year-select', 'value'),
    State('year-dropdown-select', 'value'),
    State("adminlevel-radioItem", 'value'),
    State("map-center", 'data'),
    State('built-radioItem', 'value'),
    State('pop-radioItem', 'value'),
    State('pop4def-radioItem', 'value'),
)
def update_gspread(res, startYear, endYear, adminLevel, ROIdata, bpName, popName, pop4defName):
    if res is None:
        raise PreventUpdate
    adminLevel = adminLevel if ROIdata['useAdmin'] else 0
    newDf = pd.DataFrame([['EE App', startYear, endYear, ROIdata['adminName'], adminLevel, pop4defName, popName, bpName] + res], columns=COLUMNS)
    if current_user.is_authenticated:
        doc_name = ''.join(['EE App', str(startYear), str(endYear), ROIdata['adminName'].split(' ')[0], str(adminLevel), pop4defName, popName, bpName])
        User.add_record(current_user.id, doc_name, newDf.to_dict('records')[0])
    # gspread.update_gspread(newDf)
    message = 'Sheet updated!'
    return message



@app.callback(
    [Output('alert-export-status', 'open'),
    Output('alert-export-status', 'message'),
    Output('download-city-definition', 'data')
    ],
    Input('export-city-definition', 'n_clicks'),
    State('export-option', 'value'),
    State('year-dropdown-select', 'value'),
    State("map-center", 'data'),
    State('pop4def-radioItem', 'value'),
    State('cell-TH-state', 'value'),
    State('cluster-TH-state', 'value'),   
    State('cityDef-obj', 'data'),
    prevent_initial_call=True,
)
def export_city_definition(n_click, exportOpt, year, ROIdata, pop4def, cellTH, clusterTH, cityDef):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    export = True if 'export-city-definition' in changed_id else False # if export button is most recently clicked
    if export:
        exportModel = ExportModel(asset_base=f"projects/gisproject-1/assets/CityDefinition_{pop4def.replace(' ', '')}")
        exportMethod = exportModel.export_asset if exportOpt == 'projAsset' else exportModel.download_geojson      
        res = exportMethod([{'feature': cityDef[pop4def+str(year)], 'name': ROIdata['adminName'], 'year': year, 'cellTH': cellTH, 'clusterTH': clusterTH}])     
        if exportOpt == 'projAsset': 
            res = res[0]
            is_open = not not res._result
            message = res._result
            downloaded = None
        else:
            is_open = False
            message = ''
            # prop = {'name': model.cityName, 'year': year, 'cellTH': cellTH, 'clusterTH': clusterTH} TODO：add properties
            downloaded = dict(content=res.to_json(), filename= '_'.join([pop4def, ROIdata['adminName'], str(year)])+'.geojson')

        return is_open, message, downloaded




