import ee
class WSF1519:
    # resolution: 30m
    # crs: EPSG:4326
    src19 = 'projects/gisproject-1/assets/WSF2019'
    src15 = 'DLR/WSF/WSF2015/v1'
    name = 'WSF2015 10m & WSF2019 10m'
    years = [2015, 2019] 
    cities = ['Beijing', 'Heidelberg', 'Nairobi', 'LaPaz', 'RioDeJaneiro', 'Nouakchott', 'Detroit', 'MexicoCity', 'NewYork', 'Mumbai', 'Guangzhou', 'Lagos', 'Cairo', 'Stockholm', 'Kigali', 'DarEsSalaam', 'Dubai', 'Shanghai', 'Charleston', 'Sydney']
    bandName = 'year'
    resolution = 10

    def __init__(self, *args, **kwargs):
        self.visParam = {'opacity': 0.4, 'palette': ['green']}
        self.data = ee.Image(self.src19)
    

    def queryImageByYearAndROI(self, year, roi):
        if year == 2015:
            img = ee.Image(self.src15).clip(roi).select('settlement').gt(0) #TODO: add a check after clip
        elif year == 2019:
            img = ee.ImageCollection(self.src19).filterBounds(roi).first()\
                        .select('b1').gt(0).selfMask()
        else: 
            raise Exception(f'{year} not available in WSF 2015 & 2019')
        return img