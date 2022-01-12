import pandas as pd
from .constants import *
from dataset import *

def read_gspread(sheet_id, sheet_name):
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
    return pd.read_csv(url)

# SDG dataframe
df = read_gspread(sheet_id = '1AmMWSf3tcgVofAGqH0H0jJVWLSnnX2A60RFzvJlYXgU', sheet_name = 'SDG11.3.1_Calculations')
df = df.round(3)

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