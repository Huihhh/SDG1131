import ee
import os
key = os.environ['PRIVATE_KEY']
service_account = os.environ.get('SERVICE_ACCOUNT')
credentials = ee.ServiceAccountCredentials(service_account, key_data=key)
