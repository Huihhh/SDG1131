import ee
from .utils import setYear
class WorldPop100:
    # data source: https://www.worldpop.org/project/categories?id=3
    # resolution: 100m, 2000-2020 yearly
    name = 'WorldPop 100m'
    src = 'projects/gisproject-1/assets/World_POP_100m' #'users/omegazhanghui/WorldPop100m'
    years = [2000, 2015, 2019]
    cites = ['Beijing', ]
    crs = 'EPSG:54009'
    # The two threshold 300 and 1500 is based on the pop count in a 1km * 1km cell. the scale will be multiplied by the threshold
    scale = 16
    popBand = 'b1'
    visMin = 3
    visMax = 15

    def __init__(self, cellTH=300, clusterTH=5000):
        self.cellTH = cellTH
        self.clusterTH = clusterTH

        # def renamePopBand(img):
        #     return ee.Image(img)).select('b1') \
        #                         .rename('population_count')

        # def addStartTimeProp(img):
        #     return img.setMulti({
        #         'system:time_start': ee.Date(img.get('year')).millis()
        #         })
        self.data = ee.ImageCollection(self.src)#.map(renamePopBand)