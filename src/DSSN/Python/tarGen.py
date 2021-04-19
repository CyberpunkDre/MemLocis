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

# for i in range(1,number+1):
#       outTar(i).x = randi( field(1) )
#       outTar(i).y = randi( field(2) )
#       outTar(i).id       = i
#       outTar(i).max      = number
#       outTar(i).interval = i
#       deg = randi(360)
#       xSpeed = (speed * timeDiv) * sin(deg)
#       ySpeed = (speed * timeDiv) * cos(deg)
#       outTar(i).vel = [0, speed * timeDiv]
#       outTar(i).tx = {}
#       outTar(i).rx = {}

# outTar(1).x = 20
# outTar(1).y = 20
# outTar(2).x = 90
# outTar(2).y = 90
# outTar(2).vel(2) = -outTar(2).vel(2)
# outTar(2).interval = 5
