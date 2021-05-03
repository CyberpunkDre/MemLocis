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
##      field   = [x y] field size (m m)                   ##
##      number  = number of targets in field               ##
##      speed   = velocity through the field (m/s)         ##
##      timeDiv = time increments for simulation engine    ##
##                                                         ##
## Output:                                                 ##
##      outTar   = output struct of targets                ##
##               = struct( 'x', {}, 'y', {} )              ##
##                                                         ##
## Construct data structure containing targets and their   ##
## parameters                                              ##
##                                                         ##
## Function:                                               ##
##      outTar = tarGen(field, number, speed, timeDiv)     ##
##                                                         ##
#############################################################

## Libraries
import random

class TargetObj:

    def __init__(self, x = 0, y = 0, targetId = 0, maxTarget = 0, interval = 0, vel = [0, 0], tx = {}, rx = {}):
        self.x = x
        self.y = y
        self.targetId = targetId
        self.maxTarget = maxTarget
        self.interval = interval
        self.vel = vel
        self.tx = tx
        self.rx = rx

    def setX(self, x = 0):
        self.x = x

    def setY(self, y = 0):
        self.y = y

    def setVel(self, vel = [0, 0]):
        self.vel = vel

    def getVel(self):
        return self.vel

    def getVelIndex(self, index = 0):
        return self.vel[index]

    def setInterval(self, interval = 0):
        self.interval = interval

    def getInterval(self):
        return self.interval

    def decInterval(self, decrement):
        self.interval = self.interval - decrement

    def addRxMsg(self, msg):
        self.rx.append(msg)

    def addTxMsg(self, msg):
        self.tx.apppend(msg)

    def getPos(self):
        return (self.x, self.y)

    def getTargetId(self):
        return self.targetId

    def getMaxTargets(self):
        return self.maxTarget

    def getRxSize(self):
        return len(self.rx)

    def popRx(self, index):
        return self.rx.pop(index)

    def updateTargetPosition(self):
        self.x = self.x + self.vel[0]
        self.y = self.y + self.vel[1]

    def __repr__(self):
        return "Target %d at (%3.2f, %3.2f)" % (self.targetId, self.x, self.y)

    def __str__(self):
        return "Target = %d\n(x,y) = (%3.2f, %3.2f)\nVelocity = (%3.2f, %3.2f)\nInterval = %d" % (self.targetId, self.x, self.y, self.vel[0], self.vel[1], self.interval)

def genTar(xLimit = 1.0, yLimit = 1.0, numTargets = 2, speed = 0, timeDiv = 1):
    
    returnList = []

    for i in range(1, numTargets + 1):
        newTarget = TargetObj( random.randint(1, xLimit), random.randint(1, yLimit), i, numTargets, i)
#       deg = randi(360)
#       xSpeed = (speed * timeDiv) * sin(deg)
#       ySpeed = (speed * timeDiv) * cos(deg)
        newTarget.setVel( [0, speed * timeDiv] )
        returnList.append(newTarget)

    returnList[0].setX(20)
    returnList[0].setY(20)
    returnList[1].setX(90)
    returnList[1].setY(90)
    returnList[1].setVel( [0, -returnList[0].getVelIndex(1) ] )
    returnList[1].setInterval(5)

    return returnList

if __name__ == '__main__':
    print("Running tarGen.py standalone to test generation.")
    targetList = genTar(100.0, 100.0, 3, 10, 2)
    for target in targetList:
        print("-----------------------")
        print(target)