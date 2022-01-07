import ee
from .utils import setYear
class SCBpop:
    # resolution: 250m 'EPSG:54009'
    name = 'SCB-Pop'
    src = 'JRC/GHSL/P2016/POP_GPW_GLOBE_V1' 
    years = [2015, 2000, 1990, 1975]
    # crs = 'EPSG:54009'
    popBand = 'population_count'
    visMin = 18.75
    visMax = 93.75

    def __init__(self):
        self.data = ee.ImageCollection(self.src).map(setYear) # <<<================= add a 'year' property for each image