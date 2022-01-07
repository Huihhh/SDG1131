import json
import pandas as pd
from gspread_pandas import Spread, Client, conf

from apiConfig.eeAuth import key
from client.database import read_gspread


class Gspread:
    def __init__(self, sheet_id='1rgnA03RAsY5U1xTyY4EJgKrL5rMiIjunJtVuUkx_nVs', sheet_name='Updated_City_Definition_SDG11.3.1_Calculations'):
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name

    # client = Client(config={'creds_dir': 'apiConfig/'})

    def update_gspread(self, df):
        old_df = read_gspread(self.sheet_id, self.sheet_name)
        new_df = self.update_df(old_df, df)
        self.write_gspread(new_df)

    def update_df(self, old_df, new_df):
        # ================ update the table ================
        for idx, row in new_df.iterrows():
            cond = (old_df['Tool'] == row['Tool']) & \
                (old_df['AOI'] == row['AOI']) & \
                (old_df['FAO Level'] == row['FAO Level']) & \
                (old_df['City Definition'] == row['City Definition']) & \
                (old_df['Population'] == row['Population']) & \
                (old_df['Built-Up'] == row['Built-Up']) & \
                (old_df['T1'] == int(row['T1'])) & \
                (old_df['T2'] == int(row['T2']))
            filtered = old_df[cond]

            if len(filtered) == 1:
                if len(row.compare(filtered.iloc[0])) > 0: # if there's a difference, replace the row
                    old_df.loc[cond] = row.to_list()
            else:
                old_df = old_df.append(row, ignore_index=True)
        return old_df

    def write_gspread(self, df):
        # ================== Write sheet ========================
        # 'Example Spreadsheet' needs to already exist and your user must have access to it
        # This will ask to authenticate if you haven't done so before
        spread = Spread(self.sheet_id, config=json.loads(key))

        # Save DataFrame to worksheet 'New Test Sheet', create it first if it doesn't exist
        spread.df_to_sheet(df, index=False, sheet=self.sheet_name, start='A1', replace=False, freeze_headers=True)
        print('Sheet updated!')


if __name__ == '__main__':
    sheet_id = '1rgnA03RAsY5U1xTyY4EJgKrL5rMiIjunJtVuUkx_nVs'
    sheet1 = 'sheet7'
    sheet2 = 'City_Definition_SDG11.3.1_Calculations'
    gspread = Gspread(sheet_id, sheet1)
    df2 = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet2}')
    gspread.update_gspread(df2)