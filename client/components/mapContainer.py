from dash import html
import dash_leaflet as dl
import dash_core_components as dcc
import sd_material_ui as dm 

from ..config import mapbox_access_token

mapContainer = html.Div([
        dcc.Store(id='map-center', storage_type='session'),
        dcc.Store(id='pop4def-obj', storage_type='session'),
        dcc.Store(id='popData-obj', storage_type='session'),
        dcc.Store(id='bpData-obj', storage_type='session'),
        dcc.Store(id='cityDef-obj'),
        dcc.Store(id='result-df'),
        dm.Snackbar(id='alert-result-status', message='', open=False),
        dl.Map(
            children=[
                # dl.TileLayer(url='http://a.tiles.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=' + mapbox_access_token),   
                # Edit control 
                dl.FeatureGroup(
                    children=[
                        dl.EditControl(id="edit-control"),
                        dl.FullscreenControl(),
                        dl.LayerGroup(id='geom'),
                        ], 
                    id='feature-group'
                ),
                
                dl.LayersControl(children=[
                    dl.BaseLayer(dl.TileLayer(url='http://a.tiles.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=' + mapbox_access_token), name='Satellite', checked=True),
                    dl.BaseLayer(dl.TileLayer(url='http://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}&s=Ga'), name='Hybrid', checked=False),
                    dl.Overlay(dl.TileLayer(id='base-tile', opacity=1), checked=True, name='Satellite', id='base-overlay'),
                    dl.Overlay(dl.TileLayer(id='bp-tile', opacity=1), checked=True, name='Built-up', id='bp-overlay'),
                    dl.Overlay(dl.TileLayer(id='pop-tile', opacity=1), checked=True, name='Population Growth', id='pop-overlay'),
                    dl.Overlay(dl.TileLayer(id='pop4def-tile', opacity=1), checked=True, name='Population', id='pop4def-overlay'),
                    dl.Overlay(dl.TileLayer(id='city-definition-tile', opacity=1), checked=True, name='City Definition', id='cd-overlay'),
                    dl.Overlay(dl.TileLayer(id='admin-boundary', opacity=1, zIndex=12), checked=False, name='Admin Boundary', id='admin-overlay'),
                ], id='layers'), 
            ], 
            id='map', 
            center=(59.3293, 18.0686),
            zoom=12,
            zoomSnap=0.1,
            animate=False,
            zoomDelta = 0.1,
            style={'width': '100%', 'height': '800px', 'margin': "auto", "display": "block", "position": "relative"}
        ),
        dl.Map(
            children=[
                # dl.TileLayer(url='http://a.tiles.mapbox.com/v4/mapbox.satellite/{z}/{x}/{y}.png?access_token=' + mapbox_access_token),   
                dl.TileLayer(url='https://api.mapbox.com/styles/v1/huizhang/ck0z6vek1109a1cqk04ycp4lr/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaHVpemhhbmciLCJhIjoiY2tuMG9zb25zMGVybjJvcGJtd3VydmtlNyJ9.DmDgFIsvoGMWn_E8Kv2HUQ'),   
                dl.LayersControl(children=[], id='compare-layers'), 
                # dl.TileLayer(id='admin-boundary', opacity=1, zIndex=12)，
            ], 
            id='compare-map', 
            center=(59.3293, 18.0686),
            zoom=12,
            zoomSnap=0.1,
            animate=False,
            zoomDelta = 0.1,
            style={'width': '100%', 'height': '800px', 'margin': "auto", "display": "block", "position": "relative"}
        )
])