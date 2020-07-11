import math, copy

# find euclidean distance in 3d
def dist(dataPoint1, dataPoint2):
    x = (dataPoint1[0], dataPoint1[1], dataPoint1[2])
    y = (dataPoint2[0], dataPoint2[1], dataPoint2[2])
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

# find the min distance in 2 clusters
def distMINcluster(cluster1, cluster2):
    distMin = dist(cluster1[0], cluster2[0])
    for i in cluster1:
        for j in cluster2:
            distance  = dist(i, j)
            if distMin > distance :
                distMin = distance
    return distMin

# find the max distance in 2 clusters
def distMAXcluster(cluster1, cluster2):
    distMax = dist(cluster1[0], cluster2[0])
    for i in cluster1:
        for j in cluster2:
            distance  = dist(i, j)
            if distMax < distance :
                distMax = distance
    return distMax

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
            print(f'cluster {c+1} with {numberOfPointInClass0} alives and {numberOfPointInClass1} deads the entropy is {entropyForCluster}')
        else:
            print(f'cluster {c+1} with {numberOfPointInClass0} alives and {numberOfPointInClass1} deads the entropy is {0}')
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

lenData = len(lisData)
# create the clusters
lisClusters = []
for i in range(lenData):
    lisClusters.append([])
    lisClusters[i].append(lisData[i])

# create the proximity matrix
lenClusters = len(lisClusters)
matrixProximity = []
for i in range(lenClusters):
    matrixProximity.append([])
    for j in range(lenClusters):
        matrixProximity[i].append(distMAXcluster(lisClusters[i], lisClusters[j]))

# print(matrixProximity[0][:10])

# ===============REPEAT===============
while len(lisClusters) != 1:
    # list clusters next = []
    lisClustersNext = []

    # setClustersAvailable = {}
    sca = set()
    for i in range(len(matrixProximity)):
        sca.add(i)

    # MERGE
    minimum = jMin = 0
    for i in range(len(matrixProximity)):
        if i not in sca:
            continue
        if len(sca) == 1:
            lis = []
            for point in lisClusters[i]:
                lis.append(point)
            lisClustersNext.append(lis)
            sca.discard(i)
            break
        flag = False
        for j in range(len(matrixProximity)):
            if flag == False and i != j and (j in sca) :
                minimum = matrixProximity[i][j]
                jMin = j
                flag = True
            if i != j and (j in sca) and matrixProximity[i][j] < minimum:
                minimum = matrixProximity[i][j]
                jMin = j
        
        # real merge
        lis = []
        for point in lisClusters[i]:
            lis.append(point)
        for point in lisClusters[jMin]:
            lis.append(point)
        lisClustersNext.append(lis)
        # remove clusters from set clusters available
        sca.discard(i)
        sca.discard(jMin)

    # UPDATE THE PROXIMITY MATRIX
    lisClusters.clear()
    lisClusters = copy.deepcopy(lisClustersNext)
    lenClusters = len(lisClusters)
    matrixProximity = []
    for i in range(lenClusters):
        matrixProximity.append([])
        for j in range(lenClusters):
            matrixProximity[i].append(distMAXcluster(lisClusters[i], lisClusters[j]))
    # SHOW THE CLUSTERS
    print('how many clusters : ', len(lisClusters))
    findEntropy(lisClusters)
    c = 0
    for cluster in lisClusters:
        print(f'cluster {c+1} has {len(cluster)} points, and the cluster is :' , cluster)
        c += 1
    print('_' * 100)