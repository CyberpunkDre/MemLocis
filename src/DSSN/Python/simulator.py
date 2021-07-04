#############################################################
##                                                         ##
## Re-implementation of Flexible Network Simulator project ##
## from my Distributed Sensor & System Networks class      ##
##                                                         ##
#############################################################

#############################################################
##                                                         ##
## Simulation engine                                       ##
## Inputs:                                                 ##
##      nodes = Initial struct containing nodes in field   ##
##      targets = Targets in field which will communicate  ##
##                via nodes                                ##
##      time = Time in seconds in run simulati             ##
##                                                         ##
## Output:                                                 ##
##      outDat = Unknown still                             ##
##                                                         ##
## Targets will randomly message each other every so often ##
##                                                         ##
#############################################################

# function [outData, t2Rx] = simulator(nodes, targets, time, time_div, tMax, maxRate)

## Libraries
import time
import math
import random

## Local Libraries
import nodeGen
import tarGen

# message = struct('id',{},'update',{},'expires',{},'payload',{},'nodeFrom',{})
class Message:

    def __init__(self, messageId = (0, 0), update = (0, 0), expires = 0, payload = None, nodeFrom = 0):
        self.messageId = messageId  # (timestamp, TargetId) : Note that index access is left to right index (timestamp = 0, TargetId = 1)
        self.update = update        # (update frequency, counter)
        self.expires = expires      #
        self.payload = payload      #
        self.nodeFrom = nodeFrom    #
        #    message(1).id = [t, mDest];                    % [timestamp, target destination]
        #    message(1).update = [100, 100];                % [Update frequency, counter]
        #    message(1).expires = t + 0.1/time_div;         % Interest expiration time, 1 second currently
        #    message(1).payload = pLoad;                    % Data payload
        #    message(1).nodeFrom = 0;                       % Used for back tracing later

    def getMsgId(self):
        return self.messageId

    def setMsgId(self, messageId):
        self.messageId = messageId

    def getPayloadCommand(self):
        return self.payload.getCommand()

    def getMsgExpires(self):
        return self.expires

    def setMsgExpires(self, expires):
        self.expires = expires

    def setNodeFrom(self, nodeId):
        self.nodeFrom = nodeId

    def getNodeFrom(self):
        return self.nodeFrom

    def shiftUpdate(self):
        self.update = (self.update[0], self.update[0])

    def getTargetId(self):
        return self.messageId[1]

    def getTimestamp(self):
        return self.messageId[0]

    def getUpdate(self):
        return self.update

    def setPayloadCommand(self, command):
        self.payload.setCommand(command)

    def setPayloadPosition(self, position):
        self.payload.setPosition(position)

    def setTimestamp(self, timestamp):
        self.messageId = (timestamp, self.messageId[1])

    def setUpdateRate(self, rate):
        self.update = (rate, self.update[1])

# messageQueue = struct('source',{},'dest',{},'nodeId',{},'targetId',{},'message',{})
class MessageQueue:

    def __init__(self):
        self.msgQueue = []
        self.nodeId = []
        self.targetId = []
        self.src = []
        self.dest = []
        self.timer = []
        self.size = 0

    def getMsgIndex(self, index):
        if(index < self.size):
            return self.msgQueue[index]

    def getSize(self):
        return self.size

    def tickTimerIndex(self, index):
        if(index < self.size):
            self.timer[index] = self.timer[index] - 1
        return self.timer[index]

    def getNodeIdIndex(self, index):
        if(index < self.size):
            return self.nodeId[index]

    def getTargetIdIndex(self, index):
        if(index < self.size):
            return self.targetId[index]

    def getSrcDestIndex(self, index):
        if(index < self.size):
            return (self.src[index], self.dest[index])

    def removeMsgIndex(self, index):
        self.msgQueue.remove(self.msgQueue[index])
        self.nodeId.remove(self.nodeId[index])
        self.targetId.remove(self.targetId[index])
        self.src.remove(self.src[index])
        self.dest.remove(self.dest[index])
        self.timer.remove(self.timer[index])
        self.size = self.size - 1

    def addMsgToQueue(self, src, dest, msg, nodeId, targetId, timer):
        self.msgQueue.append(msg)
        self.nodeId.append(nodeId)
        self.targetId.append(targetId)
        self.src.append(src)
        self.dest.append(dest)
        self.timer.append(timer)
        self.size = self.size + 1
        return self.size

#                               mInd = size(messageQueue, 2) + 1
#                               messageQueue(mInd).source   = curPos;
#                               messageQueue(mInd).dest     = nexPos;
#                               messageQueue(mInd).message  = sNew;
#                               messageQueue(mInd).nodeId   = intCur.sendTo;
#                               messageQueue(mInd).targetId = 0;
#                               messageQueue(mInd).timer    = randi(tMax);
    

# outData = struct('time',{},'nodePosition',{},'targetPosition',{},'message',{})
class EventHistory:

    def __init__(self, startTime = 0, endTime = 0, timeDiv = 1):
        self.startTime = startTime      # Float
        self.endTime = endTime          # Float
        self.timeDiv = timeDiv          # Float
        self.time = []                  # Ordered List of Floats
        self.nodePositions = []         # Ordered List of Lists of Tuples of Floats 
                                        # [ [(0,0), (0,0), (0,0)], [(1,1), (1,1), (1,1)], ... ]
        self.targetPositions = []       # Ordered List of Lists of Tuples of Floats 
                                        # [ [(0,0), (0,0), (0,0)], [(1,1), (1,1), (1,1)], ... ]
        self.messages = []              # Ordered List of Lists of Tuples of Floats 
                                        # [ [(0,0), (0,0), (0,0)], [(1,1), (1,1), (1,1)], ... ]
        self.eventCount = -1            # Int (Index for above ordered lists) (Steps with simulation increments)
        # Single Event = time[x], nodePositions[x], targetPositions[x], messages[x]

        self.initialize()
        self.realTimestamp = time.time()

    # Sets up structures and first event entry with empty slots to be overwritten in first *recordEvents()* method call
    def initialize(self):
        self.eventCount = 0
        self.extendStructures()

    # Reusable empty appender to the Lists of this class
    def extendStructures(self):
        self.time.append(0)
        self.messages.append([])
        self.nodePositions.append([])
        self.targetPositions.append([])

    # Record - Enter nodePositions, targetPositions, and messages for current eventCount/iteration/time, then increment eventCount
    #        - Returns event index of recorded information
    def recordEvents(self, nodePositions, targetPositions, messages):
        currentIndex = self.eventCount
        self.time[currentIndex] = self.eventCount
        self.messages[currentIndex] = messages
        self.nodePositions[currentIndex] = nodePositions
        self.targetPositions[currentIndex] = targetPositions
        self.extendStructures()
        self.eventCount = currentIndex + 1
        if(len(messages) > 0):
            print("--------------------------------------------------------------------------------------------------------------------------")
            print("Iteration runtime = %f" % (time.time() - self.realTimestamp))
            print("Time = %d, msgs = %d, nodes = %d, targets = %d" % ( currentIndex, len(messages), len(nodePositions), len(targetPositions)) )
        self.realTimestamp = time.time()
        return currentIndex

    # Append - Add message at current *eventCount* index with given message
    def appendMsg(self, message):
        self.messages[self.eventCount].append(message)

    # Overwrite

# interest = struct('id',{},'update',{},'expires',{},'sendBack',{},'sendTo',{})
class Interest:

    def __init__(self, interestId = (0, 0), update = (0,0), expires = 0, sendBack = 0, sendTo = 0):
        self.interestId = interestId    # (timestamp, targetId)
        self.update = update
        self.update = (self.update[0], 0)
        self.expires = expires
        self.sendBack = sendBack
        self.sendTo = sendTo

    def getInterestId(self):
        return self.interestId

    def getInterestExpires(self):
        return self.getInterestExpires

    def updateInterestIdExpires(self, timestamp, expires):
        self.interestId = (timestamp, self.interestId[1])
        self.expires = expires

    def checkSendTo(self):
        if(self.sendTo != 0):
            return True
        return False

    def getSendTo(self):
        return self.sendTo

    def getSendBack(self):
        return self.sendBack

    def setInterestTimestamp(self, timestamp):
        self.interestId = (timestamp, self.interestId[1])

    def setUpdate(self, update):
        self.update = update

    def getInterestIdTarget(self):
        return self.interestId[1]

    def getInterestUpdateCount(self):
        return self.update[1]

    def shiftUpdate(self):
        self.update = (self.update[0], self.update[0])

    def getUpdate(self):
        return self.update

    def getExpires(self):
        return self.expires

    def tickUpdateTimer(self):
        self.update = (self.update[0], self.update[1] - 1)

# pLoad = struct('command',{},'position',{})
class Payload:

    def __init__(self, command = None, position = None):
        self.command = command
        self.position = position

    def getCommand(self):
        return self.command

    def setCommand(self, command):
        self.command = command

    def setPosition(self, position):
        self.position = position

class Simulator:

    def __init__(self, nodes, targets, time, timeDiv, tMax, maxRate):

        self.msgQueue = MessageQueue()

# iterations = floor( time / time_div ) # Current step time every time_div
        self.iterations = math.floor( time / timeDiv)
        self.timeDiv = timeDiv

# outData = struct('time',{},'nodePosition',{},'targetPosition',{},'message',{})
        self.eventHistory = EventHistory(0, time, timeDiv)

        # NodeGen Output
        self.nodes = nodes

        # TarGen Output
        self.targets = targets

        # max milliseconds possible delay
        self.tMax = tMax

        # update frequency in milliseconds
        self.maxRate = maxRate

        self.t2Rx = 0

    def checkXorYGreater(self, pos1, pos2):
        if ( (pos1[0] > pos2[0]) or (pos1[1] > pos2[1]) ):
            return True
        return False

    def checkXorYLesser(self, pos1, pos2):
        if ( (pos1[0] < pos2[0]) or (pos1[1] < pos2[1]) ):
            return True
        return False

    def getPosList(self, objList):
        returnList = []
        for nodeOrTar in objList:
            returnList.append(nodeOrTar.getPos())
        return returnList

    def recordInitialPositions(self):
        initialMessages = []
        eventCount = self.eventHistory.recordEvents(nodeGen.genNodePosList(self.nodes), \
                                                    nodeGen.genNodePosList(self.targets), \
                                                    initialMessages)
        return eventCount

    ##
    ## Walk messageQueue
    ##
    def iterateMessageQueue(self):

        msgQ = self.msgQueue.getSize()
        i = 0
        while( i < msgQ ):
            msg = self.msgQueue.getMsgIndex(i)
            timer = self.msgQueue.tickTimerIndex(i)
            if( timer == 0):
                nodeId = self.msgQueue.getNodeIdIndex(i)
                if( nodeId == 0):
                    self.targets[self.msgQueue.getTargetIdIndex(i)-1].addRxMsg(msg)
                else:
                    self.nodes[nodeId].addIncomingMsg(msg)
                self.eventHistory.appendMsg(self.msgQueue.getSrcDestIndex(i))
                self.msgQueue.removeMsgIndex(i)
                msgQ = msgQ - 1
            i = i + 1

    ##
    ## Handle Node events
    ##
    def handleNodeEvents(self, timestep):
        
        # Determine events for each nodes
        for i in range(0, len(self.nodes)):
            curNodePos = self.nodes[i].getPos() # (x, y)

            # Handle incoming messages
            incomSize = self.nodes[i].getIncomCount()

            for j in range(0, incomSize):
                mNew = self.nodes[i].getIncomMsg(j)
                sNew = mNew
                mId = mNew.getMsgId()
                cmdN = mNew.getPayloadCommand()

                # Ensure target is not already in vicinity
                # Ensure not an interest already else increase rate of
                match = 0
                for m in range(0, self.nodes[i].getInterestsCount()):
                    intCur = self.nodes[i].getInterests(m)
                    intId = intCur.getInterestId()

                    # If this message seeks the same target
                    if( mId[1] == intId[1] ):
                        match = 1
                        
                        # If timestamps are different
                        if( mId[0] != intId[0] ):

                            # If rate of interest is increased, only
                            # distribute to proven nodes
                            self.nodes[i].getInterests(m).updateInterestIdExpires(mId[0], mNew.getMsgExpires())
                            curPos = self.nodes[i].getPos()

                            if( intCur.checkSendTo() and mNew.getPayloadCommand() == 0):
                                sNew.setNodeFrom(i)
                                sendTo = intCur.getSendTo()
                                nexPos = self.nodes[sendTo].getPos()

                                if( ( cmdN ==  0 and self.checkXorYGreater(nexPos, curPos) ) or \
                                    ( cmdN == -1 and self.checkXorYLesser(nexPos, curPos) ) ):
                                    self.msgQueue.addMsgToQueue(curPos, nexPos, sNew, sendTo, 0, random.randint(1,self.tMax))

                            else:
                                if( mNew.getPayloadCommand() == -1 ): # Found target, return to requestor
                                    sBN = intCur.getSendBack()

                                    if ( sBN != 0):
                                        sNew.setNodeFrom(i) # Maybe redundant?
                                        nexPos = self.nodes[sBN].getPos()

                                        if( ( cmdN ==  0 and self.checkXorYGreater(nexPos, curPos) ) or \
                                            ( cmdN == -1 and self.checkXorYLesser(nexPos, curPos) ) ):
                                            self.msgQueue.addMsgToQueue(curPos, nexPos, sNew, sBN, 0, random.randint(1,self.tMax))
                                    else:
                                        tarInd = 0

                                        for q in range(0, len(self.targets)):
                                            tarPos = self.targets[q].getPos()
                                            dist = math.dist(tarPos, curPos)
                                            if dist <= self.nodes[i].getRange():
                                                tarInd = q

                                        tarPos = self.targets[tarInd].getPos()
                                        sNew.setNodeFrom(i)
                                        self.msgQueue.addMsgToQueue(curPos, tarPos, sNew, 0, tarInd, random.randint(1, self.tMax))

                                else:
                                    sendM = mNew
                                    lastNode = sendM.getNodeFrom()
                                    sendM.setNodeFrom(i)
                                    sendM.shiftUpdate()
                                    passedOn = 0
                                
                                    for h in range(0, len(self.nodes)):
                                        if( (h != i) and (h != lastNode) ):
                                            otherNode = self.nodes[h].getPos()
                                            dist = math.dist(otherNode, curPos)
                                            if( dist <= self.nodes[i].getRange() ):
                                                if( ( cmdN ==  0 and self.checkXorYGreater(otherNode, curPos) ) or
                                                    ( cmdN == -1 and self.checkXorYLesser(otherNode, curPos) ) ):
                                                    self.msgQueue.addMsgToQueue(curPos, otherNode, sendM, h, 0, random.randint(1, self.tMax))
                                                    passedOn = passedOn + 1

                                    if( passedOn == 0):
                                        tarId = mNew.getTargetId() - 1
                                        tarPos = self.targets[tarId].getPos()
                                        dist = math.dist(tarPos, curPos)

                                        if( dist <= self.nodes[i].getRange()):
                                            self.msgQueue.addMsgToQueue(curPos, tarPos, sendM, 0, tarId, random.randint(1, self.tMax))

                                    self.nodes[i].setInterestsId1(m, mNew.getTimestamp())

                            # Also update interest interval settings
                            self.nodes[i].setInterestsUpdate(m, mNew.getUpdate())

#                   # the timestamps and targets match == ignore, duplicate

#               # No match for target, create new interest
                if( match == 0):
                    self.nodes[i].addInterest( mNew.getMsgId(), mNew.getUpdate(), mNew.getMsgExpires(), mNew.getNodeFrom(), 0 )
                    curPos = self.nodes[i].getPos()

                    for m in range(0, len(self.nodes)):
                        otherPos = self.nodes[m].getPos()
                        dist = math.dist(otherPos, curPos)

                        if( (dist <= self.nodes[i].getRange()) and (i != m) and (m != mNew.getNodeFrom()) ):
                            if( ( cmdN ==  0 and self.checkXorYGreater(otherPos, curPos) ) or \
                                ( cmdN == -1 and self.checkXorYLesser(otherPos, curPos) ) ):
                                sNew.setNodeFrom(i)
                                self.msgQueue.addMsgToQueue(curPos, otherPos, sNew, m, 0, random.randint(1,self.tMax))

            # Clear incoming array
            self.nodes[i].clearIncoming()
        
            # Handle updating interests
            intSize = self.nodes[i].getNumInterests()
            for j in range(0, intSize):
                if( self.nodes[i].getInterestsUpdateCount(j) == 0 ):
                    self.nodes[i].shiftInterestsUpdate(j)
                    curNodePos = self.nodes[i].getPos()
                    tarIndex = self.nodes[i].getInterestsIdTarget(j)
                    targetPos = self.targets[tarIndex - 1].getPos()
                    dist = math.dist(targetPos, curNodePos)

                    if( dist <= self.nodes[i].getRange() ):
                        nPayload = Payload(0, targetPos)
                        nMessage = Message( (timestep, tarIndex), self.nodes[i].getInterestsUpdate(j), \
                            self.nodes[i].getInterestsExpires(j), nPayload, i)
                        self.msgQueue.addMsgToQueue(curNodePos, targetPos, nMessage, 0, tarIndex, random.randint(1, self.tMax))

                self.nodes[i].tickInterestsUpdateTimer(j)
                if( timestep == self.nodes[i].getInterestsExpires(j) ):
                    self.nodes[i].clearInterests(j)
                    intSize = intSize - 1
        
            # Log current node positions

    ##
    ## Handle Target events
    ##
    def handleTargetEvents(self, timestep):

        # Determine events for each target
        for i in range(0, len(self.targets)):
        
            # Reduce interval value
            if( self.targets[i].getInterval() != 0):
                self.targets[i].decInterval(self.timeDiv)

            # Time to send new message
            if( self.targets[i].getInterval() < self.timeDiv):
                mDest = self.targets[i].getTargetId()
                while( mDest == self.targets[i].getTargetId()):
                    mDest = random.randint(1, self.targets[i].getMaxTargets() )

                nPayload = Payload(0, (0,0))
                nMessage = Message( (timestep, mDest), (100, 100), timestep + 0.1/self.timeDiv, nPayload, 0)
                self.targets[i].addTxMsg(nMessage)
                targetPos = self.targets[i].getPos()
                sent = 0

                # Find nearby nodes and transmit message
                for m in range(0, len(self.nodes)):
                    nodePos = self.nodes[m].getPos()
                    dist = math.dist(nodePos, targetPos)
                    if( dist <= self.nodes[m].getRange()):
                        self.msgQueue.addMsgToQueue(targetPos, nodePos, nMessage, m, 0, random.randint(1, self.tMax))
                        sent = sent + 1

                if( sent == 0):
                    print("Message failed to send")

                self.targets[i].setInterval(10)

            rxN = self.targets[i].getRxSize()
        
            while( rxN >= 1):
                msg = self.targets[i].popRx(0) # Covers clearing this rx message later
                cmd = msg.getPayloadCommand()

                if( cmd == 0):
                    msg.setPayloadCommand(-1)
                    msg.setPayloadPosition(self.targets[i].getPos())
                    msg.setTimestamp(timestep)
                    nInd = msg.getNodeFrom()
                    nodePos = self.nodes[nInd].getPos()
                    self.msgQueue.addMsgToQueue( self.targets[i].getPos(), nodePos, msg, nInd, 0, random.randint(1, self.tMax) )
                    self.targets[i].addTxMsg(msg)

                if( cmd == -1):
                    msg.setPayloadCommand(0)
                    msg.setPayloadPosition(self.targets[i].getPos())
                    msg.setTimestamp(timestep)
                    nInd = msg.getNodeFrom()
                    nodePos = self.nodes[nInd].getPos()
                    msg.setMsgExpires(timestep + 0.2/self.timeDiv)
                    rate = msg.getUpdate()[0]
                    if( rate >= (self.maxRate + 10) ):
                        msg.setUpdateRate(rate - 10)
                    else:
                        msg.setUpdateRate(self.maxRate)
                        
                    self.msgQueue.addMsgToQueue( self.targets[i].getPos(), nodePos, msg, nInd, 0, random.randint(1, self.tMax))
                    self.targets[i].addTxMsg(msg)

                rxN = rxN - 1
                if (i == 2):
                    self.t2Rx = self.t2Rx + 1

            # Update target position
            self.targets[i].updateTargetPosition()
        
            # Log current target positions
    ##
    ## Start/Main method of Simulator
    ##
    def run(self):

        self.t2Rx = 0
        initialEventCount = self.recordInitialPositions() + 1

        # Begin Simulation
        for t in range(int(initialEventCount), int(self.iterations)):

            self.iterateMessageQueue()

            self.handleNodeEvents(t)

            self.handleTargetEvents(t)

            self.eventHistory.recordEvents( \
                nodePositions   = self.getPosList(self.nodes),    \
                targetPositions = self.getPosList(self.targets),    \
                messages        = [] \
            )
            #print("t = %4d" % t)
        
        print("Run end")
        
        return (self.eventHistory, self.t2Rx)