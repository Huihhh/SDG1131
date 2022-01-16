import ee
# from dash.dependencies import Input, Output, State
import dash_leaflet as dl
from dash import callback_context
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import Output, Input, State, ServersideOutput
import functools

from model.eeModel import *
from ..app import app
from ..constants import CITY_CONFIGS 
from ..database import DATASET

def get_tile_url(mapid):
    return "https://earthengine.googleapis.com/v1alpha/" + mapid + "/tiles/{z}/{x}/{y}"


# ================================= Update ROI =============================
@app.callback(
    Output("map", "center"),
    Output("compare-map", "center"),
    ServersideOutput("map-center", 'data'),
    Output('admin-boundary', 'url'),
    # Output('roi-bounds', 'data'),
    Input('city-single-select', 'value'),
    Input('draw-roi', 'n_clicks'),
    Input("adminlevel-radioItem", 'value'),
    State('edit-control', 'geojson'),
    State("map-center", 'data'),
)
def update_map_center(cityName, n_clicks, adminLevel, drawnPoly, data): #TODO: if draw area isn't in the list, clear all geometries when jump to another city
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    drawROI = True if 'draw-roi' in changed_id else False 
    data = data or {'useAdmin': True, 'cityName': None}
    print(drawnPoly)

    if drawROI: # if use draw ROI
        roi = ee.FeatureCollection(drawnPoly).geometry()
        cityCoords = roi.centroid()
        center = cityCoords.getInfo()['coordinates'][::-1]
        admin, adminName = get_admin(drawROI, cityName, cityCoords, adminLevel)
        
        if 'Shanghai' in adminName:
            suzhouCity = ee.FeatureCollection('projects/gisproject-1/assets/Suzhou_admin')
            roi = roi.difference(suzhouCity.geometry(), maxError=10000)

        data.update({'useAdmin': False, 'adminName': adminName, 'center': cityCoords, 'roi': roi, 'roiBound': roi.bounds()})
    else: # use admin
        center = CITY_CONFIGS[cityName]['coords'][0][::-1]
        cityCoords = ee.Geometry.MultiPoint(CITY_CONFIGS[cityName]['coords'])
        admin, adminName = get_admin(drawROI, cityName, cityCoords, adminLevel)

        data.update({'useAdmin': True, 'adminName': adminName, 'center': cityCoords, 'roi':admin, 'roiBound': admin.geometry().bounds()})
    mapid = admin.style(**{'color': '#99ccff', 'fillColor': "#ff000000"}).getMapId()['mapid'] 
    pop4def = DATASET['GHS-Pop 1km']()
    data.update({'test': pop4def})
    return center, center, data, get_tile_url(mapid)


# ================================= Update base image =============================
# @functools.lru_cache(maxsize=32)
def get_bg_mapid(cityBounds, year):
    img, vmin, vmax = queryBaseImg(cityBounds, int(year))
    vis_NIR = {"opacity":1,"bands":["NIR","R","G"],"min":vmin,"max":vmax,"gamma":1}
    mapid = img.visualize(**vis_NIR).getMapId()['mapid'] 
    return mapid

@app.callback(
    Output('base-tile', 'url'),
    Input('year-dropdown-select', 'value'),
    Input('map-center', 'data'),
)
def update_base_tile(year, data):
    mapid = get_bg_mapid(data['roiBound'], year)
    return get_tile_url(mapid)


# ================================= Update builtup image =============================
# @functools.lru_cache(maxsize=32)
def get_bp_mapid(bp, city, year, cityBounds):
    bpData = DATASET[bp](th = CITY_CONFIGS[city]['bp_density_th'])
    mapid = bpData.queryImageByYearAndROI(int(year), cityBounds).visualize(**bpData.visParam).getMapId()['mapid']
    return mapid, bpData


@app.callback(
    ServersideOutput('bpData-obj', 'data'),
    Output('bp-tile', 'url'),

    Input('year-dropdown-select', 'value'),
    Input('built-radioItem', 'value'),
    Input('map-center', 'data'),
    State('city-single-select', 'value'),
)
def update_bp_tile(year, bp, ROIdata, city):
    if ROIdata is None:
        raise PreventUpdate
    mapid, bpData = get_bp_mapid(bp, city, year, ROIdata['roiBound'])
    print('update_bp_tile')
    return bpData, get_tile_url(mapid)


# ================================= Update population image (for city definition) =============================
# @functools.lru_cache(maxsize=32)
def get_pop4def_map(pop4def, year, ROIdata):
    pop4def = DATASET[pop4def]()
    pop4defImg = get_pop_img(pop4def, ROIdata['center'], ROIdata['roiBound'], int(year))
    return pop4defImg, pop4def

# @functools.lru_cache(maxsize=32)
def get_pop4def_mapid(pop4def, visMin, visMax):
    vis_pop = {'min': visMin, 'max':visMax, 'palette': ["ffe8d4","ffd1ba","ffc5a9","ffa083","ff985c","ff7c3d","ff4021","ff5616","ff0000","a72a05"]}
    return pop4def.getMapId(vis_pop)['mapid']

@app.callback(
    Output('pop4def-tile', 'url'),
    ServersideOutput('pop4def-obj', 'data'),
    Input('pop4def-radioItem', 'value'),
    Input('year-dropdown-select', 'value'),
    Input('map-center', 'data'),
    Input('vis-param-state', 'n_clicks'),
    State('vis-min-state', 'value'),
    State('vis-max-state', 'value'),
)
def update_pop4def_tile(pop4def, year, data, ok, visMin, visMax):
    if data is None:
        raise PreventUpdate
    pop4defImg, pop4def = get_pop4def_map(pop4def, year, data)
    mapid = get_pop4def_mapid(pop4defImg, visMin, visMax)
    print('update_pop4def_tile')
    return get_tile_url(mapid), pop4def


# ================================= Update population image (for population growth) =============================
# @functools.lru_cache(maxsize=32)
def get_pg_mapid(pop, year, cityCoords, cityBounds):
    popData = DATASET[pop]()
    vis_pop = {'min': popData.visMin, 'max':popData.visMax, 'palette': ["ffe8d4","ffd1ba","ffc5a9","ffa083","ff985c","ff7c3d","ff4021","ff5616","ff0000","a72a05"]}
    mapid = get_pop_img(popData, cityCoords, cityBounds, int(year)).getMapId(vis_pop)['mapid']
    return mapid, popData

@app.callback(
    Output('pop-tile', 'url'),
    ServersideOutput('popData-obj', 'data'),
    Input('year-dropdown-select', 'value'),
    Input('pop-radioItem', 'value'),
    Input('map-center', 'data'),
)
def update_pop_tile(year, pop, ROIdata):
    if ROIdata is None:
        raise PreventUpdate
    mapid, popData = get_pg_mapid(pop, year, ROIdata['center'], ROIdata['roiBound'])
    print('update_pop_tile')
    return get_tile_url(mapid), popData

def flip_coords(coords):
    if isinstance(coords[0][0], float):
        return [c[::-1] for c in coords]
    else:
        coordList = []
        for coord in coords:
            flipped = flip_coords(coord)
            coordList.append(flipped)
        return coordList
        
# ================================= Update City Definition =============================
def get_cityDef(pop4def, year, ROIdata, cellTH, clusterTH):
    pop4def = DATASET[pop4def](cellTH, clusterTH)
    cityDef = define_city(pop4def, int(year), ROIdata['center'], ROIdata['roi'], ROIdata['useAdmin'])
    mapid = cityDef.style(**{'color': 'blue', 'fillColor': "#ff000000"}).getMapId()['mapid']
    return mapid, cityDef

@app.callback(
    Output('city-definition-tile', 'url'),
    ServersideOutput('cityDef-obj', 'data'),
    Input('year-dropdown-select', 'value'),
    Input('pop4def-radioItem', 'value'),
    Input('submit-button-state', 'n_clicks'),
    Input('map-center', 'data'),
    Input('update-city-definition', 'n_clicks'),
    
    State('cell-TH-state', 'value'),
    State('cluster-TH-state', 'value'),   
    State('feature-group', 'children'),
    State('cityDef-obj', 'data'),
)
def update_cd_tile(year, pop4def, n_clicks, ROIdata, updateClick, cellTH, clusterTH, features, cityDefs):
    if ROIdata is None:
        raise PreventUpdate
    cityDefs = cityDefs or {}
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    update = True if 'update-city-definition' in changed_id else False # if update button is most recently clicked
    if update:
        cityDef = ee.Geometry.Polygon(features[-1]['props']['positions'])
        mapid = cityDef.style(**{'color': 'blue', 'fillColor': "#ff000000"}).getMapId()['mapid']
        return mapid, cityDef
    mapid, cityDef = get_cityDef(pop4def, year, ROIdata, cellTH, clusterTH)
    cityDefs.update({f'{pop4def}{year}': cityDef})
    return get_tile_url(mapid), cityDefs

@app.callback(
    Output('feature-group', 'children'),
    Input('cityDef-obj', 'data'),
    Input('update-city-definition', 'n_clicks'),
    State('feature-group', 'children'),
    State('city-definition-tile', 'url'),
    State('pop4def-radioItem', 'value'),
    State('year-dropdown-select', 'value'),
)
def update_cd_geom(cityDefs, n_clicks, geometries, url, pop4def, year):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    update = True if 'update-city-definition' in changed_id else False # if update button is most recently clicked
    if update:
        raise PreventUpdate
    # add city definition poly to editable feature group
    if cityDefs is None:
        raise PreventUpdate
    cityDef = cityDefs[pop4def+str(year)]
    if cityDef is None:
        raise PreventUpdate
    coords = cityDef.geometry().getInfo()['coordinates']
    for coord in coords:
        coord = flip_coords(coord)
        geometries.append(dl.Polygon(positions=coord))
    return geometries

# # ================================= Update compare map layers =============================
@app.callback(
    Output('compare-layers', 'children'),
    Input('compare-bpdata', 'n_clicks'),
    Input('map-center', 'data'),
    State('built-radioItem', 'options'),
    State('city-single-select', 'value'),
    State('year-dropdown-select', 'value'),
    State('pop4def-radioItem', 'value'),
    prevent_initial_call=True, 
)
def update_bp_compare(n_clicks, data, bpOptions, city, year, pop4def):
    if n_clicks <= 0 or data is None:
        raise PreventUpdate
    overlayers = []
    for opt in bpOptions:
        bpData = DATASET[opt['value']](th = CITY_CONFIGS[city]['bp_density_th'])
        mapid = bpData.queryImageByYearAndROI(int(year), data['roiBound']).visualize(**bpData.visParam).getMapId()['mapid']
        layerName = f"<p style='display: inline-block;color:{bpData.visParam['palette'][0]}'>{opt['label']}</p>"
        overlayers.append(dl.Overlay(dl.TileLayer(url=get_tile_url(mapid)), checked=True, name=layerName))
    defMap = ee.FeatureCollection(f"projects/gisproject-1/assets/CityDefinition_{pop4def.replace(' ', '')}/{city.replace(' ', '_')}{year}")
    mapid = defMap.style(**{'color': 'blue', 'fillColor': "#ff000000"}).getMapId()['mapid']
    # model.cityDef[pop4def + str(year)] = model.define_city(int(year))
    # mapid = model.cityDef[pop4def + str(year)].style(**{'color': 'blue', 'fillColor': "#ff000000"}).getMapId()['mapid']
    overlayers.append(dl.Overlay(dl.TileLayer(url=get_tile_url(mapid)), checked=True, name="<p style='display:inline-block;color:blue'>City Definition</p>"))
    return overlayers


# @app.callback(
#     Output('alert-update-status', 'open'),
#     Output('alert-update-status', 'message'),
#     # update city definition
#     Input('update-city-definition', 'n_clicks'),
#     State('year-dropdown-select', 'value'),
#     State('feature-group', 'children'),
#    prevent_initial_call=True, 
# )
# def update_city_definition(n_click, year, features): #TODO: make editedPoly current selected/edited one?
#     changed_id = [p['prop_id'] for p in callback_context.triggered][0]
#     update = True if 'update-city-definition' in changed_id else False # if update button is most recently clicked
#     if update:
#         cityDef = ee.Geometry.Polygon(features[-1]['props']['positions'])
#         return True, 'Updated!'
#     else:
#         return False, '' #TODO: show error message