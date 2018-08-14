import csv
import numpy as np
import matplotlib.pyplot as plt
# i think this is actually merging into a more complex version of get passengers

def p_willing(d):
    if d < 1:
        return 1.0
    elif d < 5:
        return 0.7
    elif d < 10:
        return 0.5
    elif d < 15:
        return 0.3
    elif d < 20:
        return 0.15
    elif d < 30:
        return 0.1
    else:
        return 0.0

clrs = ['purple','orange','blue','red','pink']
plt.figure()
for cn in range(5):
    clr = clrs[cn]

    stops = []
    with open(clr+'LatLong.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        n = 1
        for row in reader:
            if row == []:
                continue
            lat = float(row[4])
            lon = float(row[5])
            stops.append([n,lat,lon])
            n += 1

    lsoa = {}
    with open('../cromley_lsoa_cetroids.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row == []:
                continue
            lsoa[row[0]] = [float(row[2]),float(row[1])]

    closest = {}
    for l in lsoa:
        cent = lsoa[l]
        closest[l] = [None,30]
        for stop in stops:
            d = np.sqrt(np.power(cent[0]-stop[1],2)+np.power(cent[1]-stop[2],2))
            d = d*111248/50 # m-> moins walk 
            if d > closest[l][1]:
                continue
            closest[l] = [stop[0],d]
            
    targeted = []
    for l in closest:
        if closest[l] != [None,30]:
            targeted.append(l)

    passengers = [[0]*len(stops),[0]*len(stops)]
    files = ['../commutes_ordered_total.csv','../commutes_ordered.csv']

    for fn in range(2):
        with open(files[fn],'rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if row == []:
                    continue
                n = int(row[0])
                orig = row[1]
                dest = row[2]
                if orig not in targeted:
                    continue
                if dest not in targeted:
                    continue
                start = closest[orig]
                end = closest[dest]

                if start[0] > end[0]: # if going in wrong direction
                    continue

                av_walk = start[1]+end[1]
                p = p_willing(av_walk)

                n_passengers = round(p*n,0)

                if n_passengers == 0:
                    continue
                
                for i in range(start[0],end[0]):
                    passengers[fn][i] += n_passengers
                
    plt.subplot(2,3,cn+1)
    plt.title(clr)
    plt.plot(passengers[0],label='total')
    plt.plot(passengers[1],label='car drivers')
    plt.xlim(0,len(stops)-1)
    plt.grid()
    plt.ylim(0,180)
    if cn in [0,3]:
        plt.ylabel('potential passengers')
    if cn in [3,4]:
        plt.xlabel('stop #')
    if cn == 0:
        plt.legend()

    with open(clr+'PotentialPassengers.csv','w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Lat','Long','#total','#cars'])
        for sn in range(len(stops)):
            writer.writerow(stops[sn][1:]+[passengers[0][sn],passengers[1][sn]])

plt.tight_layout()
plt.show()
    
