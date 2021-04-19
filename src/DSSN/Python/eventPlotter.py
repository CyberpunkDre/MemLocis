#############################################################
##                                                         ##
## Re-implementation of Flexible Network Simulator project ##
## from my Distributed Sensor & System Networks class      ##
##                                                         ##
#############################################################

#############################################################
##                                                         ##
## Event Plotter                                           ##
## Inputs:                                                 ##
##      eventLog = contains time, position, and message    ##
##      data from simulation                               ##
##                                                         ##
## Output:                                                 ##
##      function [mSent, pUsed] = eventPlotter(eventLog,   ##
##                                              doPlot)    ##
##                                                         ##
## Targets will randomly message each other every so often ##
##                                                         ##
#############################################################


# function [mSent, pUsed] = eventPlotter(eventLog, doPlot)

# if doPlot == 1
#     figure(1)
#     hold on
#     xlim([1 100]);
#     ylim([1 100]);
#
# n = size(eventLog,2);
# m = size(eventLog(1).nodePosition,2);
# q = size(eventLog(1).targetPosition,2);
#
# nodePlot = zeros(m,1);
# targetPlot = zeros(q,1);
# messagePlot = eventLog(1).message;
# mSent = 0;
# pUsed = 0;

# # Draw starting positions
# if doPlot == 1:
#     title('Time: 0.0 s');
#     for j in range( 1, m + 1):
#         nodePlot(j) = plot(eventLog(1).nodePosition{j}(1),eventLog(1).nodePosition{j}(2),'og');
#
#     for j in range( 1, q + 1):
#         targetPlot(j) = plot(eventLog(1).targetPosition{j}(1),eventLog(1).targetPosition{j}(2),'xr');
#
# # Iterate through every log and plot data
# tSum = 0;
# for i in range( 2, n + 1):
#    
#     # Title/time data first
#     if doPlot == 1
#         title(['Time: ' num2str(eventLog(i).time) ' s']);
#
#     # Plot nodes
#     #     for j = 1:10
#     #        delete(nodePlot(j));
#     #        nodePlot(j) = plot(eventLog(i).nodePosition{j}(1),eventLog(i).nodePosition{j}(2),'og');
#     #        drawnow;
#
#     # Plot targets
#     if doPlot == 1:
#         for j in range( 1, q + 1):
#             delete(targetPlot(j));
#             targetPlot(j) = plot(eventLog(i).targetPosition{j}(1),eventLog(i).targetPosition{j}(2),'xr');
#             drawnow;
#
#     lastMessagePlot = messagePlot;
#     messagePlot = eventLog(i).message;
#     r = size(lastMessagePlot,2);
#     if doPlot == 1
#         for j = 1:r
#             delete(lastMessagePlot{j});
#    
#     r = size(messagePlot,2);
#     mSent = mSent + r;
#     for j = 1:r
#         p1 = [eventLog(i).message{j}(1), eventLog(i).message{j}(2)];
#         p2 = [eventLog(i).message{j}(3), eventLog(i).message{j}(4)];
#         dist = norm(p1 - p2)*100;
#         if dist ~= 0
#             pUsed = pUsed + 1/(dist^2);
#
#         if doPlot == 1
#             dp = p2 - p1;
#             messagePlot{j} = quiver(p1(1),p1(2),dp(1),dp(2),0);
#             drawnow;
#
#
# if doPlot == 1
#     hold off