import ee

class WSF_evolution:
    # resolution: 30m
    # crs: EPSG:4326
    src = 'projects/gisproject-1/assets/WSF_evolution'
    name = 'WSF evolution 30m'
    years = [i for i in range(2015, 1984, -1)] 
    cities = ['Beijing', 'Heidelberg', 'Nairobi', 'LaPaz', 'RioDeJaneiro', 'Nouakchott', 'Detroit', 'MexicoCity', 'NewYork', 'Mumbai', 'Guangzhou', 'Lagos', 'Cairo', 'Stockholm', 'Kigali', 'DarEsSalaam', 'Dubai', 'Shanghai', 'Charleston', 'Sydney']
    bandName = 'b1'
    resolution = 30

    def __init__(self, *args, **kwargs):
        self.visParam = {'opacity': 0.4, 'palette': ['green']}
        self.data = ee.ImageCollection(self.src)
    

    def queryImageByYearAndROI(self, year, roi):
        img = self.data.filterBounds(roi).mosaic()
        img = img.select('b1').lte(year).And(img.select('b1').gt(0))
        return img.selfMask()
