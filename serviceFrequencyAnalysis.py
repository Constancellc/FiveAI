import csv
import matplotlib.pyplot as plt
import scipy.ndimage.filters as fil
import numpy as np
import copy
import random

# there are bascially no comments in this script, i apologise..
i_time = []
o_time = []
with open('../time_distributions.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row == []:
            continue
        i_time.append(float(row[0]))
        o_time.append(float(row[1]))
takeUpRate = 0.5

capacity = 15
# only looking at service frequency on the way in to start with

rtes = ['pink2','blue2','red2','orange2','purple2']
plt.figure()
for rn in range(5):
    rte = rtes[rn]
    o = []
    d = []

    with open(rte+'OD.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) < 1:
                continue
            o.append(float(row[2]))#+0.1*random.random())
            d.append(float(row[3]))#+0.1*random.random())

    time2Next = []
    with open(rte+'DistTimes.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) < 1:
                continue
            time2Next.append(int(row[1]))
    time2Next.append(0)
    print(len(time2Next))
    print(len(o))
    def pickUp(t0,t1,sn):
        return o[sn]*sum(i_time[t0:t1])/sum(i_time)*takeUpRate
    def putDown(sn,num):
        return num*d[sn]/sum(d[sn:])

    lastPickUp = [0]*len(o)

    tStart = 6*60*60
    tEnd = 11*60*60


    plt.subplot(2,3,rn+1)
    plt.title(rte)

    for vehicleCapacity in [5,10,15]:

        y = []
        for frequency in range(10,120):
            t0 = copy.deepcopy(tStart)
            totalPassengers = 0
            c = 1
            while t0 < tEnd:
                t = copy.deepcopy(t0)
                nP = 0
                for sn in range(len(o)):
                    nP -=  putDown(sn,nP)
                    on_ = pickUp(lastPickUp[sn],int(t/60),sn)

                    if (nP+on_) < vehicleCapacity:
                        nP += on_
                        totalPassengers += on_
                    else:
                        totalPassengers += (vehicleCapacity-nP)
                        nP = vehicleCapacity
                        
                    lastPickUp[sn] = int(t/60)
                    t += time2Next[sn]    
                t0 += frequency*60
            y.append(totalPassengers)
        y = fil.gaussian_filter1d(y,10)
        plt.plot(range(10,120),y,label=str(vehicleCapacity)+' people capacity')
    plt.grid()
plt.legend()
plt.show()
