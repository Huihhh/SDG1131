import ee
from collections import defaultdict

def computeAreaFromPoly(poly):
    polyFeatCol = ee.FeatureCollection([poly])
    img = polyFeatCol.style(**{'color':'white', 'fillColor':'white', 'width':0}) \
                .select('vis-red').gt(0).rename('poly')
    areaHa = img.multiply(ee.Image.pixelArea()).divide(1000000)
    stats = areaHa.reduceRegion(**{
        'reducer': ee.Reducer.sum(),
        'geometry': poly.geometry(),
        'scale': 1000,
        # // maxPixels: 86062013,
        'crs': 'EPSG:4326'
    })
    return poly.setMulti({'area': ee.Number(stats.values().get(0)).round()})


def fill_holes(img, roi):

    distance = img.fastDistanceTransform(20).lt(5)
    #   // distance = img.fastDistanceTransform(256).sqrt().lt(50)
    distance = distance.mask(distance)
    poly_image = distance.reduce(ee.Reducer.anyNonZero())
    poly = poly_image.reduceToVectors(**{
    # // reducer: ee.Reducer.anyNonZero(),
    'geometry': roi,
    'scale': 1000,
    'bestEffort': True,
    'tileScale': 8
    })
    return poly

def get_admin(drawROI, cityName, center, adminLevel):
    admin = ee.FeatureCollection('FAO/GAUL/2015/level' + str(adminLevel)).filterBounds(center)
    adminName = get_city_name(admin).getInfo()

    name = adminName if drawROI else cityName
    if 'Detroit' in name:
        admin = ee.FeatureCollection("projects/gisproject-1/assets/Detroit_admin")
    if 'Sydney' in name:
        admin = ee.FeatureCollection("projects/gisproject-1/assets/Sydney_admin")
    return admin, adminName



def get_city_name(adminBound):
    firstAdm = adminBound.first()
    adm2Name = ee.Algorithms.If(firstAdm.get('ADM2_NAME'), ee.String(firstAdm.get('ADM2_NAME')).cat('/'), ee.String(''))
    return ee.String(adm2Name) \
            .cat(firstAdm.get('ADM1_NAME'))\
            .cat('/')\
            .cat(firstAdm.get('ADM0_NAME'))\


def update_city(name, cityCfg, useAdmin):
    if useAdmin:
        cityCoords = ee.Geometry.MultiPoint(cityCfg['coords'])
        if name == 'Detroit':
            city = ee.FeatureCollection("projects/gisproject-1/assets/Detroit_admin")
        elif name == 'Sydney':
            city = ee.FeatureCollection("projects/gisproject-1/assets/Sydney_admin")
        else:
            city = ee.FeatureCollection('FAO/GAUL/2015/level' + str(cityCfg['adminLevel'])) \
                .filterBounds(cityCoords)
        city = city.union().geometry()
        cityBounds = city.bounds()
        return city, cityCoords, cityBounds
    
    return cityCfg, cityCfg.centroid(), cityCfg.bounds()        
    

def queryBaseImg(roi, year):
    def l2BandRename(img): return img.select(['B4', 'B5', 'B7']).rename(['NIR', 'G', 'R'])
    def l5BandRename(img): return img.select(['B1','B2', 'B3', 'B4', 'B5', 'B7']).rename(targetBands)
    def l8BandRename(img): return img.select(['B2','B3', 'B4', 'B5', 'B6', 'B7']).rename(targetBands)
    def S2BandRename(img): return img.select(['B2','B3', 'B4', 'B8', 'B11', 'B12']).rename(targetBands)
    year_start = ee.Date(str(year) + '-06-01')
    year_end = year_start.advance(4, 'month')
    targetBands = ['B', 'G', 'R', 'NIR', 'SWIR1', 'SWIR2']

    if (year >= 1975 and year <= 1982):
        vmin = 0.01915
        vmax = 0.19556
        L2 = ee.ImageCollection("LANDSAT/LM02/C01/T1") #1975-1982
        imgCol = L2.filterBounds(roi).filterDate(year_start, year_end) \
                    .map(l2BandRename).filter(ee.Filter.lt("CLOUD_COVER_LAND", 36)) 
    elif (year >= 1984 and year <= 2012):
        vmin = 0.01915
        vmax = 0.19556
        L5 = ee.ImageCollection("LANDSAT/LT05/C01/T1_TOA") #1984-2012-05  
        imgCol = L5.filterBounds(roi).filterDate(year_start, year_end) \
                    .map(l5BandRename).filter(ee.Filter.lt("CLOUD_COVER_LAND", 36))
    elif (year >= 2013 and year <=2015):
        vmin = 0.05158
        vmax = 0.27996
        L8 = ee.ImageCollection("LANDSAT/LC08/C01/T1_TOA") # 2013-2021  
        imgCol = L8.filterBounds(roi).filterDate(year_start, year_end) \
                    .map(l8BandRename).filter(ee.Filter.lt("CLOUD_COVER_LAND", 36))
    else:
        vmin = -123.111
        vmax = 2141.467
        S2 = ee.ImageCollection("COPERNICUS/S2") # 2015-2021  
        imgCol = S2.filterBounds(roi).filterDate(year_start, year_end) \
                    .map(S2BandRename).filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 36))
    
    medianImg = imgCol.median().clip(roi)
    return medianImg, vmin, vmax

def get_pop_img(popData, cityCoords, cityBounds, year):
    return popData.data.filter(ee.Filter.eq("year", year)) \
                            .filterBounds(cityCoords) \
                            .first() \
                            .clip(cityBounds)


def define_city(pop4def, year, cityCoords, city, useAdmin):
    popRaster_raw = pop4def.data \
                            .filter(ee.Filter.eq("year", year)) \
                            .filterBounds(cityCoords) \
                            .first() \
                            .clip(city)
    #*************************************** Urban cluster **********************************************************#
    # filter out cells with pop counts smaller than 300 (1km) / 18.75 (250m)
    uCluster_th = int(pop4def.cellTH)
    popRasterMask = popRaster_raw.gt(uCluster_th).selfMask()

    urbanCluster = popRasterMask.reduceToVectors(**{
                'geometry': city,
                'scale': 1000,
                'geometryType': 'polygon',
                'maxPixels': 1e8,
                'geometryInNativeProjection': True,
                'eightConnected': True,
                # 'crs': popRaster_raw.projection().getInfo()
            })
    clusterCountsRaster = popRaster_raw.multiply(popRasterMask)
    urbanCluster_poly = clusterCountsRaster.reduceRegions(**{
        'collection': urbanCluster,
        'reducer': ee.Reducer.sum(),
        'scale': 1000,
        # 'crs': 'EPSG:4326',
            # filter out small clusters with a total pop counts less than 5000 \
        }).filter(ee.Filter.gt('sum', int(pop4def.clusterTH)))#.map(computeAreaFromPoly) \
        # .sort('area', False) \
        # .first()
        # .filter(ee.Filter.gt('area', 60))
        # .union(**{'maxError': 10})

    # ========================= get city definition polygon =======================
    if type(urbanCluster_poly) == ee.element.Element:
        urbanCluster_poly = ee.FeatureCollection([urbanCluster_poly])
    zoneCluster = urbanCluster_poly.reduceToImage(**{
        'properties': ['sum'],
        'reducer': ee.Reducer.first(),
        })
    urbanCluster_poly = fill_holes(zoneCluster, city)#.geometry()
    if not useAdmin:
        urbanCluster_poly = ee.FeatureCollection([urbanCluster_poly.geometry().buffer(-1000)])

    return urbanCluster_poly

def computePop(popData, year, cityBoundary):
    return popData.data.filter(ee.Filter.eq("year", year)) \
                    .filterBounds(cityBoundary) \
                    .first() \
                    .clip(cityBoundary) \
                    .reduceRegion(**{'reducer':ee.Reducer.sum(),
                        'geometry':cityBoundary,
                        # 'scale': 100,
                        'maxPixels': 1e8,}).get(popData.popBand)
                        # 'crs': self.popData.projection()}) \


def computeArea(bpData, year, cityBoundary):
    builtupImg = bpData.queryImageByYearAndROI(year, cityBoundary) # builtup is a 0-1 mask
    area = builtupImg.clip(cityBoundary) \
                .multiply(ee.Image.pixelArea()).divide(1e6)
    stats = area.reduceRegion(**{
        'reducer': ee.Reducer.sum(),
        'geometry': cityBoundary,
        'maxPixels': 1e12,
        'scale': bpData.resolution,
        # 'crs': self.bpData.crs if self.bpData.name == 'GHS 250' else None,
        # 'scale': 250 if self.bpData.name == 'GHS 250' else None
    })
    return ee.Number(stats.values().get(0))

def computeRate(startYear, endYear, valueStartYear, valueEndYear):
    return ee.Number(valueEndYear).log() \
                    .subtract(ee.Number(valueStartYear).log()) \
                    .divide(endYear - startYear)

def computeSDG(bpData, popData, startYear, endYear, cityDef):
    popStartYear = ee.Number(computePop(popData, startYear, cityDef))
    popEndYear = ee.Number(computePop(popData, endYear, cityDef))

    bpStartYear = computeArea(bpData, startYear, cityDef)
    bpEndYear = computeArea(bpData, endYear, cityDef)

    popGrowthRate = computeRate(startYear, endYear, popStartYear, popEndYear)
    landComRate = computeRate(startYear, endYear, bpStartYear, bpEndYear)
    # total built-up area in the urban area in time t (in square meters) / the population in the urban area in time t
    # m^2/person
    LCPCStartYear = ee.Number(bpStartYear).multiply(1e6).divide(ee.Number(popStartYear))
    LCPCEndYear = ee.Number(bpEndYear).multiply(1e6).divide(ee.Number(popEndYear))

    TotalChangeInBuiltUp = ee.Number(bpEndYear).subtract(ee.Number(bpStartYear)).divide(ee.Number(bpStartYear))
    sdg = landComRate.divide(popGrowthRate)
    return ee.List([sdg, LCPCStartYear, LCPCEndYear, TotalChangeInBuiltUp, bpStartYear, bpEndYear, popStartYear, popEndYear, landComRate, popGrowthRate])



class Model:
    def __init__(self, popData=None, bpData=None, pop4def=None, startYear=None, endYear=None, useAdmin=True):
        self.cityDef = defaultdict()
        self.popRaster = defaultdict()
        self.bpRaster = defaultdict()
        self.baseImg = defaultdict()
        self.popData = popData
        self.pop4def = pop4def # popData for city definition
        self.bpData = bpData
        self.startYear = startYear
        self.endYear = endYear
        self.citymask = defaultdict()
        self.useAdmin = useAdmin
        # get the city admin boundary as ROI
        # self.update_city(name, cityCfg)
    



                        



