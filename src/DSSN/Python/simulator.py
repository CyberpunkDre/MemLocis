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

## Libraries
import math

class EventHistory:

    def __init__(self, startTime = 0, endTime = 0, timeDiv = 1):
        self.startTime = startTime
        self.endTime = endTime
        self.timeDiv = timeDiv
        self.time = []
        self.nodePositions = []
        self.targetPositions = []
        self.messages = []

    def addTimeEntry(self, time):
        self.time.append(time)

    def addNodePosition(self, iteration, nodeXY):
        if(iteration >= len(self.nodePositions)):
            self.nodePositions.append([nodeXY])
        else:
            self.nodePositions[iteration - 1].append(nodeXY)

class Interest:

    def __init__(self, interestId = 0, update = 0, expires = 0, sendBack = 0, sendTo = 0):
        self.interestId = interestId
        self.update = update
        self.expires = expires
        self.sendBack = sendBack
        self.sendTo = sendTo

class Payload:

    def __init__(self, command = None, position = None):
        self.command = command
        self.position = position

class Message:

    def __init__(self, messageId = 0, update = 0, expires = 0, payload = None, nodeFrom = 0):
        self.messageId = messageId
        self.update = update
        self.expires = expires
        self.payload = payload
        self.nodeFrom = nodeFrom
        self.timer = timer

class MessageQueue:

    def __init__(self):
        self.queue = []
        # source
        # dest
        # nodeId
        # targetId

    def addMsg(self, msg):
        self.queue.append(msg)



class Simulator:

    def __init__(self, nodes, targets, time, timeDiv, tMax, maxRate):
        self.msgQueue = MessageQueue()
        self.iteration = math.floor( time / timeDiv)

        self.eventHistory = EventHistory(0, time, timeDiv)

        self.t2Rx = 0

    def recordInitialPositions(self):


    def run(self):
        self.t2Rx = 0








# function [outData, t2Rx] = simulator(nodes, targets, time, time_div, tMax, maxRate)

# iterations = floor( time / time_div ) # Current step time every time_div
# outData = struct('time',{},'nodePosition',{},'targetPosition',{},'message',{})
# message = struct('id',{},'update',{},'expires',{},'payload',{},'nodeFrom',{})
# interest = struct('id',{},'update',{},'expires',{},'sendBack',{},'sendTo',{})
# pLoad = struct('command',{},'position',{})

# messageQueue = struct('source',{},'dest',{},'nodeId',{},'targetId',{},'message',{})

# outData(1).time = 0
# t2Rx = 0
# for i in range(1, size(nodes,2) ):
#   # Log initial nodes positions
#   outData(1).nodePosition{i} = [nodes(i).x, nodes(i).y]
# for i in range(1, size(targets,2) ):
#   # Log initial target positions
#   outData(1).targetPosition{i} = [targets(i).x, targets(i).y]

# Begin Simulation
# for t in range(2, (iterations + 1) ):
#
#   outData(t).time = (t - 1) * time_div
#   
#   msgQ = size(messageQueue, 2)
#   i = 1
#   k = 1
#   while ( i <= msgQ ):
#       src  = messageQueue(i).source
#       dest = messageQueue(i).dest
#       msg  = messageQueue(i).message
#       nId  = messageQueue(i).nodeId
#       tId  = messageQueue(i).targetId
#       count = messageQueue(i).timer - 1
#       if count == 0:
#           if nId == 0:
#               targets(tId).rx{ size(targets(tID).rx, 2) + 1 } = msg
#           else:
#               nodes(nId).incoming{ size(nodes(nId).incoming, 2) + 1 } = msg
#           outData(t).message{k} = [src, dest];
#           messageQueue(i) = []
#           msgQ = msgQ - 1
#           k = k + 1
#       else:
#           messageQueue(i).timer = count
#           i = i + 1
#
#   # Determine events for each nodes
#   for i in range( 1, size(nodes,2) ):
#       curNodePos = [nodes(i).x, nodes(i).y]
#       # Handle incoming messages
#       incomSize = size( nodes(i).incoming, 2 )
#       for j in range(1, incomSize + 1):
#           mNew = nodes(i).incoming{j}
#           sNew = mNew
#           mId = mNew.id
#           cmdN = mNew.payload.command
#           # Ensure target is not already in vicinity
#           # Ensure not an interest already else increase rate of
#           match = 0
#           for m in range(1, size(nodes(i).interests, 2)):
#               intCur = nodes(i).interests(m)
#               intId = intCur.id
#               # If this message seeks the same target
#               if mId(2) == intId(2):
#                   match = 1
#                   # If timestamps are different
#                   if mId(1) ~= intId(1):
#                       # If rate of interest is increased, only
#                       # distribute to proven nodes
#                       nodes(i).interests{m}.id(1) = mNew.id(1)
#                       nodes(i).interests{m}.expires = mNew.expires
#                       curPos = [nodes(i).x, nodes(i).y]
#                       if ( intCur.sendTo ~= 0 and mNew.payload.command == 0):
#                           sNew.nodeFrom = i
#                           nexPos = [nodes(intCur.sendTo).x, nodes(intCur.sendTo).y]
#                           if ( ( cmdN == 0) and ( ( nexPos(1) > curPos(1) ) or ( nexPos(2) > curPos(2) ) ) )
#                               or ( ( cmdN == -1) and ( (nexPos(1) < curPos(1)) or (nexPos(2) < curPos(2)) ) ):
#                               
#                               mInd = size(messageQueue, 2) + 1
#                               messageQueue(mInd).source   = curPos;
#                               messageQueue(mInd).dest     = nexPos;
#                               messageQueue(mInd).message  = sNew;
#                               messageQueue(mInd).nodeId   = intCur.sendTo;
#                               messageQueue(mInd).targetId = 0;
#                               messageQueue(mInd).timer    = randi(tMax);
#                           else:
#                               if mNew.payload.command == -1: # Found target, return to requestor
#                                   sBN = intCur.sendBack
#                                   nodes(i).interests{m}.sendTo = mNew.nodeFrom
#                                   if sBN ~= 0:
#                                       sNew.nodeFrom = i
#                                       nexPos = [nodes(sBN).x, nodes(sBN).y]
#                                       if ( ( cmdN == 0) and ( ( nexPos(1) > curPos(1) ) or ( nexPos(2) > curPos(2) ) ) )
#                                           or ( ( cmdN == -1) and ( (nexPos(1) < curPos(1)) or (nexPos(2) < curPos(2)) ) ):
#                                           
#                                           mInd = size(messageQueue, 2) + 1
#                                           messageQueue(mInd).source   = curPos
#                                           messageQueue(mInd).dest     = nexPos
#                                           messageQueue(mInd).message  = sNew
#                                           messageQueue(mInd).nodeId   = sBN
#                                           messageQueue(mInd).targetId = 0
#                                           messageQueue(mInd).timer    = randi(tMax)
#                                   else:
#                                       tarInd = 1;
#                                       for q = 1:size(targets,2)
#                                           tarPos = [targets(q).x, targets(q).y];
#                                           dist = norm(tarPos - curPos);
#                                           if dist <= nodes(i).range
#                                               tarInd = q;
#                                       tarPos = [targets(tarInd).x, targets(tarInd).y];
#                                       sNew.nodeFrom = i;
#                                       mInd = size(messageQueue, 2)+1;
#                                       messageQueue(mInd).source = curPos;
#                                       messageQueue(mInd).dest = tarPos;
#                                       messageQueue(mInd).message = sNew;
#                                       messageQueue(mInd).nodeId = 0;
#                                       messageQueue(mInd).targetId = tarInd;
#                                       messageQueue(mInd).timer = randi(tMax);
#                               else
#                                   sendM = mNew;
#                                   lastNode = sendM.nodeFrom;
#                                   sendM.nodeFrom = i;
#                                   sendM.update(2) = sendM.update(1);
#                                   passedOn = 0;
#                                   for h in range(1, size(nodes,2) + 1):
#                                       if h ~= i && h~= lastNode:
#                                           otherNode = [nodes(h).x, nodes(h).y];
#                                           dist = norm(otherNode - curPos);
#                                           if dist <= nodes(i).range:
#                                              if ((cmdN == 0)&&((otherNode(1)>curPos(1))||(otherNode(2)>curPos(2)))) || ((cmdN==-1)&&((otherNode(1)<curPos(1))||(otherNode(2)<curPos(2)))):
#                                                 mInd = size(messageQueue, 2)+1;
#                                                 messageQueue(mInd).source = curPos;
#                                                 messageQueue(mInd).dest = otherNode;
#                                                 messageQueue(mInd).message = sendM;
#                                                 messageQueue(mInd).nodeId = h;
#                                                 messageQueue(mInd).targetId = 0;
#                                                 messageQueue(mInd).timer = randi(tMax);
#                                                 passedOn = passedOn + 1;
#                                   if passedOn == 0:
#                                        tarId = mNew.id(2);
#                                        tarPos = [targets(tarId).x, targets(tarId).y];
#                                        dist = norm(tarPos - curPos);
#                                        if dist <= nodes(i).range
#                                            mInd = size(messageQueue, 2)+1;
#                                            messageQueue(mInd).source = curPos;
#                                            messageQueue(mInd).dest = tarPos;
#                                            messageQueue(mInd).message = sendM;
#                                            messageQueue(mInd).nodeId = 0;
#                                            messageQueue(mInd).targetId = tarId;
#                                            messageQueue(mInd).timer = randi(tMax);

#                                   nodes(i).interests{m}.id(1) = mNew.id(1);

#                       # Also update interest interval settings
#                       nodes(i).interests{m}.update = mNew.update;
#                   # the timestamps and targets match == ignore, duplicate

#           if match == 0:
#               # No match for target, create new interest
#               interest(1).id = mNew.id;
#               interest(1).update = mNew.update;
#               interest(1).update(2) = 0;
#               interest(1).expires = mNew.expires;
#               interest(1).sendBack = mNew.nodeFrom;
#               interest(1).sendTo = 0;
#               nodes(i).interests{size(nodes(i).interests,2)+1} = interest;
#               curPos = [nodes(i).x, nodes(i).y];
#               for m in range(1, size(nodes,2) + 1):
#                   othePos = [nodes(m).x, nodes(m).y];
#                   dist = norm(othePos - curPos);
#                   if dist <= nodes(i).range && (i ~= m) && (m ~= interest(1).sendBack)
#                       if ((cmdN == 0)&&((othePos(1)>curPos(1))||(othePos(2)>curPos(2)))) || ((cmdN==-1)&&((othePos(1)<curPos(1))||(othePos(2)<curPos(2))))
#                           sNew.nodeFrom = i;
#                           mInd = size(messageQueue, 2)+1;
#                           messageQueue(mInd).source = curPos;
#                           messageQueue(mInd).dest = othePos;
#                           messageQueue(mInd).message = sNew;
#                           messageQueue(mInd).nodeId = m;
#                           messageQueue(mInd).targetId = 0;
#                           messageQueue(mInd).timer = randi(tMax);

#       # Clear incoming array
#       nodes(i).incoming = {};
        
#       # Handle updating interests
#       intSize = size(nodes(i).interests,2);
#       for j in range(1, intSize):
#           if nodes(i).interests{j}.update(2) == 0:
#               nodes(i).interests{j}.update(2) = nodes(i).interests{j}.update(1);
#               # Look for desired target
#               curNodePos = [nodes(i).x, nodes(i).y];
#               tarIndex = nodes(i).interests{j}.id(2);
#               targetPos = [targets(tarIndex).x, targets(tarIndex).y];
#               dist = norm(targetPos - curNodePos);
#               if dist<=nodes(i).range:  
#                   pLoad(1).command = 0;
#                   pLoad(1).position = targetPos;
#                   message(1).id = [t, nodes(i).interests{j}.id(2)];
#                   message(1).update = nodes(i).interests{j}.update;
#                   message(1).expires = nodes(i).interests{j}.expires;
#                   message(1).payload = pLoad;
#                   message(1).nodeFrom = i;                 
#                   mInd = size(messageQueue, 2)+1;
#                   messageQueue(mInd).source = curNodePos;
#                   messageQueue(mInd).dest = targetPos;
#                   messageQueue(mInd).message = message;
#                   messageQueue(mInd).nodeId = 0;
#                   messageQueue(mInd).targetId = tarIndex;
#                   messageQueue(mInd).timer = randi(tMax);

#           nodes(i).interests{j}.update(2) = nodes(i).interests{j}.update(2) - 1;
#           if t == nodes(i).interests{j}.expires
#               nodes(i).interests(j) = [];
#               intSize = intSize - 1;
        
#       # Log current node positions
#       outData(t).nodePosition{i} = curNodePos;

#   # Determine events for each target
#   for i in range(1, size(targets,2)):
        
#       # Reduce interval value
#       if targets(i).interval ~= 0
#           targets(i).interval = targets(i).interval - time_div;
        
#       # Time to send new message
#       if targets(i).interval < time_div:
#           mDest = targets(i).id;
#           while (mDest == targets(i).id):
#               mDest = randi(targets(i).max);
#
#           pLoad(1).command = 0;
#           pLoad(1).position = [0, 0];
#           message(1).id = [t, mDest];                    % [timestamp, target destination]
#           message(1).update = [100, 100];                % [Update frequency, counter]
#           message(1).expires = t + 0.1/time_div;         % Interest expiration time, 1 second currently
#           message(1).payload = pLoad;                    % Data payload
#           message(1).nodeFrom = 0;                       % Used for back tracing later
#           targets(i).tx{size(targets(i).tx,2)+1} = message;
#           targetPos = [targets(i).x, targets(i).y];
#           % Find nearby nodes and transmit message
#           sent = 0;
#           for m in range(1, size(nodes,2) + 1 ):
#               nodePos = [nodes(m).x, nodes(m).y];
#               dist = norm(nodePos - targetPos);
#               if dist <= nodes(m).range:
#                   mInd = size(messageQueue, 2)+1;
#                   messageQueue(mInd).source = targetPos;
#                   messageQueue(mInd).dest = nodePos;
#                   messageQueue(mInd).message = message;
#                   messageQueue(mInd).nodeId = m;
#                   messageQueue(mInd).targetId = 0;
#                   messageQueue(mInd).timer = randi(tMax);
#                   sent = sent + 1;

#           if sent == 0:
#               fprintf('Message failed to send\n');

#           targets(i).interval = 10;

#       rxN = size(targets(i).rx,2);
        
#       while (rxN >= 1):
#           msg = targets(i).rx{1};
#           cmd = msg.payload.command;
#           if cmd == 0:
#               msg.payload.command = -1;
#               msg.payload.position = [targets(i).x, targets(i).y];
#               msg.id(1) = t;
#               nInd = msg.nodeFrom;
#               nodePos = [nodes(nInd).x, nodes(nInd).y];
#               mInd = size(messageQueue, 2)+1;
#               messageQueue(mInd).source = [targets(i).x, targets(i).y];
#               messageQueue(mInd).dest = nodePos;
#               messageQueue(mInd).message = msg;
#               messageQueue(mInd).nodeId = nInd;
#               messageQueue(mInd).targetId = 0;
#               messageQueue(mInd).timer = randi(tMax);
#               targets(i).tx{size(targets(i).tx,2)+1} = msg;

#           if cmd == -1
#               msg.payload.command = 0;
#               msg.payload.position = [targets(i).x, targets(i).y];
#               msg.id(1) = t;
#               nInd = msg.nodeFrom;
#               nodePos = [nodes(nInd).x, nodes(nInd).y];
#               msg.expires = t + 0.2/time_div;
#               rate = msg.update(1);
#               if rate >= (maxRate + 10)
#                   msg.update(1) = rate - 10;
#               else
#                   msg.update(1) = maxRate;

#               mInd = size(messageQueue, 2)+1;
#               messageQueue(mInd).source = [targets(i).x, targets(i).y];
#               messageQueue(mInd).dest = nodePos;
#               messageQueue(mInd).message = msg;
#               messageQueue(mInd).nodeId = nInd;
#               messageQueue(mInd).targetId = 0;
#               messageQueue(mInd).timer = randi(tMax);
#               targets(i).tx{size(targets(i).tx,2)+1} = msg;

#           targets(i).rx(1) = [];
#           rxN = rxN - 1;
#           if i == 2
#               t2Rx = t2Rx + 1;
#  
#       # Update target position
#       targets(i).x = targets(i).x + targets(i).vel(1);
#       targets(i).y = targets(i).y + targets(i).vel(2);
        
#       # Log current target positions
#       outData(t).targetPosition{i} = [targets(i).x, targets(i).y];

#   # fprintf('t = %4d\n',t);
