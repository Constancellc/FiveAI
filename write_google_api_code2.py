import csv
import matplotlib.pyplot as plt
import numpy as np
import copy


clrs = ['red','pink','purple','orange','blue']
ods = {}
for clr in clrs:
    stops = []
    with open(clr+'LatLong.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row == []:
                continue
            lat = float(row[4])
            lon = float(row[5])
            stops.append([lat,lon])
    ods[clr] = [stops[0],stops[-1]]

f = open('mapsAPI.txt','w')
for clr in ods:
    f.write('var '+clr+'_start = {lat:'+str(ods[clr][0][0])+', lng:'+
            str(ods[clr][0][1])+'};\n')
    f.write('var '+clr+'_end = {lat:'+str(ods[clr][1][0])+', lng:'+
            str(ods[clr][1][1])+'};\n')
f.write('var depot = {lat:51.372639, lng:-0.124805};\n')
f.write('var all = [')
for clr in ods:
    f.write(clr+'_start, ')
f.write('depot];\n')
f.write('var names = [')
for clr in ods:
    f.write('"start of '+clr+'", ')
f.write('"depot"];\n')

f.close()
