import random, math, copy, numpy
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

# find euclidean distance in 3d
def dist(dataPoint, centroid):
    x = (dataPoint[0], dataPoint[1], dataPoint[2])
    y = (centroid[0], centroid[1], centroid[2])
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

# show data in clusters and random centroids
def show(data):
    fig = pyplot.figure()
    ax = Axes3D(fig)
    x = []
    y = []
    z = []
    x1 = []
    y1 = []
    z1 = []
    for i in data:
        if i[3] == 1 :
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])
        else:
            x1.append(i[0])
            y1.append(i[1])
            z1.append(i[2])
    # live :)
    ax.scatter(x, y, z, c='g', marker='o')
    # dead :(
    ax.scatter(x1, y1, z1, c='r', marker='o')

    pyplot.show()

# show clusters and centroids in colors
def showClusters(centeroids,lisClusters ):
    fig = pyplot.figure()
    ax = Axes3D(fig)
    xx = []
    yy = []
    zz = []
    for cluster in lisClusters:
        x = []
        y = []
        z = []
        for i in cluster:
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])
        # for each cluster
        ax.scatter(x, y, z, 'color', marker='o')
    for i in centeroids:
        xx.append(i[0])
        yy.append(i[1])
        zz.append(i[2])
    # each centroids
    ax.scatter(xx, yy, zz, c='b', marker='^')
    pyplot.show()

# find the entropy based on live or dead
def findEntropy(lisClusters):
    c = 0
    for cluster in lisClusters:
        if len(cluster) == 0:
            print(f'//len of cluster {c+1} is empty\\\\')
            continue
        entropyForCluster = 0
        numberOfPointInClass0 = 0
        numberOfPointInClass1 = 0
        for point in cluster:
            if point[3] == 1:
                numberOfPointInClass0 += 1
            else:
                numberOfPointInClass1 += 1
        # divisionOfNumberOfPointsInClusterToAllPoints
        division1 = (numberOfPointInClass0 / len(cluster))
        division2 = (numberOfPointInClass1 / len(cluster))
        if division1 != 0 and division2 != 0:
            entropyForCluster = - (division1 * (math.log2(division1))) - (division2 * (math.log2(division2)))
            print('for cluster of ', c + 1, ' the entropy is ', entropyForCluster)
        else:
            print('for cluster of ', c + 1, ' the entropy is ', 0)
        c += 1
    print('*' * 30)

# read from data
fileData = open('haberman.data','r')

# import data into list
# lisData = age, year, no, survival
lisData = []
for line in fileData:
    lisData.append(list(map(int, line.split(','))))
fileData.close()

minAge = minYear = minNo = 100
maxAge = maxYear = maxNo = 0
for i in lisData:
    if i[0] < minAge:
        minAge = i[0] 
    if i[1] < minYear:
        minYear = i[1]
    if i[2] < minNo:
        minNo = i[2]
    if i[0] > maxAge:
        maxAge = i[0] 
    if i[1] > maxYear:
        maxYear = i[1]
    if i[2] > maxNo:
        maxNo = i[2]
# print(minAge, minYear, minNo, maxAge, maxYear, maxNo)

# select k random centroids
k = 3
# location of k centroids
# lisCentrois = x,y,z == age, year, no
lisCentroids = []
for i in range(k):
    lisCentroids.append([])
    lisCentroids[i].append(random.randint(minAge,maxAge))
    lisCentroids[i].append(random.randint(minYear,maxYear))
    lisCentroids[i].append(random.randint(minNo,maxNo))
# print(lisCentroids)

show(lisData)

# THE REPAET
# we need lisCentroids pre for checking that centroid change or not
lisCentroidsPre = []
for iteration in range(50):
    # if the iteration is over
    if lisCentroids == lisCentroidsPre :
        break

    # assinging all points in clusters
    lisClusters = []
    for j in range(k):
        lisClusters.append([])
    for point in lisData:
        # distance from each centroid and point
        lisDistance = []
        for j in range(k):
            lisDistance.append(dist(point, lisCentroids[j]))
        # print(min(lisDistance), lisDistance.index(min(lisDistance)))
        
        # which centroid is close to point
        whichCluster = lisDistance.index(min(lisDistance))
        lisClusters[whichCluster].append(point)

    showClusters(lisCentroids,lisClusters)

    lisCentroidsPre = copy.deepcopy(lisCentroids)
    # recompute the centroids
    c = 0
    for cluster in lisClusters:
        midAge = midYear = midNo = 0
        # compute the mid of all points in cluster
        for point in cluster:
            midAge += point[0]
            midYear += point[1]
            midNo += point[2]
        lenCluster = len(cluster)
        if lenCluster != 0:
            lisCentroids[c] = [midAge / lenCluster , midYear / lenCluster, midNo / lenCluster]
        c += 1
    findEntropy(lisClusters)
    # print(iteration, lisCentroids)
