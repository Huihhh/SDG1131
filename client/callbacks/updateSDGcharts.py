from pydoc import doc
from dash import dcc, no_update
import itertools
import pandas as pd
from dash.dependencies import Input, Output, State
import plotly.express as px
from flask_login import current_user

from client.user import User
from ..constants import COMPARE
from ..app import app

# def read_gspread(sheet_id, sheet_name):
#     url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
#     return pd.read_csv(url)


# SDG dataframe
# df = read_gspread(sheet_id = '1AmMWSf3tcgVofAGqH0H0jJVWLSnnX2A60RFzvJlYXgU', sheet_name = 'SDG11.3.1_Calculations')
# df = df.round(3)

@app.callback(
    Output('sdg-records', 'data'),
    Input('loc-url', 'pathname')
)
def update_db_store(pathname):
    if pathname == '/':
        if current_user.is_authenticated:
            data = User.get_records(current_user.id)
            # newData = df.to_dict('records')
            # for entry in newData:
            #     doc_name = ''.join([entry['Tool'], str(entry['T1']), str(entry['T2']), entry['AOI'], str(entry['FAO Level']), entry['City Definition'], entry['Population'], entry['Built-Up'],])
            #     User.add_record(current_user.id, doc_name, entry)
            # print('---------------- data', data)
            return pd.DataFrame(data).to_dict('index')
    
    return no_update

@app.callback(
    Output('datatable-interactivity', "data"),
    Input('city-dropdown-select', 'value'),
    Input('sdg-records', 'data'),
)
def update_table(selected_cities, data):
    if not data:
        return no_update
    df = pd.DataFrame.from_dict(data, orient='index').round(3)
    # print(df)
    # dff = df[df.AOI.isin(selected_cities)].sort_values(by=['Built-Up', 'T1'])
    # print(len(dff))
    return df.to_dict('records')


def group_column(series):
    v = '-'.join([str(series['T1']), str(series['T2'])])
    # uniqueValues = pd.unique(series['Built-Up'])
    # x = itertools.product(v, uniqueValues)
    return '<br>'.join([v, series['Built-Up']])

def make_y_title(yCol):
    if 'pop' in yCol:
        return 'Population'
    elif 'Built' in yCol:
        return 'Area/Square km'
    else: 
        return 'SDG 11.3.1'

def make_title(yCol):
    if 'T1' in yCol:
        return 'SDG 11.3.1 - Population in 2000'
    elif 'T2' in yCol:
        return 'SDG 11.3.1 - Population in 2015'
    else: 
        return 'SDG 11.3.1 2000-2015'


def make_figure(dff, city, comp, yCol, colors):
    city = city if isinstance(city, list) else [city]    
    title = 'SDG 11.3.1 ' + city[0]
    newdf = dff[dff.AOI.isin(city)]
    if comp['label'] == 'Compare Builtup data':
        newdf = newdf[(newdf['Tool']=='EE App') & (newdf['Population']=='GHS-Pop 250m')]
        newdf.loc[:, 'Period'] = newdf[['T1', 'T2']].apply(lambda x: '-'.join([str(x['T1']), str(x['T2'])]), axis=1) 
        xCol = 'Period'
        color = 'Built-Up'

    elif comp['label'] == 'Compare Population Growth data':
        newdf = newdf[(newdf['Tool']=='EE App') & (newdf['Built-Up']=='GHS-Built 38m') & (newdf['T1']==2000)]
        xCol = 'AOI'
        title = make_title(yCol)
        color = 'Population'

    else:
        newdf = newdf[newdf['Population']=='GHS-Pop 250m']
        newdf.loc[:, 'xaxis'] = newdf[['T1', 'T2', 'Built-Up']].apply(group_column, axis=1)
        xCol = 'xaxis'
        color = 'Tool'  


    # name = colValue if isinstance(colValue, str) else colValue['name']   
    # colValue = colValue if isinstance(colValue, str) else colValue['name']
    
    # newdf.AOI = newdf.AOI.astype('category')
    # newdf.AOI.cat.set_categories(city, inplace=True)
    # newdf = newdf.sort_values('AOI')   
    fig = px.bar(newdf, 
                x=xCol, 
                y=yCol, 
                text=yCol, 
                color=color, 
                barmode="group", 
                category_orders={'AOI': city, 'T1': [1975, 1990, 2000, 2015], 'Population': ['WorldPop 100m', 'GHS-Pop 250m', 'GPWv4 30 arc-second']}, 
                color_discrete_sequence=colors,
                facet_row_spacing=0,
                )

    # fig.update_traces(width=0.1, gap=0,)

    fig.update_layout(                 
        xaxis = {"automargin": True,
                'title': {"text":comp['xtitle']}},
        yaxis = {"automargin": True,
                 "title": {"text": make_y_title(yCol)},
                 'gridcolor': '#e6e6e6'
                 },
        legend = {'x': 0, 'y': 0.99},# 'orientation':"h", 'xanchor':"right", 'yanchor':"bottom",},
        # legend = {'x': 0.95, 'y': 0.99, 'orientation':"h", 'xanchor':"right", 'yanchor':"bottom",},
        # width=200, #[0.3] * 21,
        # bargap=0, # [0.2] * 21,
        bargroupgap=0,
        height=500,
        margin={"t": 80, "l": 10, "r": 10},
        title={'text':title, 'x':0.5},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text= '',
        font={'size': 20})
    return fig

@app.callback(
    # Output('sdg-charts-container-Compare-Builtup-data', 'children'),
    [Output('sdg-charts-container-'+comp['label'].replace(' ', '-'), "children") for comp in COMPARE],
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('city-dropdown-select', 'value'),
    Input('datatable-interactivity', "filter_query"),
    Input('res-tabs', 'value'),
    Input('sdg-records', 'data'),
)
def update_graphs(rows, derived_virtual_selected_rows, selected_cities, filter, selectedTab, data):
    # When the table is first rendered, `derived_virtual_data` and
    # `derived_virtual_selected_rows` will be `None`. This is due to an
    # idiosyncrasy in Dash (unsupplied properties are always None and Dash
    # calls the dependent callbacks when the component is first rendered).
    # So, if `rows` is `None`, then the component was just rendered
    # and its value will be the same as the component's dataframe.
    # Instead of setting `None` in here, you could also set
    # `derived_virtual_data=df.to_rows('dict')` when you initialize
    # the component.
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []
    if not data:
        return no_update

    df = pd.DataFrame.from_dict(data, orient='index').round(3)

    dff = df if rows is None else pd.DataFrame(rows)

    colors1 = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]
    colors2 = ['#ff9933' if i in derived_virtual_selected_rows else '#ff9933'
              for i in range(len(dff))]  
    colors3 = ['#267326' if i in derived_virtual_selected_rows else '#267326'
              for i in range(len(dff))]      
    colors4 = ['#8f00b3' if i in derived_virtual_selected_rows else '#8f00b3'
              for i in range(len(dff))]      
    colors = [colors4, colors1, colors3, colors2]        

    def make_xaxis(city, comp, colValue):
        if comp['label'] == 'Compare Population Growth data':
            return city #sorted(city)
        city = city if isinstance(city, list) else [city]
        colName = comp['colName']
        colValue = colValue if isinstance(colValue, str) else colValue['name']
        filtered_T1 = dff[(dff[colName]==colValue) & dff.AOI.isin(city)]['T1']
        filtered_T2 = dff[(dff[colName]==colValue) & dff.AOI.isin(city)]['T2']
        s = ['-'.join([str(t1), str(t2)]) for (t1, t2) in zip(filtered_T1, filtered_T2)]
        if comp['label'] == 'Compare Tools':
            uniqueValues = pd.unique(dff['Built-Up'])
            x = itertools.product(s, uniqueValues)
            s = ['<br>'.join(xx) for xx in x]
        return s
    
    def make_yaxis(dff, city, comp, colValue):
        city = city if isinstance(city, list) else [city]
        colValue = colValue if isinstance(colValue, str) else colValue['name']
        if comp['label'] == 'Compare Builtup data':
            newdf = dff[(dff[comp['colName']]==colValue) & (dff['Tool']=='EE App') & (dff['Population']=='GHS-Pop 250m')]
        elif comp['label'] == 'Compare Population Growth data':
            newdf = dff[(dff[comp['colName']]==colValue) & (dff['Tool']=='EE App') & (dff['Built-Up']=='GHS-Built 38m') & (dff['T1']==2000)]
        else:
            newdf = dff[(dff[comp['colName']]==colValue) & newdf.AOI.isin(city)]
        newdf = newdf[newdf.AOI.isin(city)]
        newdf.AOI = newdf.AOI.astype('category')
        newdf.AOI.cat.set_categories(city, inplace=True)
        newdf = newdf.sort_values('AOI')['pop - T1']#.loc[:, ['pop - T1', 'pop - T2']].melt(value_name='newcol')['newcol']#['SDG 11.3.1']
        return newdf

    idx = int(selectedTab[-1]) - 1

    def compare_tab(tabName, compName):
        show = COMPARE[idx]['label'] == compName
        return show
        


    if COMPARE[idx]['label'] == 'Compare Population Growth data':
        updates = [dcc.Graph(
            id='compare-pop-growth-data',
            figure=make_figure(dff, selected_cities, comp, 'pop - T2', colors),
            style={'width': '100%', 'height': '90vh'}
        ) if compare_tab(selectedTab, comp['label']) else no_update for comp in COMPARE]
        # updates = [dcc.Graph(
        #     id='compare-pop-growth-data',
        #     figure={
        #         "data": [
        #             {
        #                 "x": make_xaxis(selected_cities, comp, colValue),
        #                 "y": make_yaxis(selected_cities, comp, colValue),
        #                 "text": make_yaxis(selected_cities, comp, colValue),
        #                 "type": "bar",
        #                 'width': 0.3,
        #                 'bargap': 0.2,
        #                 'bargroupgap': [0.1] * 21,
        #                 "marker": {"color": colors[i]},
        #                 'name': colValue if isinstance(colValue, str) else colValue['name'],

        #             } for i, colValue in enumerate(comp['value'])],
                
        #         "layout": {
        #             "xaxis": {"automargin": True,
        #                     "title": {"text":comp['xtitle']}},
        #             "yaxis": {
        #                 "automargin": True,
        #                 "title": {"text": 'Population'}
        #             },
        #             'legend': {'x': 0, 'y': 1},
        #             # 'width': 200, #[0.3] * 21,
        #             'bargap': 0.1, # [0.2] * 21,
        #             "height": 500,
        #             # "margin": {"t": 60, "l": 10, "r": 10},
        #             'title': f"SDG indicator 11.3.1 - Population in 2000",
        #             'font': {'size': 12}
        #         },
        #     },
        #     style={'width': '180vh', 'height': '90vh'}
        # ) if compare_tab(selectedTab, comp['label']) else no_update for comp in COMPARE]
    else: 
        updates = [[dcc.Graph(
            id=city,
            figure=make_figure(dff, city, comp, 'SDG 11.3.1', colors),
            style={'width': '100%', 'height': '90vh'}
        ) for city in selected_cities] if compare_tab(selectedTab, comp['label']) else no_update for comp in COMPARE]
        # updates = [[dcc.Graph(
        #             id=city,
        #             figure={
        #                 "data": [
        #                     {
        #                         "x": make_xaxis(city, comp, colValue),
        #                         "y": make_yaxis(city, comp, colValue),
        #                         "text": make_yaxis(city, comp, colValue),
        #                         "type": "bar",
        #                         "marker": {"color": colors[i]},
        #                         'name': colValue if isinstance(colValue, str) else colValue['name'],
        #                     } for i, colValue in enumerate(comp['value'])],
                        
        #                 "layout": {
        #                     "xaxis": {"automargin": True,
        #                             "title": {"text": make_annotations(comp)}},
        #                     "yaxis": {
        #                         "automargin": True,
        #                         "title": {"text": 'SDG 11.3.1'}
        #                     },
                            
        #                     "height": 500,
        #                     "margin": {"t": 60, "l": 10, "r": 10},
        #                     'title': f"SDG indicator 11.3.1 {city}",
        #                     'font': {'size': 20}
        #                 },
        #             },
        #             style={'width': '180vh', 'height': '90vh'}
        # ) for city in selected_cities] if compare_tab(selectedTab, comp['label']) else no_update for comp in COMPARE] 

    return updates