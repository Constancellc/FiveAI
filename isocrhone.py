import csv
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
import numpy as np
from scipy.interpolate import interp1d

orange_start = [546598,163982]
pink_start = [531479,157201]
red_start = [533165,159755]
purple_start = [538051,166008]
blue_start = [532316,166170]

pink2_start = [531592,157376]
orange2_start = [546952,164213]
blue2_start = [536198,165576]
purple2_start = [538188,165971]
red2_start = [533378,159106]

# change these two to switch the map being made 
rte = 'orange' 
start = orange_start

'''
rte can take the following values

'pink'
'orange'
'red'
'purple'
'blue'
'pink2_'
'orange2_'
'blue2_'
'purple2_'
'red2_'
'''

def alpha_shape(points, alpha=8000, only_outer=True):
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

def smooth(x,y):
    orig_len = len(x)
    x = x[-3:-1] + x + x[1:3]
    y = y[-3:-1] + y + y[1:3]

    t = np.arange(len(x))
    ti = np.linspace(2, orig_len + 1, 10 * orig_len)

    xi = interp1d(t, x, kind='quadratic')(ti)
    yi = interp1d(t, y, kind='quadratic')(ti)

    return [xi,yi]

test15 = []
test30 = []
test60 = []
u10 = {'x':[],'y':[]}
u20 = {'x':[],'y':[]}
u30 = {'x':[],'y':[]}
o30 = {'x':[],'y':[]}


pickUp = {'pink':['7','13','End'],'orange':['9','20','End'],
          'red':['9','16','End'],'purple':['9','21','End'],
          'blue':['15','23','End'],'pink2_':['7','17','End'],
          'orange2_':['10','18','End'],'blue2_':['8','17','End'],
          'purple2_':['8','12','End'],'red2_':['6','14','End']}

pickUpTimes = {'pink':[290,717,1569],'orange':[355,898,1672],
               'red':[383,664,1379],'purple':[298,932,1596],
               'blue':[925,475,2050],'pink2_':[226,718,1472],
               'orange2_':[470,910,1790],'blue2_':[345,915,1541],
               'purple2_':[476,696,1194],'red2_':[293,728,1523]}


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

edges60 = alpha_shape(np.array(test60),alpha=2500)
edges30 = alpha_shape(np.array(test30),alpha=2700)
edges15 = alpha_shape(np.array(test15),alpha=3000)

img = plt.imread("back.png")
fig, ax = plt.subplots(figsize=(10,8))
plt.xlim(527500,547500)
plt.xticks([527500,547500],['',''])
plt.yticks([156000,172000],['',''])
plt.ylim(156000,172000)
ax.imshow(img, extent=[527500, 547500, 156000, 172000])
'''
plt.scatter(o30['x'],o30['y'])
plt.scatter(u30['x'],u30['y'])
plt.scatter(u20['x'],u20['y'])
plt.scatter(u10['x'],u10['y'])
'''
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
[xi,yi] = smooth(x,y)
plt.plot(xi,yi,'b',ls=':')


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
[xi,yi] = smooth(x,y)
plt.plot(xi,yi,'g',ls=':')

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
[xi,yi] = smooth(x,y)
plt.plot(xi,yi,'r',ls=':')
    
plt.scatter([start[0]],[start[1]],20,'k',zorder=3)


# now let's get the new one

test15 = []
test30 = []
test60 = []
u10 = {'x':[],'y':[]}
u20 = {'x':[],'y':[]}
u30 = {'x':[],'y':[]}
o30 = {'x':[],'y':[]}


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

with open(rte+'LatLong.csv','rU') as csvfile:
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
[xi,yi] = smooth(x,y)
plt.plot(xi,yi,'b')

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
[xi,yi] = smooth(x,y)
plt.plot(xi,yi,'g')
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
[xi,yi] = smooth(x,y)
plt.plot(xi,yi,'r')


plt.tight_layout()
plt.show()
