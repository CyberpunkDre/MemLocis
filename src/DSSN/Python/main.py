#############################################################
##                                                         ##
## Re-implementation of Flexible Network Simulator project ##
## from my Distributed Sensor & System Networks class      ##
##                                                         ##
#############################################################

# Libraries
import numpy as np

# Local Libraries
import nodeGen
import tarGen
import simulator as simGen

# Parameters
xLen = 100.0        # m
yLen = 100.0        # m
nodeRange  = 15     # m
nodeNumber = 10     # units
targetNumber = 2    # units
targetSpeed  = 15   # m/s
timeDiv = 10**-3    # s (per iteration)
timeSim = 2.5       # s
tMax    = 3         # max milliseconds possible delay
maxRate = 30        # update frequency in milliseconds
method  = 1         # Node generation method
                    # 0 = basic
                    # 1 = grid
                    # 2 = random

field = [xLen, yLen]

powP = np.zeros(100)

def main():

    fails = 0
    mMsg = 0
    mPow = 0
    
    for i in range(1,101):
        #
        # Node Gen
        # nodes = nodeGen(field, nodeNumber, nodeRange, method)
        nodes = nodeGen.genNodes(xLen, yLen, nodeNumber, nodeRange, 'GRID')
        #nodes = nodeGen.genNodes(100, 100, 5, 10, 'PRESET')
        #nodes = nodeGen.genNodes(100, 100, 10, 40, 'RANDOM')
        
        # Target Gen
        # targets = tarGen(field, targetNumber, targetSpeed, timeDiv)
        targets = tarGen.genTar(xLen, yLen, targetNumber, targetSpeed, timeDiv)
    
        # [eventLog, t2Rx] = simulator(nodes, targets, timeSim, timeDiv, tMax, maxRate)
        simulator = simGen.Simulator(nodes, targets, timeSim, timeDiv, tMax, maxRate)
        (eventLog, t2Rx) = simulator.run()

        # if t2Rx == 0
        #     fails = fails + 1;
        # else
        #     [mSent, pUsed] = eventPlotter(eventLog, 0)
        #     mMsg = mMsg + mSent
        #     mPow = mPow + pUsed
        #     powP = pUsed
        if( t2Rx == 0):
            fails = fails + 1
        #else:
            #eventPlotter

        print("Run Num = %3d" % i)

    mMsg = mMsg / (100 - fails)
    mPow = mPow / (100 - fails)

    print("Mean messages sent = %5.3f" % mMsg)
    print("Mean power used = %5.4f" % mPow)
    print("Failures = %3d" % fails)

    # figure(1)
    # hold on
    # plot(1:100, powP)


if __name__ == '__main__':
    main()