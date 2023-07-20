# %%
import matplotlib.pylab as plt
import math
import random as rand
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pathlib

def readPoints(fileName):
    #open and parser kml file
    file_path = pathlib.Path(fileName)
    tree = ET.parse(file_path)
    folder = tree.getroot()[0][1]
    names = []
    size = len(folder) - 1
    #points = np.random.randint(-1000, 1000, size * 2)
    points = np.zeros(size * 2)
    points = np.reshape(points, [size, 2])
    for i in range(1, len(folder)):
        node = folder[i]
        names.append(node[0].text)
        tokens = node[2][0].text.split(',')
        long = math.radians(float(tokens[0]))
        lat = math.radians(float(tokens[1]))
        alt = math.radians(float(tokens[2]))
        points[i-1, 0] = long
        points[i-1, 1] = lat
        #print(i-1, long, lat, alt) 
    return points, names, size 

def calcDistances(points, size):
    G = np.zeros(size * size)
    G = np.reshape(G, [size, size])
    R = 6373.0  #radius of Earth in km 
    for i in range(0, size): 
        for j in range(i + 1, size):
            long1 = points[i,0]
            lat1 = points[i,1]
            long2 = points[j,0]
            lat2 = points[j,1]
            dlong = abs(long2 - long1)
            dlat = abs(lat2 - lat1)
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlong / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            d = c * R   #distance between points in km
            G[i,j] = d
            G[j,i] = d
            #print(long1, lat1, long2, lat2, d)
    return G

def calcPathDistance(G, path):
    dist = 0
    for j in range(len(path) - 1):
        dist += G[int(path[j]), int(path[j+1])]
    return dist

def crossover(p1, p2):
    cut = rand.randrange(1, len(p1) - 2)
    child = np.zeros(len(p1))
    S = {}
    for j in range(cut):
        child[j] = p1[j] 
        S[p1[j]] = 1
    for j in range(len(p2)):
        if not p2[j] in S:
            child[cut] = p2[j]
            S[p2[j]] = 1
            cut += 1
    return child

#bitswap
def mutation(path):
    r1 = rand.randrange(len(path))
    r2 = rand.randrange(len(path))
    temp = path[r1]        
    path[r1] = path[r2]        
    path[r2] = temp         
    return path
    
def genetic_algorithm(G, size, pop_size, gen_limit):   
    next_pop_limit = math.floor(pop_size / 2)
    #initialize population
    paths = []
    for i in range(pop_size):
        path = np.random.permutation(size) 
        paths.append(path)

    gen = 1
    bestPath = []
    bestDistance = float('inf')
    while gen <= gen_limit:
        #calculate path distance
        distances = np.zeros(pop_size)
        for i in range(len(paths)):
            distances[i] = calcPathDistance(G, paths[i])   
        #sort distance ascended 
        paths, distances = (list(x) for x in zip(*sorted(zip(paths,distances), key=lambda pair:pair[1])))

        #choose best solutions
        if bestDistance > distances[0]:
            bestDistance = distances[0]
            bestPath = paths[0]
        gen += 1
        
        #crossover
        for i in range(next_pop_limit, pop_size): 
            p1 = paths[rand.randrange(next_pop_limit)]
            p2 = paths[rand.randrange(next_pop_limit)]  
            paths[i] = crossover(p1, p2) 
        
        #mutation 
        for i in range(next_pop_limit, pop_size): 
            if rand.random() < 0.5:
                paths[i] = mutation(paths[i])    
    
    return bestPath, bestDistance, gen

points, names, size = readPoints(r'Άγιος Γεώργιος.kml')
G = calcDistances(points, size)
gen_limit = 500
pop_size = 200
print("Running for", size ,"points")
print("Generations:", gen_limit)
print("Population:", pop_size)
print("Please wait...")
bestPath, bestDistance, gens = genetic_algorithm(G, size, pop_size, gen_limit)

print("Best Distance:", bestDistance, "km")  #fitness
print("With path: ")
for i in range(len(bestPath)):
    print(names[int(bestPath[i])], end = ' ') 

print() 

long = np.zeros(len(bestPath))
lat = np.zeros(len(bestPath))

for i in range(0, len(bestPath)):  
    long[i] = points[int(bestPath[i]),0]
    lat[i] = points[int(bestPath[i]),1]

plt.figure(figsize=(23,12))
plt.plot(long, lat, '-o', c='green')
#plt.scatter(long,lat)
plt.xlabel('Longitude (γεωγραφικό μήκος)')
plt.ylabel('Latitude (γεωγραφικό πλάτος)')
#plt.grid(True)
plt.show     

# %%
