import ee
class GAIA:
    name = 'GAIA 10m'
    src = 'Tsinghua/FROM-GLC/GAIA/v10'
    years = [i for i in range(2018, 1984, -1)]
    crs = 'EPSG:4326'
    bandName = 'change_year_index'
    resolution = 30

    def __init__(self, *args, **kwargs):
        self.visParam = {'opacity': 0.4, 'bands': ['change_year_index'], 'palette': ['red']}

    @classmethod
    def queryImageByYearAndROI(cls, year, roi):
        return ee.Image(cls.src).clip(roi).gte(ee.Number(cls.years.index(year)).add(1))
