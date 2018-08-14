import csv
import matplotlib.pyplot as plt
import numpy as np
import copy
import random

# first get all stops and store the ones within the bromley area
stops = {}
with open('bus-stops.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) <= 1:
            continue
        code = row[0]
        east = int(row[4])
        if east < 528000 or east > 548000:
            continue
        north = int(row[5])
        if north < 157000 or north > 171000:
            continue
        stops[code] = [east,north]

routes = {}
with open('bus-sequences.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) <= 1:
            continue
        sCode = row[3]
        if sCode not in stops:
            continue
        rCode = row[0]+'-'+row[1]
        if rCode not in routes:
            routes[rCode] = []
        routes[rCode].append(sCode)

# now let's get our route to compare, i think I've done this before somewhere...
cs = ['r','c','g','b','y','m']
c = 0
      
plt.figure()
img = plt.imread("back.png")
fig, ax = plt.subplots()
plt.xlim(527500,547500)
plt.ylim(156000,172000)
ax.imshow(img, extent=[527500, 547500, 156000, 172000])
for rCode in routes:
    x = []
    y = []
    offset = 200*random.random()-100
    if c == 6:
        c = 0
    for sCode in routes[rCode]:
        x.append(stops[sCode][0]+offset)
        y.append(stops[sCode][1]+offset)
    ax.plot(x,y,lw=1.0,alpha=0.9,c='b')#,c=cs[c])
    c += 1


for clr in ['pink','red','blue','orange','purple']:
    e = []
    n = []
    with open(clr+'LatLong.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row == []:
                continue
            e.append(int(row[0]))
            n.append(int(row[1]))
            
    ax.plot(e,n,lw=5,alpha=0.4,c='r')

plt.show()
