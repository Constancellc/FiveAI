import csv
import matplotlib.pyplot as plt
import numpy as np
import copy

xs = []
ys = []

pts = []

        
with open('base-ptals-grid-values.csv','rU') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        x = 50*int(int(row[1])/50)
        y = 50*int(int(row[2])/50)

        if x < 525500:
            continue
        if x > 548500:
            continue
        if y > 173000:
            continue
        if y < 155000:
            continue
        
        if x not in xs:
            xs.append(x)            
        if y not in ys:
            ys.append(y)
            
        z = int(row[4][0])

        pts.append([x,y,z])

xs = sorted(xs)
ys = sorted(ys)

def fit2grid(x,y):
    # first x
    i = 0
    while xs[i] < x:
        i += 1
    if abs(x-xs[i]) > abs(x-xs[i-1]):
        i -= 1
    # then y
    j = 0
    while ys[j] < y:
        j += 1
    if abs(y-ys[j]) > abs(y-ys[j-1]):
        j -= 1

    return [i,j]
        
x_in = {}
for i in range(len(xs)):
    x_in[xs[i]] = i
y_in = {}
for i in range(len(ys)):
    y_in[ys[i]] = i

grid = []
for i in range(len(ys)):
    grid.append([-1.0]*len(xs))

for p in pts:
    grid[len(ys)-1-y_in[p[1]]][x_in[p[0]]] = p[2]

def find_nearest(im,x,y,step):
    x2 = None
    y2 = None
    closest = 100000
    for i in np.arange(x-step,x+step):
        for j in np.arange(y-step,y+step):
            try:
                if im[int(i)][int(j)] == -1:
                    continue
            except:
                continue
            dist = np.power(i-x,2)+np.power(j-y,2)
            if dist < closest:
                closest = dist
                x2 = int(i)
                y2 = int(j)
                
    return [x2,y2]
    
def in_paint(im):
    swaps = {}
    for x in range(len(im)):
        for y in range(len(im[0])):
            if im[x][y] == -1:
                [x2,y2] = find_nearest(im,x,y,5)
                if x2 == None:
                    im[x][y] = 0
                    continue
                if x not in swaps:
                    swaps[x] = {}
                swaps[x][y] = [x2,y2]

    for x in swaps:
        for y in swaps[x]:
            [x2,y2] = swaps[x][y]
            im[x][y] = im[x2][y2]
    return im

grid2 = in_paint(grid)
plt.figure()
img = plt.imread("back2.png")
plt.imshow(img, extent=[527500, 547500, 156000, 172000])
plt.xlim(527500,547500)
plt.ylim(156000,172000)
plt.xticks([527500,547500],['',''])
plt.yticks([156000,172000],['',''])
plt.imshow(grid2,cmap='magma',extent=[min(xs),max(xs),min(ys),max(ys)],
           alpha=0.4)

for clr in ['pink','red','blue','orange','purple']:
    route = []
    e0 = []
    n0 = []
    with open(clr+'LatLong.csv','rU') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row == []:
                continue
            x = int(row[0])
            y = int(row[1])
            e0.append(x)
            n0.append(y)
            [i,j] = fit2grid(x,y)
            route.append([i,j])

    p = []
    e = []
    n = []

    for i in range(len(route)):
        e.append(xs[route[i][0]])
        n.append(ys[len(grid2)-route[i][1]])
        p.append(grid2[len(grid2)-route[i][1]][route[i][0]])

    s = 0
    av = 0
    print(clr)
    print(p)
    for i in range(1,len(p)):
        av += 0.5*(p[i-1]+p[i])*np.sqrt(np.power(e[i]-e[i-1],2)+\
                                        np.power(n[i]-n[i-1],2))
        s += np.sqrt(np.power(e[i]-e[i-1],2)+np.power(n[i]-n[i-1],2))
    print(av/s)
            
    plt.plot(e0,n0,c='white')#clr)
plt.colorbar()
plt.title('PTAL Heatmap')
plt.show()
        
