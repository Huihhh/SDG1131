import zipfile
import os
from pathlib import Path
import subprocess
import logging
import re, sys
logging.basicConfig(
    stream=sys.stdout, 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    )

logger = logging.getLogger(__name__)


class UploadModel:

    def __init__(self, gs_dir, local_dir, assetFolder='CityDefinition_GHSpop1k_v1', asset_type='folder') -> None:
        self.assetFolder = assetFolder
        self.asset_type = asset_type
        self.gs_dir = gs_dir
        self.base_dir = Path(local_dir) # dir that contains .zip files
        self.tifFolder = self.base_dir / 'tif'
        self.cogFolder = self.base_dir  / "COG"
        self.tifFolder.mkdir(exist_ok=True)
        self.cogFolder.mkdir(exist_ok=True)
        # create asset folder/collection if not exist
        output = subprocess.getstatusoutput(f'earthengine acl get {assetFolder}')
        if (output[0] == 1 and 'not exist' in output[1]):
            res = subprocess.getstatusoutput(f'earthengine create {self.asset_type} {assetFolder}')
            logger.info(f'Asset {asset_type}: {assetFolder} created!')
        else:
            logger.info(f'Asset info {output[1]}')
        # TODO: create gcs folder if not exist
        self.unzip()
        
    
    def download(self, url): #TODO
        pass


    def unzip(self):
        '''STEP 1: unzip'''
        for file in os.listdir(self.base_dir):
            if file.endswith('.zip'):
                with zipfile.ZipFile(self.base_dir / file, 'r') as zip_ref:
                    zip_ref.extractall(self.tifFolder)

    def upload(self):
        fileList = [filename[:-4] for filename in os.listdir(self.tifFolder) if filename.endswith('.tif') and filename not in os.listdir(self.cogFolder)]
        TASK_DICT = {}

        for filename in fileList:
            input_url = self.tifFolder / f"{filename}.tif"
            cog_url = self.cogFolder / f"{filename}.tif"

            # '''STEP 2: convert to COG'''
            os.system(f"gdal_translate {input_url} {cog_url} -co TILED=YES -co COPY_SRC_OVERVIEWS=YES -co COMPRESS=LZW")

            # '''STEP 3: upload to GCS'''
            os.system(f"gsutil -m cp -r {cog_url} {self.gs_dir}/")

            # '''STEP 4: upload to GEE asset'''
            task_dict = self.upload_cog_into_eeImgCol(fileList=[filename], upload_flag=True) #TODO: why fileList?
            TASK_DICT.update(task_dict)
            self.check_status_and_set_property(TASK_DICT)

    
    def upload_cog_into_eeImgCol(self, fileList=None, upload_flag=True):
        """ upload_cog_as_eeImgCol """
        # print(os.path.split(gs_dir))
        print(f"eeImgCol: {self.assetFolder}")

        if upload_flag:

            """ Upload to earth engine asset """
            task_dict = {}
            for filename in fileList:
                print(f"\n{filename}")
                print("--------------------------------------------------------------------")

                # tmp = filename.split('_') #TODO: parameterize assetname
                # assetname = f"{tmp[2]}_{'_'.join(tmp[7:])}"
                asset_id = f"{self.assetFolder}/{filename}"
                ee_upload_image = f"earthengine upload image --force --asset_id={asset_id} {self.gs_dir}/{filename}.tif"
                print(ee_upload_image)
                # os.system(ee_upload_image)

                ee_upload_response = subprocess.getstatusoutput(ee_upload_image)[1]
                print('gcs upload res: ', ee_upload_response)
                task_id = ee_upload_response.split("ID: ")[-1]
                task_dict.update({filename: {'task_id': task_id, 'asset_id': asset_id}})

                print(f"{asset_id}")
                # pprint(f"task id: {task_id}")
                print()
            return task_dict

    def check_status_and_set_property(self, task_dict):

        """ check upload status """
        print("=============> check upload status <===============")
        # upload_finish_flag = False
        # while(not upload_finish_flag):
        #     time.sleep(60) # delay 30s
            
        upload_finish_flag = True
        for filename in task_dict.keys():
            asset_id = task_dict[filename]['asset_id'] #f"users/omegazhangpzh/Sentinel1/{filename}"
            task_id = task_dict[filename]['task_id']

            check_upload_status = f"earthengine task info {task_id}"
            response = subprocess.getstatusoutput(check_upload_status)[1]
            print(response)
            if "COMPLETED" in response:
                state = 'COMPLETED'
                # os.system(f"earthengine acl set public {asset_id}")
                # """ Set Properties """
                self.set_image_property(asset_id)
                # task_dict.pop(filename)
            elif 'FAILED' in response:
                state = 'FAILED'
                upload_finish_flag = True
            else: 
                state = 'UPLOADING'
                upload_finish_flag = False
            task_dict[filename].update({'state': state})
            # check_asset_permission(asset_id)
            print(f"\n{filename}: {state}")

        print("-----------------------------------------------------------------------\n")
        # pprint(task_dict)
        return upload_finish_flag
        
    def set_image_property(self, asset_id):
        product_id = os.path.split(asset_id)[-1]
        # GHS_BUILT_LDS1975_GLOBE_R2018A_54009_250_V2_0_12_3
        searchObj = re.search('\d+', product_id)
        year = int(searchObj.group()) #TODO: function as input
        print()
        # pprint(product_id)
        print("-----------------------------------------------------------------")
        print(year)

        os.system(f"earthengine asset set -p year={year} {asset_id}")


if __name__ == '__main__':
    gs_dir = "gs://sgd1131/WorldPop1k"
    folder = 'download_data/worldpop1km/'
    assetFolder = 'projects/gisproject-1/assets/World_POP_1km_unadj'
    model = UploadModel(gs_dir, folder, assetFolder=assetFolder, asset_type='collection')
    model.upload()










