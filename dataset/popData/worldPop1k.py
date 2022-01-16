import ee
from .utils import setYear
class WorldPop1k:
    # resolution: 1km, coverage: Chinese cities
    name = 'WorldPop 1km'
    src = 'projects/gisproject-1/assets/World_POP_1km_unadj' #'users/omegazhanghui/WorldPop1k'
    years = [2000, 2005 ,2010, 2015, 2019]
    # cities = ['Beijing', 'Shanghai', 'Tianjin', 'Guangzhou']
    crs = 'EPSG:54009'
    # The two threshold 300 and 1500 is based on the pop count in a 1km * 1km cell. the scale will be multiplied by the threshold
    scale = 16
    popBand = 'b1'
    visMin = 300
    visMax = 1500
    
    def __init__(self, cellTH=300, clusterTH=5000):
        self.cellTH = cellTH
        self.clusterTH = clusterTH
        self.data = ee.ImageCollection(self.src)#.map(renamePopBand)
        self.scale = self.data.first().projection().nominalScale()

    def queryImageByYearAndROI(self, year, roi):
        return self.data.filter(ee.Filter.eq('year', year)).filterBounds(roi).first()