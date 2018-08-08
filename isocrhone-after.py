import csv
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import numpy as np


def alpha_shape(points, alpha=2500, only_outer=True):
    """
    Compute the alpha shape (concave hull) of a set of points.
    :param points: np.array of shape (n,2) points.
    :param alpha: alpha value.
    :param only_outer: boolean value to specify if we keep only the outer border
    or also inner edges.
    :return: set of (i,j) pairs representing edges of the alpha-shape. (i,j) are
    the indices in the points array.
    """
    assert points.shape[0] > 3, "Need at least four points"

    def add_edge(edges, i, j):
        """
        Add an edge between the i-th and j-th points,
        if not in the list already
        """
        if (i, j) in edges or (j, i) in edges:
            # already added
            assert (j, i) in edges, "Can't go twice over same directed edge right?"
            if only_outer:
                # if both neighboring triangles are in shape, it's not a boundary edge
                edges.remove((j, i))
            return
        edges.add((i, j))

    tri = Delaunay(points)
    edges = set()
    # Loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]
        # Computing radius of triangle circumcircle
        # www.mathalino.com/reviewer/derivation-of-formulas/derivation-of-formula-for-radius-of-circumcircle
        a = np.sqrt((pa[0] - pb[0]) ** 2 + (pa[1] - pb[1]) ** 2)
        b = np.sqrt((pb[0] - pc[0]) ** 2 + (pb[1] - pc[1]) ** 2)
        c = np.sqrt((pc[0] - pa[0]) ** 2 + (pc[1] - pa[1]) ** 2)
        s = (a + b + c) / 2.0
        area = np.sqrt(s * (s - a) * (s - b) * (s - c))
        circum_r = a * b * c / (4.0 * area)
        if circum_r < alpha:
            add_edge(edges, ia, ib)
            add_edge(edges, ib, ic)
            add_edge(edges, ic, ia)
    return edges

test15 = []
test30 = []
test60 = []
u10 = {'x':[],'y':[]}
u20 = {'x':[],'y':[]}
u30 = {'x':[],'y':[]}
o30 = {'x':[],'y':[]}

orange_start = [546598,163982]
pink_start = [531479,157201]

pickUp = {'pink':['7','13','End'],'orange':['9','20']}
pickUpTimes = {'pink':[290,717,1569],'orange':[355,898]}

start = orange_start
rte = 'orange'

stopTimes = [0]
with open(rte+'DistTimes.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    t = 0
    for row in reader:
        if len(row) < 1:
            continue
        t += int(row[1])
        stopTimes.append(t)
print(stopTimes)

with open(rte+'EasNor.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    i = 0
    for row in reader:
        if len(row) < 1 or i == len(stopTimes)-1:
            continue
        t = stopTimes[i]
        if t < 15*60:
            test15.append([float(row[0]),float(row[1])])
            u10['x'].append(float(row[0]))
            u10['y'].append(float(row[1]))
        if t < 30*60:
            test30.append([float(row[0]),float(row[1])])
            u20['x'].append(float(row[0]))
            u20['y'].append(float(row[1]))
        if t < 60*60:            
            test60.append([float(row[0]),float(row[1])])
            u30['x'].append(float(row[0]))
            u30['y'].append(float(row[1]))
        i += 1
        

with open('from'+rte+'StartEN.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) <= 2:
            continue
        t = int(row[4])
        if t < 15*60:
            test15.append([float(row[2]),float(row[3])])
            u10['x'].append(float(row[2]))
            u10['y'].append(float(row[3]))
        if t < 30*60:
            test30.append([float(row[2]),float(row[3])])
            u20['x'].append(float(row[2]))
            u20['y'].append(float(row[3]))
        if t < 60*60:            
            test60.append([float(row[2]),float(row[3])])
            u30['x'].append(float(row[2]))
            u30['y'].append(float(row[3]))
        else:
            o30['x'].append(float(row[2]))
            o30['y'].append(float(row[3]))

for i in range(len(pickUp[rte])):
    with open('from'+rte+pickUp[rte][i]+'EN.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) < 1:
                continue
            t = int(row[4])+pickUpTimes[rte][i]
            if t < 15*60:
                test15.append([float(row[2]),float(row[3])])
                u10['x'].append(float(row[2]))
                u10['y'].append(float(row[3]))
            if t < 30*60:
                test30.append([float(row[2]),float(row[3])])
                u20['x'].append(float(row[2]))
                u20['y'].append(float(row[3]))
            if t < 60*60:            
                test60.append([float(row[2]),float(row[3])])
                u30['x'].append(float(row[2]))
                u30['y'].append(float(row[3]))
            else:
                o30['x'].append(float(row[2]))
                o30['y'].append(float(row[3]))
            

edges60 = alpha_shape(np.array(test60))
edges30 = alpha_shape(np.array(test30))
edges15 = alpha_shape(np.array(test15))


plt.figure()
img = plt.imread("back.png")
fig, ax = plt.subplots()
plt.xlim(527500,547500)
plt.ylim(156000,172000)
ax.imshow(img, extent=[527500, 547500, 156000, 172000])
'''
plt.scatter(o30['x'],o30['y'])
plt.scatter(u30['x'],u30['y'])
plt.scatter(u20['x'],u20['y'])
plt.scatter(u10['x'],u10['y'])
#'''
x = []
y = []
lines = {}
for i, j in edges60:
    lines[i] = j
nodes = [i,j]
while len(nodes) < len(lines)+1:
    nodes.append(lines[nodes[-1]])
for p in nodes:
    x.append(test60[p][0])
    y.append(test60[p][1])
    #plt.fill(x,y,'y',alpha=0.5)
    plt.plot(x,y,'b')
x = []
y = []
lines = {}
for i, j in edges30:
    lines[i] = j
nodes = [i,j]
while len(nodes) < len(lines)+1:
    nodes.append(lines[nodes[-1]])
for p in nodes:
    x.append(test30[p][0])
    y.append(test30[p][1])
    plt.plot(x,y,'g')
x = []
y = []
lines = {}
for i, j in edges15:
    lines[i] = j
nodes = [i,j]
while len(nodes) < len(lines)+1:
    nodes.append(lines[nodes[-1]])
for p in nodes:
    x.append(test15[p][0])
    y.append(test15[p][1])
    plt.plot(x,y,'r')
    #plt.fill(x,y,'r',alpha=0.5)
    #plt.plot([test15[i][0],test15[j][0]],[test15[i][1],test15[j][1]],c='r')
plt.scatter([start[0]],[start[1]],20,'k',zorder=3)
plt.show()
