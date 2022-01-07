import ee

def setYear(img):
  return img.setMulti({'year': ee.Number.parse(img.date().format().slice(0,4))})

def insertNewImagePoP(popdataset,datasetnum):
  # fit the data
  def createTimeBand(image):
  # Scale milliseconds by a large constant to avoid very small slopes
  # in the linear regression output.
     return image.addBands(image.metadata('system:time_start').divide(1e12))
  
  popdataset1 = popdataset.filter(ee.Filter.inList('year', ['2000','2005','2010','2015'])).map(createTimeBand)
  # Map the time band function over the collection.
  # Reduce the collection with the linear fit reducer.
  # Independent variable are followed by dependent variables.
  linearFit = popdataset1.select(['system:time_start','population_count']).reduce(ee.Reducer.linearFit())
  #create new image
  newmap1990 = popdataset.filter(ee.Filter.eq('year', '2015')).first() \
                         .addBands(linearFit.select('scale').multiply(631152000000).divide(1e12).add(linearFit.select('offset')))
  newmap1990 = newmap1990.select('scale').rename(['population_count']).setMulti({'year': '1990'})
  newmap2010 = popdataset.filter(ee.Filter.eq('year', '2015')).first() \
                         .addBands(linearFit.select('scale').multiply(1262304000000).divide(1e12).add(linearFit.select('offset')))
  newmap2010 = newmap2010.select('scale').rename(['population_count']).setMulti({'year': '2010'})
  newmap2016 = popdataset.filter(ee.Filter.eq('year', '2015')).first() \
                         .addBands(linearFit.select('scale').multiply(1451606400000).divide(1e12).add(linearFit.select('offset')))
  newmap2016 = newmap2016.select('scale').rename(['population_count']).setMulti({'year': '2016'})
  newmap2018 = popdataset.filter(ee.Filter.eq('year', '2015')).first() \
                         .addBands(linearFit.select('scale').multiply(1514764800000).divide(1e12).add(linearFit.select('offset')))
  newmap2018 = newmap2018.select('scale').rename(['population_count']).setMulti({'year': '2018'})
  newmap2020 = popdataset.filter(ee.Filter.eq('year', '2015')).first() \
                         .addBands(linearFit.select('scale').multiply(1577836800000).divide(1e12).add(linearFit.select('offset')))
  newmap2020 = newmap2020.select('scale').rename(['population_count']).setMulti({'year': '2020'})
  popdataset = popdataset.select(['population_count'])
  popdataset = popdataset.merge(ee.ImageCollection([newmap2016,newmap2018]))
  if datasetnum == 1:
    return popdataset.merge(ee.ImageCollection([newmap2010,newmap2020]))
  elif datasetnum == 2:
    return popdataset.merge(ee.ImageCollection([newmap2010,newmap2020]))
  else:
    return popdataset.merge(ee.ImageCollection([newmap1990]))
  return popdataset