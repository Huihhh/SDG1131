import ee
from .utils import setYear
class GPWv4:
    # resolution: 30 arc-second (927.67 meters), 2000, 2005, 2010, 2015, and 2020 
    name = 'GPWv4 30 arc-second'
    src = 'CIESIN/GPWv411/GPW_Population_Count'
    years = [2000, 2005, 2010, 2015, 2020]
    crs = 'EPSG:4326'
    # The two threshold 300 and 1500 is based on the pop count in a 1km * 1km cell. the scale will be multiplied by the threshold
    scale = 16
    popBand = 'population_count'
    visMin = 300
    visMax = 1500

    def __init__(self, cellTH=300, clusterTH=5000):
        self.cellTH = cellTH
        self.clusterTH = clusterTH
        self.data = ee.ImageCollection(self.src).map(setYear)
        self.scale = self.data.first().projection().nominalScale()

    def queryImageByYearAndROI(self, year, roi):
        return self.data.filter(ee.Filter.eq('year', year)).filterBounds(roi).first()