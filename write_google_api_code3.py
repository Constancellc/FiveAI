import csv
import matplotlib.pyplot as plt
import numpy as np
import copy
import random
'''
# first pre-procesing all stops
stops = {}
with open('bus-stops.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) < 2:
            continue
        code = row[0]
        e = int(row[4])
        n = int(row[5])
        if (e < 527500) or (e > 547500):
            continue
        if (n < 156000) or (n > 172000):
            continue
        stops[code] = [e,n]

f = open('cromley-bus-stops.txt','w')
for code in stops:
    f.write(code+','+str(stops[code][0])+','+str(stops[code][1])+'\n')
f.close()
'''

chsn = []
f = open('mapsAPI.txt','w')

pink_start = [51.298761, -0.11549768]
pink_7 = [51.313105,-0.13464017]
pink_13 = [51.322285,-0.13626267]
pink_end = [51.340185,-0.11738861]

orange_start = [51.355801,0.10377777]
orange_9 = [51.363314,0.081884558]
orange_20 = [51.389993,0.034498167]
orange_end = [51.408797,-0.0243993]

red_start = [51.321321,-0.090375963]
red_9 = [51.338681,-0.11835475]
red_16 = [51.361245,-0.11786109]
red_end = [51.381272,-0.11344696]

purple_start = [51.376349,-0.017879250]
purple_9 = [51.370141,0.0023834700]
purple_21 = [51.360133,0.065020228]
purple_end = [51.344050,0.11110847]

blue_start = [51.379169,-0.10016941]
blue_15 = [51.374264,-0.051174961]
blue_23 = [51.375983,-0.015926486]
blue_end = [51.397177,0.014762691]


pink2_start = [51.300307,-0.11381333]
pink2_7 = [51.305711,-0.11430913]
pink2_17 = [51.319457,-0.14731290]
pink2_end = [51.340185,-0.11738861]

orange2_start = [51.357988,0.10917818]
orange2_10 = [51.361682,0.071525315]
orange2_18 = [51.389993,0.034498167]
orange2_end = [51.408666,-0.024635018]

blue2_start = [51.372914,-0.044651702]
blue2_8 = [51.377328,-0.022061594]
blue2_17 = [51.380912,0.0046211456]
blue2_end = [51.404800,0.018634735]

purple2_start = [51.375983,-0.015926486]
purple2_8 = [51.367207,0.046776979]
purple2_12 = [51.361817,0.071517044]
purple2_end = [51.344050,0.11110847]

red2_start = [51.315439,-0.087563678]
red2_6 = [51.330563,-0.10901204]
red2_14 = [51.353439,-0.10616012]
red2_end = [51.387485,-0.12628478]


start = orange_start
stops = []
with open('cromley-bus-stops.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if row == []:
            continue
        stops.append([float(row[4]),float(row[5]),row[0]])

np.random.shuffle(stops)

latLongs = []

for s in stops: 
    latLong = str(int(s[0]*50))+str(int(s[1]*50))
    d = np.sqrt(np.power(s[0]-start[0],2)+np.power(s[1]-start[1],2))
    ran = 1
    if d < 0.05:
        ran = random.random()
    if (latLong in latLongs) and ran > 0.25:
        continue
    latLongs.append(latLong)
    chsn.append(s[2])
    f.write('var SC'+s[2]+' = {lat:'+str(s[0])+',lng:'+str(s[1])+'};\n')

f.write('var markers = [')
for row in chsn[:-1]:
    f.write('SC'+row+', ')
f.write('SC'+chsn[-1]+'];\n')

f.close()
