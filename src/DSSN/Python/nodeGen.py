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
import numpy as np

# function outNodes = nodeGen(field, number, range, method)
#
# outNodes = struct('x', {}, 'y', {})
#

# pos = zeros(number, 2)

# if method == 2:
#       xLim = field(1)
#       yLim = field(2)
#
#   for i in range(1, number+1):
#       outNodes(i).x = rand()*xLim
#       outNodes(i).y = rand()*yLim
#       pos(i,:) = [outNodes(i).x, outNodes(i).y]
#       
#       if i ~= 1:
#           inRange = 0
#           while inRange == 0:
#               for j in range(1, (i - 1) ):
#                   dist = norm( pos(i,:) - pos(j,:) )
#                   if dist <= range:
#                       inRange = 1
#                       j = i
#                   else:
#                       outNodes(i).x = rand()*xLim;
#                       outNodes(i).y = rand()*yLim;
#                       pos(i,:) = [outNodes(i).x, outNodes(i).y]
#       
#       outNodes(i).id = i
#       outNodes(i).range = range
#       outNodes(i).incoming = {}
#       outNodes(i).interests = {}
#
# if method == 1:
#       xLim = floor( field(1) / 10) - 1
#       yLim = floor( field(2) / 10) - 1
#       k = 1
#       for i in range (1, xLim + 1):
#           for j in range (1, yLim + 1):
#               outNodes(k).x = i*(10);
#               outNodes(k).y = j*(10);
#               outNodes(k).id = k;
#               outNodes(k).range = 10;
#               outNodes(k).incoming = {};
#               outNodes(k).interests = {};
#               k = k + 1
#
# if method == 0:
#       outNodes(1).x = 25
#       outNodes(1).y = 25
#       outNodes(1).id = 1
#       outNodes(1).range = 40
#       outNodes(1).incoming = {}
#       outNodes(1).interests = {}
#       outNodes(2).x = 50
#       outNodes(2).y = 50
#       outNodes(2).id = 2
#       outNodes(2).range = 40
#       outNodes(2).incoming = {}
#       outNodes(2).interests = {}
#       outNodes(3).x = 75
#       outNodes(3).y = 75
#       outNodes(3).id = 3
#       outNodes(3).range = 40
#       outNodes(3).incoming = {}
#       outNodes(3).interests = {}
#       outNodes(4).x = 50
#       outNodes(4).y = 35
#       outNodes(4).id = 4
#       outNodes(4).range = 40
#       outNodes(4).incoming = {}
#       outNodes(4).interests = {}
#       outNodes(5).x = 35
#       outNodes(5).y = 50
#       outNodes(5).id = 5
#       outNodes(5).range = 40
#       outNodes(5).incoming = {}
#       outNodes(5).interests = {}