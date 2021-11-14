#8 queen problem   
import random
import copy
import math
import time

#Number of diagonals = (nDimension*2-3)*2

class BoardPageState:

    def __init__(self, boardPage):
        self.boardPage = boardPage
        self.dimension = len(self.boardPage)
        self.checkAttacks()
        self.setHeuristic()

    def checkAttack(self):
        rows = {};
        positiveDiagonals = {};
        negativeDiagonals = {};

        for i in range(self.dimension):
            rows[i]=0

        for i in range(self.dimension*2-3):
            positiveDiagonals[i] = 0
            negativeDiagonals[-i] = 0

        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.boardPage[i][j]:
                    rows[i] += 1

        for i in range(1,self.dimension*2-3):
            if i >= self.dimension-1:
                a = self.dimension-1
                b = 1 + (i - self.dimension - 1)
                while(a<=1):
                    if self.boardPage[a][b]:
                        positiveDiagonals[i] +=1
                    a -= 1
                    b += 1
            else:
                a = i
                b = 0
                while(a>=0):
                    if self.boardPage[a][b]:
                        positiveDiagonals[i] +=1
                    a -= 1
                    b += 1

        for i in range(self.dimension*2-3,0,-1):

            if i >= self.dimension-1:
                a = self.dimension-1
                b = 1 + (i - self.dimension - 1)
                while(a<=1):
                    if self.boardPage[b][a]:
                        negativeDiagonals[-i] +=1
                    a -= 1
                    b += 1
            else:
                a = i
                b = 0
                while(a>=0):
                    if self.boardPage[b][a]:
                        negativeDiagonals[-i] +=1
                    a -= 1
                    b += 1
        self.dicRows = rows
        self.dicDiagonal1 = positiveDiagonals
        self.dicDiagonal2 = negativeDiagonals

    def checkAttacks(self):
        #function is used to check if queens are in same row or diagonal
        rows = {}
        diagonal1 = {}
        diagonal2 = {}
        for i in range(self.dimension):
            rows[i] = 0
            for j in range(self.dimension):
                diagonal1[i-j] = 0
                diagonal2[i+j] = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.boardPage[i][j]:
                    rows[i] += 1
                    diagonal1[i-j] += 1
                    diagonal2[j+i] += 1
        self.dicRows = rows
        self.dicDiagonal1 = diagonal1
        self.dicDiagonal2 = diagonal2

    def setHeuristic(self):
        #Heuristic is number of pairs attacking each other
        h = 0
        for key in self.dicRows:
            if self.dicRows[key] > 1:
                h += self.dicRows[key]*(self.dicRows[key]-1)/2
        for key in self.dicDiagonal1:
            if self.dicDiagonal1[key] > 1:
                h += self.dicDiagonal1[key]*(self.dicDiagonal1[key]-1)/2
        for key in self.dicDiagonal2:
            if self.dicDiagonal2[key] > 1:
                h += self.dicDiagonal2[key]*(self.dicDiagonal2[key]-1)/2
        self.h = h

    def getSteepestAscent(self):
        neighbors = []
        huristic = float("inf")
        for j in range(self.dimension):
            for i in range(self.dimension):
                if self.boardPage[i][j] == 1:
                    ikeep = i
                    break
            for i in range(self.dimension):
                if self.boardPage[i][j] == 0:
                    newCheck = copy.deepcopy(self.boardPage)
                    newCheck[i][j] = 1
                    newCheck[ikeep][j] = 0
                    neighbor = BoardPageState(newCheck)
                    if neighbor.h < huristic:
                        neighbors[:] = []
                        huristic = neighbor.h
                    if neighbor.h == huristic:
                        neighbors.append(neighbor)
        global val
        lowest = float("inf")
        for x in neighbors:
            if (x.h < lowest):
                print("hello")
                lowest = x.h
                val = x

        return val     

    def getRandomSteepestAscent(self):
        neighbors = []
        huristic = float("inf")
        for j in range(self.dimension):
            for i in range(self.dimension):
                if self.boardPage[i][j] == 1:
                    ikeep = i
                    break
            for i in range(self.dimension):
                if self.boardPage[i][j] == 0:
                    newCheck = copy.deepcopy(self.boardPage)
                    newCheck[i][j] = 1
                    newCheck[ikeep][j] = 0
                    neighbor = BoardPageState(newCheck)
                    if neighbor.h < huristic:
                        neighbors[:] = []
                        huristic = neighbor.h
                    if neighbor.h == huristic:
                        neighbors.append(neighbor)
        return(random.choice(neighbors))

    def showChessboard(self):
        for values in self.boardPage:
            print("|".join(map(str, values)))
            print("- "*self.dimension)

    def showMove(self,neighborBoard):
        move = 0
        for i in range(self.dimension):
            for j in range(self.dimension):
                if self.boardPage[i][j] != neighborBoard.boardPage[i][j]:
                    if neighborBoard.boardPage[i][j] == 1:
                        xfinal=i
                        yfinal=j
                        move += 1
                    else:
                        xInitial = i
                        yInitial = j
                        move +=1
                    if move==2:
                        print("Move is made from ({0},{1}) Coordinates to ({2},{3})\n".format(xInitial,yInitial,xfinal,yfinal))
                        break
    

def HillCLimbingSteepestAscent(InitialChessBoard):
    current = BoardPageState(InitialChessBoard)
    #print("start of hill climbing algorithm steepest ascent")
    counter = 0
    while 1:
        print("current chessBoard:")
        current.showChessboard()
        print("current state h:{0}\n".format(current.h))
        neighbor = current.getSteepestAscent()
        counter+=1
        if neighbor.h >= current.h:
            if current.h == 0:
                print("the hill climbing algorithm steepest ascent variant found a solution\n")
                print("Number of Steps taken {0}\n".format(counter))
                return True, counter
            else:
                print("FAILED: the hill climbing algorithm steepest ascent variant got stuck in local minimum\n")
                print("Number of Steps taken {0}\n".format(counter))
                return False, counter
        current.showMove(neighbor)
        current = neighbor

def stochasticHillClimbing(InitialChessBoard):
    current = BoardPageState(InitialChessBoard)
    #print("start of hill climbing algorithm first choice variant")
    counter = 0
    while 1:
        print("current state chessBoard:")
        current.showChessboard()
        print("current state h:", current.h)
        neighbor = current.getRandomSteepestAscent()
        counter+=1
        if neighbor is None:
            if current.h == 0:
                print("the hill climbing algorithm first choice variant found a solution")
                print("Number of steps taken {0}\n".format(counter))
                return True, counter
            else:
                print("the hill climbing algorithm first choice variant got stuck in local minimum")
                print("Number of steps taken {0}\n".format(counter))
                return False, counter
        current.showMove(neighbor)
        current = neighbor


def createRandomChessBoard(nDimension):
    #generate nDimension random numbers:
    randomlist = random.sample(range(0,nDimension),k=nDimension)
    chessboard = [[0 for _ in range(nDimension)] for _ in range(nDimension)]
    #put queens on chessboard:
    for i in range(nDimension):
        chessboard[i][randomlist[i]]=1

    return chessboard


failureSteps = 0
successSteps = 0
numberFailure = 0
numberSuccess = 0
totaltime = 0

for i in range(10):
    randomBoard = createRandomChessBoard(8)
    print("-----------------******************----------------")
    startHillSteep = time.time()
    success,steps = HillCLimbingSteepestAscent(randomBoard)
    #success,steps = stochasticHillClimbing(randomBoard)
    if success :
        numberSuccess += 1
        successSteps += steps
    else:
        numberFailure += 1
        failureSteps += steps
    endHillSteep = time.time()
    totaltime += (endHillSteep - startHillSteep)
    print("run time of hill climbing steepest ascent {0}\n".format(endHillSteep - startHillSteep))
    print("-----------------******************----------------")

print("Number of successes {0}\n".format(numberSuccess))
if numberSuccess:
    print("Number of average steps per success {0}\n".format(successSteps/numberSuccess))
print("Number of Failures {0}\n".format(numberFailure))
if numberFailure:
    print("Number of steps per Failure {0}\n".format(failureSteps/numberFailure))
print("Total Time Taken for 1000 randomly generated boards {0}\n".format(totaltime))