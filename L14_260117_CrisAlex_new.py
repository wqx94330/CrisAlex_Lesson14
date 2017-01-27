##Team CrisAlex
##Exercise 14
##26/01/2017

from twython import Twython
import json
import os
import datetime 
import subprocess 
from osgeo import ogr, osr

#Enter Twitter API Key information
consumer_key = 'HUtvTq5kBciJoEeSYr7qPbLPP'
consumer_secret = 'G1oH4WodLtD8Aurl3wFf7IK6fBlxOwWsfUhnv3fJrzTH7ckUp3'
access_token = '824530811710042112-19iZJdnfUOo8O1di5e35hASVLS9c4ML'
access_secret = 'vifY6wDrRwOwVyxwEYNa7DiAXv8S1HXSUbDTF4g8v9wuh'

#Key factors of locating Amsterdam and the neighbourhood
lat = 52.3702
lon = 4.8952  
rad = 60
query = "amsterdam"

##Initiate Twython object and save to a .csv format file 
twitter = Twython(consumer_key, consumer_secret, access_token, access_secret)
search_results = twitter.search(q = query, geocode = "%f,%f,%dkm" % (lat, lon, rad), count = 200)
for results in search_results['statuses']:
    print results
data = search_results["statuses"]
output_file = 'amsterdam.csv'
ams_coordinates=[]
target = open(output_file, 'w')
target.write('\n')
for tweet in data:
    x = 0
    y = 0    
    user =  tweet['user']['screen_name']
    content = tweet['text']
    if tweet['place'] != None:
        location_name = tweet['place']['full_name']
        location_type =  tweet['place']['place_type']    
    coordinates = tweet['coordinates'] 
    if not coordinates is None:
       lon_tweet = coordinates['coordinates'][0]
       lat_tweet = coordinates['coordinates'][1]
       coordinates= (lon_tweet,lat_tweet)
       ams_coordinates.append(coordinates)
       x = str(lon_tweet)
       y = str(lat_tweet)
    Tweet_info_String = '%s, %s, %s'%(user,x,y)
    target = open(output_file, 'a')
    target.write(Tweet_info_String) 
    target.write('\n')
    target.close()
    
#Create the shapefile to be added with the basemap in QGIS
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName(driverName)
fn = "Amsterdam_tweet.shp"
ds = drv.CreateDataSource(fn)

if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName   

layername = "Amsterdam_tweet"
amsterdam_shp = "Amsterdam_tweet.shp" 
amsterdam_csv  = open('amsterdam.csv', 'r')
datasrc = drv.CreateDataSource(amsterdam_shp) 
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
layer = ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)

for i in ams_coordinates:
    point = ogr.Geometry(ogr.wkbPoint)
    point.SetPoint(0,i[0],i[1]) 
    layerDefinition = layer.GetLayerDefn()
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(point)
    layer.CreateFeature(feature)  
ds.Destroy()






