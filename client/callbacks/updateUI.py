from dash.dependencies import Input, Output, State
from ..app import app
from ..constants import CITY_CONFIGS, DATASET, CD_DATA, PG_DATA, BP_DATA, WORLD_POP_1km

# ======================= Update UI =======================
@app.callback(
    Output("adminlevel-radioItem", 'value'),
    Input('city-single-select', 'value'),
)
def update_admin_level(cityName):
    return str(CITY_CONFIGS[cityName]['adminLevel'])

@app.callback(
    Output('year-dropdown-select', 'value'),
    Output('year-dropdown-select', 'options'),
    Input('pop4def-radioItem', 'value'),
)
def update_years(pop4def):
    selectable = DATASET[pop4def].years
    # if pop4def == GHS_POP_1km: # select group 1 disable group 2
    #     selectable = [1975, 1990, 2000, 2015]
    # else: #TODO: add worldPop
    #     selectable = [2000, 2005, 2010, 2015]
    value = selectable[1]
    options = [{'label': y, 'value': y} for y in selectable]
    # options.extend([{'label': y, 'value': y, 'disabled': True} for y in YEARS if y not in selectable])
    return value, options

@app.callback(
    Output('built-radioItem', 'value'),
    Output('built-radioItem', 'options'),
    Input('pop4def-radioItem', 'value'),
    Input('year-dropdown-select', 'value'),
)
def update_bp_selector(pop4def, year):
    selectable = [d['name'] for d in BP_DATA if year in DATASET[d['name']].years]
    options = [{'label': y, 'value': y} for y in selectable]
    return selectable[0], options    

# @app.callback(
#     # Output('op4def-radioItem', 'value'),
#     Output('pop4def-radioItem', 'options'),
#     Input('city-single-select', 'value'),
# )
# def update_pop4def_selector(city):
#     pop4def_options = [{'label': d['name'], 'value': d['name'], 'disabled': False} for d in CD_DATA]
#     pop_options = [{'label': d['name'], 'value': d['name'], 'disabled': False} for d in PG_DATA]

#     if city not in ['Beijing', 'Tianjin', 'Shanghai', 'Guangzhou']:
#         pop4def_options = [{**item, 'disabled': True} if item['label']==WORLD_POP_1km['name'] else item for item in pop4def_options]
#     return pop4def_options

def get_first_abled(options):
    for opt in options:
        if not opt['disabled']:
            return opt['value']

@app.callback(
    Output('pop-radioItem', 'value'),
    Output('pop-radioItem', 'options'),
    Input('city-single-select', 'value'),
    Input('year-dropdown-select', 'value'),
)
def update_pop_selector(city, year):
    pop_options = [{'label': d['name'], 'value': d['name'], 'disabled': True} for d in PG_DATA]
    pop_options = [{**item, 'disabled': False} if year in DATASET[item['value']].years else item for item in pop_options]

    if city not in ['Beijing', 'Tianjin', 'Shanghai', 'Guangzhou']:
        pop_options = [{**item, 'disabled': True} if item['label']==WORLD_POP_1km else item for item in pop_options]
    # if city not in ['']
    return get_first_abled(pop_options), pop_options


@app.callback(
    Output('start-year-select', 'options'),
    Input('pop-radioItem', 'value'),
    Input('built-radioItem', 'value'),
    Input('year-dropdown-select', 'value')
)
def update_startyear_selector(popData, bpData, endYear):
    commonYears = [y for y in DATASET[popData].years if (y in DATASET[bpData].years and y<endYear)]
    return [{'label': y, 'value': y} for y in commonYears]


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]
