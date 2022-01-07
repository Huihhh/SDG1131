import ee
class GHSbp250:
    name = 'GHS-Built 250m'
    src = 'projects/gisproject-1/assets/GHS_BP250m' #'users/omegazhanghui/GHS_BP250'
    bandName = 'b1'
    years = [1975, 1990, 2000, 2015]
    resolution = 250
    

    def __init__(self, th=40, crs='EPSG:4326'):
        self.crs = crs
        self.th = th
        self.visParam = {'opacity': 0.5, 'bands': ["b1"], 'palette': ['#ff9933']}
    
    def queryImageByYearAndROI(self, year, roi):
        self.userData = ee.ImageCollection(self.src)
        return self.userData.filterBounds(roi).filter(ee.Filter.eq('year', year)) \
                .mosaic().clip(roi) \
                .gt(self.th).selfMask()