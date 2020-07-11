import numpy as np, random, copy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def show(w,data):
    # show hyperplane
    a,b,c,d = int(w[0]), int(w[1]), int(w[2]), int(w[3])
    # x, y ranges in my data because the hyperplane draws in that range
    x = np.linspace(29,84,55)
    y = np.linspace(57,70,23)
    X,Y = np.meshgrid(x,y)
    Z = (-d - a*X - b*Y) / c
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, Z)
    # show the data
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

    plt.show()

# read from data
fileData = open('haberman.data','r')

# import data into list
# lisData = age, year, no, survival
lisData = []
for line in fileData:
    lisData.append(list(map(int, line.split(','))))
fileData.close()

# shuffle the input data
random.shuffle(lisData)
trainData = copy.deepcopy(lisData[:250])
testData = copy.deepcopy(lisData[250:])
# ______________________TRAIN______________________

w = np.array([[0],[0],[0],[0]])
ro = 1
wPre = None

# REPEAT
# from the rosenblatt algo
for i in range(200):
    for point in trainData:
        x = np.array([[point[0]],[point[1]],[point[2]],[1]])
        wMULTx = int(np.dot(w.T,x))
        # w1 alive
        if point[3] == 1 and wMULTx <= 0:
            wNew = np.add(w,ro*x)
        # w2 dead
        elif point[3] == 2 and wMULTx >= 0:
            wNew = np.subtract(w,ro*x)
        else:
            wNew = w.copy()
        w = wNew.copy()
    ro = ro / (i + 1)
    if np.array_equal(w,wPre):
        break
    wPre = w.copy()
show(w,trainData)

# ______________________TEST______________________

# v = predict   ,  actual :
# a = alive     ,   alive
# b = dead      ,   alive
# c = alive     ,   dead
# d = dead      ,   dead
a = b = c = d = 0
for point in testData:
    x = np.array([[point[0]],[point[1]],[point[2]],[1]])
    wMULTx = int(np.dot(w.T,x))
    if wMULTx > 0:
        if point[3] == 1:   # a
            a += 1
        else:               # c
            c += 1
    elif wMULTx < 0:
        if point[3] == 2:   # d
            d += 1
        else:               # b
            b += 1
print("""
number of people that we predict = alive and actual = alive : {0:2}
number of people that we predict = alive and actual = dead  : {1:2}
number of people that we predict = dead and actual = alive  : {2:2}
number of people that we predict = dead and actual = dead   : {3:2}
Percision   : {4:f}
Recall      : {5:f}
Accuracy    : {6:f}
""".format(a, c, b, d, a/(a+c), a/(a+b), (a+d)/(a+b+c+d)))
