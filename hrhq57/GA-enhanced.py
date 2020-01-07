import os
import sys
import time
import random

def read_file_into_string(input_file, from_ord, to_ord):
    # take a file "input_file", read it character by character, strip away all unwanted
    # characters with ord < "from_ord" and ord > "to_ord" and return the concatenation
    # of the file as the string "output_string"
    the_file = open(input_file,'r')
    current_char = the_file.read(1)
    output_string = ""
    while current_char != "":
        if ord(current_char) >= from_ord and ord(current_char) <= to_ord:
            output_string = output_string + current_char
        current_char = the_file.read(1)
    the_file.close()
    return output_string

def stripped_string_to_int(a_string):
    # take a string "a_string" and strip away all non-numeric characters to obtain the string
    # "stripped_string" which is then converted to an integer with this integer returned
    a_string_length = len(a_string)
    stripped_string = "0"
    if a_string_length != 0:
        for i in range(0,a_string_length):
            if ord(a_string[i]) >= 48 and ord(a_string[i]) <= 57:
                stripped_string = stripped_string + a_string[i]
    resulting_int = int(stripped_string)
    return resulting_int

def get_string_between(from_string, to_string, a_string, from_index):
    # look for the first occurrence of "from_string" in "a_string" starting at the index
    # "from_index", and from the end of this occurrence of "from_string", look for the first
    # occurrence of the string "to_string"; set "middle_string" to be the sub-string of "a_string"
    # lying between these two occurrences and "to_index" to be the index immediately after the last
    # character of the occurrence of "to_string" and return both "middle_string" and "to_index"
    middle_string = ""              # "middle_string" and "to_index" play no role in the case of error
    to_index = -1                   # but need to initialized to something as they are returned
    start = a_string.find(from_string,from_index)
    if start == -1:
        flag = "*** error: " + from_string + " doesn't appear"
        #trace_file.write(flag + "\n")
    else:
        start = start + len(from_string)
        end = a_string.find(to_string,start)
        if end == -1:
            flag = "*** error: " + to_string + " doesn't appear"
            #trace_file.write(flag + "\n")
        else:
            middle_string = a_string[start:end]
            to_index = end + len(to_string)
            flag = "good"
    return middle_string,to_index,flag

def string_to_array(a_string, from_index, num_cities):
    # convert the numbers separated by commas in the file-as-a-string "a_string", starting from index "from_index",
    # which should point to the first comma before the first digit, into a two-dimensional array "distances[][]"
    # and return it; note that we have added a comma to "a_string" so as to find the final distance
    # distance_matrix = []
    if from_index >= len(a_string):
        flag = "*** error: the input file doesn't have any city distances"
        #trace_file.write(flag + "\n")
    else:
        row = 0
        column = 1
        row_of_distances = [0]
        flag = "good"
        while flag == "good":
            middle_string, from_index, flag = get_string_between(",", ",", a_string, from_index)
            from_index = from_index - 1         # need to look again for the comma just found
            if flag != "good":
                flag = "*** error: there aren't enough cities"
                # trace_file.write(flag + "\n")
            else:
                distance = stripped_string_to_int(middle_string)
                row_of_distances.append(distance)
                column = column + 1
                if column == num_cities:
                    distance_matrix.append(row_of_distances)
                    row = row + 1
                    if row == num_cities - 1:
                        flag = "finished"
                        row_of_distances = [0]
                        for i in range(0, num_cities - 1):
                            row_of_distances.append(0)
                        distance_matrix.append(row_of_distances)
                    else:
                        row_of_distances = [0]
                        for i in range(0,row):
                            row_of_distances.append(0)
                        column = row + 1
        if flag == "finished":
            flag = "good"
    return flag

def make_distance_matrix_symmetric(num_cities):
    # make the upper triangular matrix "distance_matrix" symmetric;
    # note that there is nothing returned
    for i in range(1,num_cities):
        for j in range(0,i):
            distance_matrix[i][j] = distance_matrix[j][i]

# read input file into string

#######################################################################################################
############ now we read an input file to obtain the number of cities, "num_cities", and a ############
############ symmetric two-dimensional list, "distance_matrix", of city-to-city distances. ############
############ the default input file is given here if none is supplied via a command line   ############
############ execution; it should reside in a folder called "city-files" whether it is     ############
############ supplied internally as the default file or via a command line execution.      ############
############ if your input file does not exist then the program will crash.                ############

input_file = "AISearchfile058.txt"

#######################################################################################################

# you need to worry about the code below until I tell you; that is, do not touch it!

if len(sys.argv) == 1:
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
else:
    input_file = sys.argv[1]
    file_string = read_file_into_string("../city-files/" + input_file,44,122)
file_string = file_string + ","         # we need to add a final comma to find the city distances
                                        # as we look for numbers between commas
print("I'm working with the file " + input_file + ".")
                                        
# get the name of the file

name_of_file,to_index,flag = get_string_between("NAME=", ",", file_string, 0)

if flag == "good":
    print("I have successfully read " + input_file + ".")
    # get the number of cities
    num_cities_string,to_index,flag = get_string_between("SIZE=", ",", file_string, to_index)
    num_cities = stripped_string_to_int(num_cities_string)
else:
    print("***** ERROR: something went wrong when reading " + input_file + ".")
if flag == "good":
    print("There are " + str(num_cities) + " cities.")
    # convert the list of distances into a 2-D array
    distance_matrix = []
    to_index = to_index - 1             # ensure "to_index" points to the comma before the first digit
    flag = string_to_array(file_string, to_index, num_cities)
if flag == "good":
    # if the conversion went well then make the distance matrix symmetric
    make_distance_matrix_symmetric(num_cities)
    print("I have successfully built a symmetric two-dimensional array of city distances.")
else:
    print("***** ERROR: something went wrong when building the two-dimensional array of city distances.")

#######################################################################################################
############ end of code to build the distance matrix from the input file: so now you have ############
############ the two-dimensional "num_cities" x "num_cities" symmetric distance matrix     ############
############ "distance_matrix[][]" where "num_cities" is the number of cities              ############
#######################################################################################################

# now you need to supply some parameters ...

#######################################################################################################
############ YOU NEED TO INCLUDE THE FOLLOWING PARAMETERS:                                 ############
############ "my_user_name" = your user-name, e.g., mine is dcs0ias                        ############

my_user_name = "dcs0ias"

############ "my_first_name" = your first name, e.g., mine is Iain                         ############

my_first_name = "Iain"

############ "my_last_name" = your last name, e.g., mine is Stewart                        ############

my_last_name = "Stewart"

############ "alg_code" = the two-digit code that tells me which algorithm you have        ############
############ implemented (see the assignment pdf), where the codes are:                    ############
############    BF = brute-force search                                                    ############
############    BG = basic greedy search                                                   ############
############    BS = best_first search without heuristic data                              ############
############    ID = iterative deepening search                                            ############
############    BH = best_first search with heuristic data                                 ############
############    AS = A* search                                                             ############
############    HC = hilling climbing search                                               ############
############    SA = simulated annealing search                                            ############
############    GA = genetic algorithm                                                     ############

alg_code = "GA"

############ you can also add a note that will be added to the end of the output file if   ############
############ you like, e.g., "in my basic greedy search, I broke ties by always visiting   ############
############ the first nearest city found" or leave it empty if you wish                   ############

added_note = ""

############ the line below sets up a dictionary of codes and search names (you need do    ############
############ nothing unless you implement an alternative algorithm and I give you a code   ############
############ for it when you can add the code and the algorithm to the dictionary)         ############

codes_and_names = {'BF' : 'brute-force search',
                   'BG' : 'basic greedy search',
                   'BS' : 'best_first search without heuristic data',
                   'ID' : 'iterative deepening search',
                   'BH' : 'best_first search with heuristic data',
                   'AS' : 'A* search',
                   'HC' : 'hilling climbing search',
                   'SA' : 'simulated annealing search',
                   'GA' : 'genetic algorithm'}

#######################################################################################################
############    now the code for your algorithm should begin                               ############
#######################################################################################################

import heapq as hp
import random as rd
import math

# Defines set of cities for quick checking
citySet = set(range(num_cities))

# Custom class for chromosomes; stores own tour, length and fitness (inverse of length)
class Chrom():
    # Gives chromosome a random tour if none specified
    def __init__(self,tour):
        self.tour = [c for c in tour]
        self.calcFit()
    
    # Calculates tour length and fitness
    def calcFit(self):
        tourLen = 0
        for i in range(-1,num_cities-1):
            tourLen += distance_matrix[self.tour[i]][self.tour[i+1]]
        self.l = tourLen
        self.f = 1000/tourLen
        return
    
    # Prints chromosome attributes
    def __str__(self):
        return "{self.tour} - {self.l} - {self.f}".format(self=self)

    # Redefines state comparisons to be in terms of length
    def __eq__(self,other):
        return self.l == other.l
    def __ne__(self,other):
        return self.l != other.l
    def __lt__(self,other):
        return self.l < other.l
    def __le__(self,other):
        return self.l <= other.l
    def __gt__(self,other):
        return self.l > other.l
    def __ge__(self,other):
        return self.l >= other.l

# Selects a chromosome via a random weighted process, equivalent to roulette
def roulette():
    pick = rd.uniform(0,sumFit)
    current = 0
    for c in pop:
        current += c.f
        if current > pick:
            return c
        
# Checks average fitness of chroms picked by roulette()
def checkAverages():
    sumFit = sum([c.f for c in pop])    
    avgFit = sumFit / popSize
    total = 0
    for i in range(10000):
        chrom = roulette()
        total += chrom.f
    avgSel = total / 10000
    print(avgFit)
    print(avgSel)

# Crossover as provided on lecture slides and spec
def crossover(X,Y):
    pos = rd.randint(1,num_cities-1)
    splitX = (X.tour[:pos],X.tour[pos:])
    splitY = (Y.tour[:pos],Y.tour[pos:])
    newX = splitX[0]+splitY[1]
    newY = splitY[0]+splitX[1]
    notX = citySet - set(newX)
    notY = citySet - set(newY)
    seenX = set()
    seenY = set()
    dupesX = []
    dupesY = []
    for i in range(num_cities):
        if newX[i] not in seenX:
            seenX.add(newX[i])
        else:
            dupesX.append(i)
        if newY[i] not in seenY:
            seenY.add(newY[i])
        else:
            dupesY.append(i)
    for i in dupesX:
        newX[i] = notX.pop()
    for i in dupesY:
        newY[i] = notY.pop()
    tourX = 0
    tourY = 0
    for i in range(-1,num_cities-1):
        tourX += distance_matrix[newX[i]][newX[i+1]]
        tourY += distance_matrix[newY[i]][newY[i+1]]
    if tourX <= tourY:
        return(Chrom(newX))
    else:
        return(Chrom(newY))

# Mutation as provided on lecture slides and spec
def mutateIP(chrom):
    posA = rd.randint(0,num_cities-1)
    posB = rd.randint(0,num_cities-1)
    temp = chrom.tour[posA]
    chrom.tour[posA] = chrom.tour[posB]
    chrom.tour[posB] = temp
    chrom.calcFit()
    return

def mutate(chrom):
    tour = [c for c in chrom.tour] 
    posA = rd.randint(0,num_cities-1)
    posB = rd.randint(0,num_cities-1)
    temp = tour[posA]
    tour[posA] = tour[posB]
    tour[posB] = temp
    return Chrom(tour)

def mutateSub(chrom):
    tour = [c for c in chrom.tour] 
    pos = rd.randint(0,num_cities-1)
    tour[pos:pos+30] = tour[pos:pos+30][::-1]
    return Chrom(tour)

def greedyChrom():
    city = rd.randint(0,num_cities-1)
    noVisit = []
    tour = [city]
    cities = 1
    # Iterates through unvisited cities, picking nearest as next destination
    while cities != num_cities:
        distances = [c for c in distance_matrix[city]]
        # Ignores distances to visited cities by making them infinite
        for i in tour:
            distances[i] = math.inf
        smallest = min(distances)
        city = distances.index(smallest)
        tour.append(city)
        cities += 1
    return Chrom(tour)

def heurCost():
    # Figures out unvisited cities
    noVisit = [c for c in range(num_cities) if c not in self.set]
    city = self.tour[-1]
    length = self.length
    heur = 0
    # Loops until full tour found
    while length != num_cities:
        # Makes a dictionary of neighbour:distance to neighbour
        distances = {c:distance_matrix[city][c] for c in noVisit}
        # Picks nearest neighbour as next city
        city = min(distances,key=distances.get)
        noVisit.remove(city)
        heur += distances[city]
        length += 1
    # Joins up start and end cities
    heur += distance_matrix[city][0]
    return heur

# Terminate after either 2 minutes,
# or no improvement in fitness for a few generations

start = time.time()
TIME_LIMIT = 99999999999 # 115 seconds

pop = []
popSize = 75
for i in range(popSize):
    hp.heappush(pop,Chrom(rd.sample(citySet,num_cities)))
    #hp.heappush(pop,greedyChrom())
best = pop[0]
#rd.shuffle(pop)
gen = -1
sumFit = sum([c.f for c in pop])
prob = 0.05
generations = 3000

for i in range(generations):
    newPop = []
    for j in range(popSize):
        if rd.uniform(0,1) < prob:
            #child = mutateSub(roulette())
            child = mutate(roulette())
        else:
            child = crossover(roulette(),roulette())
        hp.heappush(newPop,child)
    if newPop[0] < best:
        best = newPop[0]
        gen = i
    if time.time() >= start + TIME_LIMIT:
        break
    pop = newPop
    #rd.shuffle(pop)
    sumFit = sum([c.f for c in pop])

end = time.time()
elapsed = end-start

print()
print("it took me",elapsed,"seconds to find:")
print(best)
print(gen)

tour = best.tour
tour_length = best.l

start = time.time()

# Performs the 2-opt algorithm
swapped = True
# Repeats until no swaps (improvements) made
while swapped == True:
    swaps = 0
    tourCopy = tour[:]
    # Tries each pair of cities
    for i in range(0,num_cities-2):
        for j in range(i+1,num_cities-1):
            # Reverses subsequence to simulate "uncrossing" overlapping edges
            newTour = revSub(tourCopy,i,j)
            # Calculates new tour length
            tourLen = 0
            for k in range(-1,num_cities-1):
                tourLen += distance_matrix[newTour[k]][newTour[k+1]]
            # If tour length improved, starts process again on new tour with swap
            if tourLen < tour_length:
                swaps += 1
                tour_length = tourLen
                tour = [c for c in newTour]
    if swaps == 0:
        swapped = False

end = time.time()
elapsed = end-start
print("it took an extra",elapsed,"s to improve to:")
print(tour,tour_length)



#######################################################################################################
############ the code for your algorithm should now be complete and you should have        ############
############ computed a tour held in the list "tour" of length "tour_length"               ############
#######################################################################################################

# you do not need to worry about the code below; that is, do not touch it

#######################################################################################################
############ start of code to verify that the constructed tour and its length are valid    ############
#######################################################################################################

check_tour_length = 0
for i in range(0,num_cities-1):
    check_tour_length = check_tour_length + distance_matrix[tour[i]][tour[i+1]]
check_tour_length = check_tour_length + distance_matrix[tour[num_cities-1]][tour[0]]
flag = "good"
if tour_length != check_tour_length:
    flag = "bad"
if flag == "good":
    print("Great! Your tour-length of " + str(tour_length) + " from your " + codes_and_names[alg_code] + " is valid!")
else:
    print("***** ERROR: Your claimed tour-length of " + str(tour_length) + "is different from the true tour length of " + str(check_tour_length) + ".")

'''
#######################################################################################################
############ start of code to write a valid tour to a text (.txt) file of the correct      ############
############ format; if your tour is not valid then you get an error message on the        ############
############ standard output and the tour is not written to a file                         ############
############                                                                               ############
############ the name of file is "my_user_name" + mon-dat-hr-min-sec (11 characters);      ############
############ for example, dcs0iasSep22105857.txt; if dcs0iasSep22105857.txt already exists ############
############ then it is overwritten                                                        ############
#######################################################################################################

if flag == "good":
    local_time = time.asctime(time.localtime(time.time()))   # return 24-character string in form "Tue Jan 13 10:17:09 2009"
    output_file_time = local_time[4:7] + local_time[8:10] + local_time[11:13] + local_time[14:16] + local_time[17:19]
                                                             # output_file_time = mon + day + hour + min + sec (11 characters)
    output_file_name = my_user_name + output_file_time + ".txt"
    f = open(output_file_name,'w')
    f.write("USER = " + my_user_name + " (" + my_first_name + " " + my_last_name + ")\n")
    f.write("ALGORITHM = " + alg_code + ", FILENAME = " + name_of_file + "\n")
    f.write("NUMBER OF CITIES = " + str(num_cities) + ", TOUR LENGTH = " + str(tour_length) + "\n")
    f.write(str(tour[0]))
    for i in range(1,num_cities):
        f.write("," + str(tour[i]))
    if added_note != "":
        f.write("\nNOTE = " + added_note)
    f.close()
    print("I have successfully written the tour to the output file " + output_file_name + ".")
    
'''