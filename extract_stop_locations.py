import csv
import matplotlib.pyplot as plt
import numpy as np
import copy

stops = {}
with open('bus-stops.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) <= 1:
            continue
        code = row[0]
        east = int(row[4])
        north = int(row[5])
        stops[code] = [east,north]

clrs = ['red','purple','blue','orange','pink']

for clr in clrs:
    print(clr)
    data = []
    with open(clr+'_stops.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        n = 1
        for row in reader:
            if row == []:
                continue
            data.append(stops[row[0]]+[n])
            n += 1

    with open(clr+'EasNor.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Easting','Northing','n'])
        for row in data:
            writer.writerow(row)
        
# lets visualise
x = []
y = []

with open('blueEasNor.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row == []:
                continue
            x.append(int(row[0]))
            y.append(int(row[1]))

plt.figure()
plt.plot(x,y)
plt.show()
