import ee
class GHS_S2:
    name = 'GHS-Built-S2 10m'
    src = 'projects/gisproject-1/assets/GHS_BUILT_S2_2018_GLOBE_R2020A' #'users/omegazhanghui/GHS_BUILT_S2_2018_GLOBE_R2020A_tile_schema'
    years = [2018]
    crs = 'EPSG:4326'
    bandName = 'built'
    resolution = 10

    def __init__(self, *args, **kwargs):
        self.scale = ee.FeatureCollection(self.src).first().projection().nominalScale()
        self.visParam = {'opacity': 0.3, 'bands': ['built'], 'palette': ['grey']}

    @classmethod
    def queryImageByYearAndROI(cls, year, roi):
        intersects = ee.FeatureCollection(cls.src).filterBounds(roi)
        
        def func_ovr(el):
            return el.setMulti({"url": ee.String("gs://wildfire_unet/GHS_Built_S2/") \
                                    .cat(el.get("grid_zone")).cat("_PROB.tif")})
        intersects = intersects.map(func_ovr)

        url_list = intersects.aggregate_array("url")
        builtUpImgList = ee.List([])

        def add_img(url, builtUpImgList):
            img = ee.Image.loadGeoTIFF(url)
            return ee.List(builtUpImgList).add(img)
        
        builtUpImgList = ee.List(url_list.iterate(add_img, builtUpImgList))
        builtUpImgCol = ee.ImageCollection(builtUpImgList)
        return builtUpImgCol.mosaic().clip(roi).gt(0)