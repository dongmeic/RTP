import json
from urllib.request import urlopen
import arcpy
from arcpy import env
import os

path = r'T:\MPO\RTP\FY20 2045 Update\Data and Resources\Facility'
arcpy.env.workspace = os.path.join(path, 'Facility.gdb')
arcpy.env.overwriteOutput = True

# function to convert json from url to features
def json2shp(url_string, filename):
    response = urlopen(url_string)
    data = response.read()
    txt_str = data.decode('utf-8')
    lines = txt_str.split("\r\n")
    file = path + '/' + filename + '.json'
    fx = open(file, "w")
    for line in lines:
        fx.write(line+ "\n")
    fx.close()
    arcpy.JSONToFeatures_conversion(file, filename)