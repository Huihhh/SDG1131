import ee
from .utils import setYear
class GHSpop250:
    # resolution: 250m 'EPSG:54009'
    name = 'GHS-Pop 250m'
    src = 'JRC/GHSL/P2016/POP_GPW_GLOBE_V1'
    years = [2015, 2000, 1990, 1975]
    crs = 'EPSG:54009'
    # The two threshold 300 and 1500 is based on the pop count in a 1km * 1km cell. the scale will be multiplied by the threshold
    scale = 1 
    popBand = 'population_count'
    visMin = 18.75
    visMax = 93.75

    def __init__(self):
        self.data = ee.ImageCollection(self.src).map(setYear)