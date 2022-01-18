from os import mkdir
import yaml
from pathlib import Path
import urllib3
import requests
from tqdm import tqdm
import pandas as pd
import os

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

root = Path('download_data')
print(root.exists())
file = root / 'download_config.yaml'



def get_patch_corners(lng_range: tuple, lat_range: tuple) -> list:
    lng_min, lng_max = lng_range
    lat_min, lat_max = lat_range
    
    lng_min = int(lng_min) - 2 if int(lng_min) % 2 == 0 else int(lng_min) - 3
    lng_max = int(lng_max) if int(lng_max) % 2 == 0 else int(lng_max) + 1
    
    lat_min = int(lat_min) - 2 if int(lat_min) % 2 == 0 else int(lat_min) - 3
    lat_max = int(lat_max) if int(lat_max) % 2 == 0 else int(lat_max) + 1
    
    corners = []
    for east in range(lng_min, lng_max + 1, 2):
        for north in range(lat_min, lat_max + 1, 2):
            corners.append((east, north))
            # print(f'{east} - {north}')
    return corners

def download_wsf2019_patch(roi_id: str, east: int, north: int):
    url = f'https://download.geoservice.dlr.de/WSF2019/files/WSF2019_v1_{east}_{north}.tif'
    response = requests.get(url)
    if response.status_code == 200:
        http = urllib3.PoolManager()
        r = http.request('GET', url, preload_content=False)
        file = root / 'data' / f'WSF2019_v1_{east}_{north}.tif'
        if not file.exists():
            print(f'downloading {roi_id}: {file.name}')
            with open(file, 'wb') as out:
                while True:
                    data = r.read(100000)
                    if not data:
                        break
                    out.write(data)

            r.release_conn()

def download_worldpop_patch(year: str, countryId: str, group='Global_2000_2020_1km_UNadj'):
    countryId_cap = countryId.upper()
    countryId_s = countryId.lower()
    url = f'https://data.worldpop.org/GIS/Population/{group}/{year}/{countryId_cap}/{countryId_s}_ppp_{year}_1km_Aggregated_UNadj.tif'
    datadir = root / 'data'
    file = root / 'data' / f'WorlPop1km_{countryId_cap}_{year}.tif'
    os.system(f'wget -P {datadir.absolute()} {url}')
    # response = requests.get(url)
    # if response.status_code == 200:
    #     http = urllib3.PoolManager()
    #     r = http.request('GET', url, preload_content=False)
    #     (root / 'data').mkdir(parents=True, exist_ok=True)
    #     file = root / 'data' / f'WorlPop1km_{countryId_cap}_{year}.tif'
    #     print(file)
    #     if not file.exists():
    #         print(f'downloading {countryId_cap}: {file.name}')
    #         with open(file, 'wb') as out:
    #             while True:
    #                 data = r.read(100000)
    #                 if not data:
    #                     break
    #                 out.write(data)

    #         r.release_conn()
    
data = 'worldpop'
print(root.absolute())
if 'worldpop' in data:
    countryInfo = pd.read_csv(root/ 'countries_codes_and_coordinates.csv')
    for code in countryInfo['Alpha-3 code']:
        download_worldpop_patch('2016', code.replace('"', '').replace(' ', ''))
            

if 'wsf' in data:
    with open(str(file)) as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
        content = yaml.load(file, Loader=yaml.FullLoader)
        rois = content['ROIS']

    for i, roi in enumerate(rois):
        print(i, roi['ID'])
        roi = rois[66]
        lng_min, lng_max = roi['LNG_RANGE']
        lat_min, lat_max = roi['LAT_RANGE']
        corners = get_patch_corners(roi['LNG_RANGE'], roi['LAT_RANGE'])
        for roi in rois:
            corners = get_patch_corners(roi['LNG_RANGE'], roi['LAT_RANGE'])
            for corner in corners:
                east, north = corner
                download_wsf2019_patch(roi['ID'], east, north)


