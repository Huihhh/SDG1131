import os
import asyncio
import ee
import subprocess
import logging
import json
import eeconvert
import geopandas


logger = logging.getLogger(__name__)

class ExportModel:
    def __init__(self, asset_base='users/omegazhanghui/CityDefinition_GHSpop1k', asset_type='Folder'):
        self.asset_base = asset_base[:-1] if asset_base.endswith('/') else asset_base
        self.asset_type = asset_type
        # create folder if not exist
        try:
            ee.data.getAsset(asset_base)
        except Exception as e:
            logger.info(e.args)
            logger.info(f'Creating...')
            assetInfo = ee.data.createAsset({'type': asset_type}, asset_base)
            logger.info(f'Asset {asset_type}: {asset_base} created! {assetInfo}')
        
    def download_geojson(self, assetConfis):
        for city in assetConfis:
            gdf = eeconvert.fcToGdf(city['feature'])
        return gdf

    def export_asset(self, assetConfis):
        """========================> Check Exporting Status & set public <============================"""
        async def check_status(task, asset_id, city):
            while True:
                if task.status()['state'] == 'COMPLETED':
                    logger.info("Export completed: {}".format(asset_id))
                    assetInfo = ee.data.getAsset(asset_id)
                    # ========= Set property =========
                    city.pop('feature', None)
                    assetInfo.update({'properties': city})
                    ee.data.updateAsset(asset_id, assetInfo, 'properties')
                    # ======== Set publick ============
                    ee.data.setAssetAcl(asset_id, {'all_users_can_read':True})
                    # res = subprocess.getstatusoutput(f'earthengine acl set public {asset_id}')
                    # for propName, propValue in city.items():
                    #     res = subprocess.getstatusoutput(f"earthengine asset set -p {propName}={propValue} {asset_id}")
                    #     print(f"earthengine asset set -p {propName}={propValue} {asset_id}")
                    # print(res)
                    return 'Export succeed: ' + asset_id
                elif task.status()['state'] == 'FAILED':
                    print("Error with export: {}".format(asset_id))
                    print(f"Error message: {task.status()['error_message']}")
                    return 'Export failed: ' + asset_id
                else:
                    await asyncio.sleep(1)
                    # continue


        # # ================== Export city boundaries to asset =============================
        async def main():
            for city in assetConfis:
                des = city['name'].replace(' ', '_') + str(city['year'])
                assetId = self.asset_base + '/' + des
                # check if asset exists
                # assetInfo = subprocess.getstatusoutput(f'earthengine acl get {assetId}')
                try:
                    assetInfo = ee.data.getAsset(assetId)
                    ee.data.deleteAsset (assetId)
                    logger.info(f'Asset {assetId} deleted: {json.dump(assetInfo, 4)}')
                except Exception as e:
                    logger.info(e.args)
                logger.info(f'Export from GEE to asset: {assetId}')
                task = ee.batch.Export.table.toAsset(
                    collection = city['feature'],  # ee.FeatureCollection([]) is fist polygon
                    description = des, 
                    assetId=assetId
                )
                task.start()
                synctask = asyncio.create_task(check_status(task, assetId, city)) 
                return synctask

        # loop = asyncio.get_event_loop()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        s = loop.run_until_complete(asyncio.gather(main()))
        return s

if __name__ == '__main__':
    # model = ExportModel()
    assetId = 'users/omegazhanghui/Oliver_sampling10'
    assetInfo = subprocess.getstatusoutput(f'earthengine acl get {assetId}')
    if (assetInfo[0] == 0 and 'owners' in assetInfo[1]):
        res = subprocess.getstatusoutput(f'earthengine rm {assetId}')
        logger.info(f'Asset {assetId} deleted: {res}')
    else:
        logger.info(f"Asset {assetId} doesn't exist.")
