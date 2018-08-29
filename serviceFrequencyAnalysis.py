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

takeUpRates = [1,0.5,0.25]
clrs = {4:'b',6:'r',8:'g'}

capacity = 15
# only looking at service frequency on the way in to start with

#rtes = ['pink','blue','red','orange','purple']

rtes = ['pink2','blue2','red2','orange2','purple2']
plt.figure(figsize=(10,7))
for tn in range(3):
    takeUpRate = takeUpRates[tn]
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
        #with open(rte+'DistTimes.csv','rU') as csvfile:
        with open(rte+'_DistTimes.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                if len(row) < 1:
                    continue
                time2Next.append(int(row[1]))
        time2Next.append(0)
        def pickUp(t0,t1,sn):
            return o[sn]*sum(i_time[t0:t1])/sum(i_time)*takeUpRate
        def putDown(sn,num):
            if num == 0 or sum(d[sn:]) == 0:
                return num
            else:
                return num*d[sn]/sum(d[sn:])

        lastPickUp = [0]*len(o)

        tStart = 6*60*60
        tEnd = 11*60*60


        plt.subplot(2,3,rn+1)
        plt.title(rte)

        for vehicleCapacity in [4,6]:

            y = []
            for frequency in range(1,30):
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
            if tn == 0:
                plt.plot(range(1,30),y,c=clrs[vehicleCapacity],
                         label=str(vehicleCapacity)+' people capacity\n100% take up')
            elif tn == 1:
                plt.plot(range(1,30),y,ls='--',c=clrs[vehicleCapacity],
                         label=str(vehicleCapacity)+' people capacity\n50% take up')
            else:
                plt.plot(range(1,30),y,ls=':',c=clrs[vehicleCapacity],
                         label=str(vehicleCapacity)+' people capacity\n25% take up')
        plt.grid()
        if rn in [2,3,4] and tn == 1:
            plt.xlabel('frequency (mins)')
        plt.xlim(1,29)
        plt.ylim(0,300)
        if rn in [0,3] and tn == 1:
            plt.ylabel('Number of customers')
plt.tight_layout()
plt.legend(loc=[1.3,0.2])
plt.show()
