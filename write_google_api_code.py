import csv
import matplotlib.pyplot as plt
import numpy as np
import copy

stops = []
with open('orangeLatLong.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row == []:
            continue
        '''
        lat = float(row[2])
        lon = float(row[3])
        '''
        lat = float(row[4])
        lon = float(row[5])
        stops.append([lat,lon])

if len(stops) < 25:
    f = open('mapsAPI.txt','w')
    f.write('var wpts = [')
    for stop in stops[1:-1]:
        f.write('{location: {lat:'+str(stop[0])+', lng:'+str(stop[1])+
                '}, stopover: true},\n')
    f.write('];\n')

    f.write('var start = {lat:'+str(stops[0][0])+', lng:'+str(stops[0][1])+'};\n')
    f.write('var end = {lat:'+str(stops[-1][0])+', lng:'+str(stops[-1][1])+'};\n')
    f.close()

else:
    n = 0
    f = open('mapsAPI.txt','w')
    f.write('var start1 = {lat:'+str(stops[n][0])+', lng:'+str(stops[n][1])+'};\n')
    f.write('var wpts1 = [')
    n += 1
    while n < 23:
        f.write('{location: {lat:'+str(stops[n][0])+', lng:'+str(stops[n][1])+
                '}, stopover: true},\n')
        n += 1
    f.write('];\n')
    f.write('var end1 = {lat:'+str(stops[n][0])+', lng:'+str(stops[n][1])+'};\n')
    f.write('var start2 = {lat:'+str(stops[n][0])+', lng:'+str(stops[n][1])+'};\n')
    n += 1
    f.write('var wpts2 = [')
    while n < len(stops)-1:
        f.write('{location: {lat:'+str(stops[n][0])+', lng:'+str(stops[n][1])+
                '}, stopover: true},\n')
        n += 1
    f.write('];\n')
    f.write('var end2 = {lat:'+str(stops[n][0])+', lng:'+str(stops[n][1])+'};\n')
    
    
    f.close()    
