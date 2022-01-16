import ee
class GHSbp38:
    name = 'GHS-Built 38m'
    src = 'JRC/GHSL/P2016/BUILT_LDSMT_GLOBE_V1'
    years = [1975, 1990, 2000, 2015]
    crs = 'EPSG:3857'
    bandName = 'built'
    resolution = 38
    
    def __init__(self, *args, **kwargs):
        self.scale = ee.Image(self.src).select('built').projection().nominalScale()
        self.visParam = {'opacity': 0.4, 'bands': ['built'], 'palette': ['#0074D9']}
    
    @classmethod
    def queryImageByYearAndROI(cls, year, roi):
        bpData = ee.Image(cls.src).clip(roi)
        return bpData.select('built').gt(ee.Number(cls.years[::-1].index(year)).add(2)).selfMask()
