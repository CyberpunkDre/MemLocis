#############################################################
##                                                         ##
## Re-implementation of Flexible Network Simulator project ##
## from my Distributed Sensor & System Networks class      ##
##                                                         ##
#############################################################

# Libraries
import numpy as np

# Parameters
xLen = 100          # m
yLen = 100          # m
nodeRange  = 15     # m
nodeNumber = 81     # m
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

mMsg = 0
mPow = 0
powP = np.zeros(100)
fails = 0

def main():

    for i in range(1,101):
        #
        # Node Gen
        # nodes = nodeGen(field, nodeNumber, nodeRange, method)
        #
        # Target Gen
        # targets = tarGen(field, targetNumber, targetSpeed, timeDiv)
    
        # [eventLog, t2Rx] = simulator(nodes, targets, timeSim, timeDiv, tMax, maxRate)

        # if t2Rx == 0
        #     fails = fails + 1;
        # else
        #     [mSent, pUsed] = eventPlotter(eventLog, 0)
        #     mMsg = mMsg + mSent
        #     mPow = mPow + pUsed
        #     powP = pUsed

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