import ee
class GHSbp30:
    name = 'GHS-Built 30m'
    src = 'projects/gisproject-1/assets/GHS_Built30m'
    years = [1975, 1990, 2000, 2015]
    crs = 'EPSG:3857'
    bandName = 'b1'
    
    def __init__(self, *args, **kwargs):
        self.scale = ee.ImageCollection(self.src).first().projection().nominalScale()
        self.visParam = {'opacity': 0.4, 'bands': ['b1'], 'palette': ['#0074D9']}
    
    @classmethod
    def queryImageByYearAndROI(cls, year, roi):
        bpData = ee.ImageCollection(cls.src).filterBounds(roi).mosaic()
        return bpData.select('b1').gt(ee.Number(cls.years[::-1].index(year)).add(2)).selfMask()
