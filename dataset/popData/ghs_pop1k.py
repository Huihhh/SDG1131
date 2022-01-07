import ee
from .utils import setYear
class GHSpop1k:
    # resolution: 1km
    name = 'GHS-Pop 1km'
    src = 'projects/gisproject-1/assets/GHS_POP_1km' #'users/omegazhanghui/GHS_POP_1km'
    years = [1975, 1990, 2000, 2015]
    crs = 'EPSG:54009'
    # The two threshold 300 and 1500 is based on the pop count in a 1km * 1km cell. the scale will be multiplied by the threshold
    scale = 16
    popBand = 'b1'
    visMin = 300
    visMax = 1500

    def __init__(self, cellTH=300, clusterTH=5000):
        self.cellTH = cellTH
        self.clusterTH = clusterTH
        # def addYearProp_and_renamePopBand(img):
        #     return ee.Image(img.setMulti({'year': ee.String(img.get('system:index')).slice(9, 13)})) \
        #                         .select('b1') \
        #                         .rename('population_count')

        # def addStartTimeProp(img):
        #     return img.setMulti({
        #         'system:time_start': ee.Date(img.get('year')).millis()
        #         })
        self.data = ee.ImageCollection(self.src)#.map(addYearProp_and_renamePopBand) \
                #    .map(addStartTimeProp)