#############################################################
##                                                         ##
## Re-implementation of Flexible Network Simulator project ##
## from my Distributed Sensor & System Networks class      ##
##                                                         ##
#############################################################

#############################################################
##                                                         ##
## Node generator                                          ##
## Inputs:                                                 ##
##      field  = [x y] field size                          ##
##      number = number of nodes generated                 ##
##      range  = Distance nodes can communicate            ##
##      method = Node generation method                    ##
##               0 = basic, 1 = grid, 2 = random           ##
##                                                         ##
## Output:                                                 ##
##      outNodes = Output struct of nodes                  ##
##               = struct( 'x', {}, 'y', {} )              ##
##                                                         ##
## Construct data structure containing nodes and their     ##
## capabilities                                            ##
##                                                         ##
## Function:                                               ##
##      outNodes = nodeGen(field, number, range, method)   ##
##                                                         ##
#############################################################

## Libraries
import math
import random
import numpy as np

## Local Libraries
import simulator

class NodeObj:

    # id -> nodeId and range -> commRange to avoid built-in Python functions
    def __init__(self, x = 0, y = 0, nodeId = 0, commRange = 40, incoming = [], interests = []):
        self.x = x
        self.y = y
        self.nodeId = nodeId
        self.commRange = commRange
        self.incoming = incoming
        self.interests = interests

    def setx(self, x = 0):
        self.x = x

    def sety(self, y = 0):
        self.y = y

    def getPos(self):
        return (self.x, self.y)

    def getRange(self):
        return self.commRange

    def addIncomingMsg(self, msg):
        self.incoming.append(msg)    

    def getIncomCount(self):
        return len(self.incoming)

    def getIncomMsg(self, index):
        return self.incoming[index]

    def getInterestsCount(self):
        return len(self.interests)

    def getInterests(self, index):
        return self.interests[index]

    def setInterestsId1(self, index, newId):
        self.interests[index].setInterestTimestamp(newId)

    def setInterestsUpdate(self, index, update):
        self.interests[index].setUpdate(update)

    def addInterest(self, interestId, update, expires, sendBack, sendTo):
        self.interests.append(simulator.Interest(interestId, update, expires, sendBack, sendTo))

    def clearIncoming(self):
        self.incoming = []

    def clearInterests(self, index):
        self.interests.remove(self.interests[index])

    def getNumInterests(self):
        return len(self.interests)

    def getInterestsIdTarget(self, index):
        return self.interests[index].getInterestIdTarget()

    def shiftInterestsUpdate(self, index):
        self.interests[index].shiftUpdate()

    def getInterestsUpdateCount(self, index):
        return self.interests[index].getInterestUpdateCount()

    def getInterestsUpdate(self, index):
        return self.interests[index].getUpdate()

    def getInterestsExpires(self, index):
        return self.interests[index].getExpires()

    def tickInterestsUpdateTimer(self, index):
        return self.interests[index].tickUpdateTimer()

    def __repr__(self):
        return "Node %d at (%3.2f, %3.2f)" % (self.nodeId, self.x, self.y)

    def __str__(self):
        return "Node ID = %d\n(x,y) = (%3.2f, %3.2f)\nRange = %3.2f" % (self.nodeId, self.x, self.y, self.commRange)

#
# Walks a List of NodeObj and returns a List of (NodeObj.x, NodeObj.y)
#
def genNodePosList(nodeList):
    
    returnList = []

    for node in nodeList:
        returnList.append(node.getPos())

    return returnList

#
# Generates an array of NodeObj of size *numNodes* with given commRange
#
def genNodeList(numNodes = 1, commRange = 1):

    returnList = []

    for i in range(1, numNodes + 1):
        newNode = NodeObj(0, 0, i, commRange, [], [])
        returnList.append(newNode)

    return returnList

#
# Generates an array of NodeObj with given commRange
# Number scales based on x/yLimits and scalar
#
def genGridNodeList(xLimit = 1.0, yLimit = 1.0, commRange = 1, scalar = 10):

    returnList = []

    xLim = int(math.floor( xLimit / scalar ))
    yLim = int(math.floor( yLimit / scalar ))
    k = 1

    for i in range(1, xLim):
        for j in range(1, yLim):
            newNode = NodeObj( i * scalar, j * scalar, k, commRange, [], [])
            returnList.append(newNode)
            k = k + 1

    return returnList

#
# Generates an array of NodeObj to match a preset given in original code
#
def genPresetNodeList():

    returnList = []

    returnList.append( NodeObj(25, 25, 1, 40, [], []) )
    returnList.append( NodeObj(50, 50, 2, 40, [], []) )
    returnList.append( NodeObj(75, 75, 3, 40, [], []) )
    returnList.append( NodeObj(50, 30, 4, 40, [], []) )
    returnList.append( NodeObj(30, 50, 5, 40, [], []) )

    return returnList
    
#
# Randomly shuffles (x,y) positions of given array of NodeObj
#
def shufflePosRandom(xLimit = 1.0, yLimit = 1.0, nodeList = []):

    for node in nodeList:
        randX = random.random() * xLimit
        node.setx(randX)
        randY = random.random() * yLimit
        node.sety(randY)

#
# Randomly shuffles (x,y) positions of given array of NodeObj following old code spacing rules
#
def shufflePosRandomSpacer(xLimit = 1.0, yLimit = 1.0, nodeList = []):

    posTracker = []
    i = 0
    for node in nodeList:
        randX = random.random() * xLimit
        randY = random.random() * yLimit
        
        posTracker.append([randX, randY])

        inRange = 0
        while (inRange == 0) and (i != 0):
            for j in range(0, i):
                dist = np.linalg.norm(np.array(posTracker[i]) - np.array(posTracker[j]))
                if dist <= node.getRange():
                    inRange = 1
                    j = i
                else:
                    randX = random.random() * xLimit
                    randY = random.random() * yLimit
                    posTracker[i] = [randX, randY]

        node.setx(randX)
        node.sety(randY)
        i = i + 1
#
# Generates a list of nodes with given parameters
#
def genNodes(xLimit = 1.0, yLimit = 1.0, numNodes = 1, commRange = 40, method = 'RANDOM'):

    returnNodeList = []

    if(method == 'RANDOM'):
        returnNodeList = genNodeList(numNodes, commRange)
        shufflePosRandom(xLimit, yLimit, returnNodeList)
    elif(method == 'GRID'):
        returnNodeList = genGridNodeList(xLimit, yLimit, commRange)
    elif(method == 'PRESET'):
        returnNodeList = genPresetNodeList()

    return returnNodeList

if __name__ == '__main__':
    
    print("Running nodeGen.py separately to test structure generation.")
    print("")
    print("Test #1: Preset Node Gen")
    print("xLimit = 100, yLimit = 100, numNodes = 5, commRange = 40, method = PRESET")
    NodeList1 = genNodes(100, 100, 5, 40, 'PRESET')
    print("Len of return node list = %d" % len(NodeList1))
    print("------------------------")
    for node in NodeList1:
        print(node)
        print("------------------------")
    print("")
    print("")
    print("Test #2: Grid Node Gen")
    print("xLimit = 100, yLimit = 100, numNodes = x, commRange = 10, method = GRID")
    NodeList2 = genNodes(100, 100, 5, 10, 'GRID')
    print("Len of return node list = %d" % len(NodeList2))
    print("------------------------")
    for node in NodeList2:
        print(node)
        print("------------------------")
    print("")
    print("")
    print("Test #3: Random Node Gen")
    print("xLimit = 100, yLimit = 100, numNodes = 50, commRange = 40, method = RANDOM")
    NodeList3 = genNodes(100, 100, 50, 40, 'RANDOM')
    print("Len of return node list = %d" % len(NodeList3))
    print("------------------------")
    for node in NodeList3:
        print(node)
        print("------------------------")
