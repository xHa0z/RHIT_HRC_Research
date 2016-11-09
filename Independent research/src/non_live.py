################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import sys, os, msvcrt

import numpy as np
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib.pyplot import pause

xpar = []  # (ryder)
ypar = []
zpar = []

filename_XY = "Leap_Coordinates_XY.txt"  # Stored data for x,y
filename_XZ = "Leap_Coordinates_XZ.txt"  # Stored data for x,z

count = 0

# Defines the plot to show live data
fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)



# Opens the File to write and clear the data out of the text file
with open(filename_XY, 'w') as f:
    f.write("\n")

with open(filename_XZ, 'w') as f:
    f.write("\n")

class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    # Put stuff here for initialize (ryder)
    def on_init(self, controller):
        print "Initialized"
    # Put stuff here for after initialize (ryder)
    def on_connect(self, controller):
        print "Connected"

        # Enable gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    # This is done over and over (ryder)
    def on_frame(self, controller):

        global xpar, ypar, zpar, count, avg_xpar_sum , avg_ypar_sum

        # time.sleep(0.5)  # (ryder)

        # Get the most recent frame and report some basic information
        frame = controller.frame()

########
        # trying to use tools (ryder)
        if not frame.tools.is_empty:  # check if there is a tool

            # print the current location and orientation of the tool
            # print frame.tools[0].tip_position
            # print frame.tools[0].direction

            a = 1

            if a == 1:
                ################# This is for the paper on the wall ###########################
                # compute the distance along the tool direction from the tip position to the table top
                # the -11 is due to the fact that the origin in ~11 mm above the table top
                #####################################################################################
                # 1,2,3,4,5,6,7 feet

                mag = (1 / frame.tools[0].direction[2]) * (-424.6118 - frame.tools[0].tip_position[2])
                # print mag

                # compute the position in the table top plane using the magnitude
                xpos = frame.tools[0].tip_position[0] + mag * frame.tools[0].direction[0]
                ypos = frame.tools[0].tip_position[1] + mag * frame.tools[0].direction[1]

                # build array of values
                xpar = np.append(xpar, xpos)
                ypar = np.append(ypar, ypos)

                # define the size of the window over which to filter
#                 window = 100
#                 if xpar.size >= window:
#
#                     # average values in the window
#                     xpavg = np.mean(xpar)
#                     ypavg = np.mean(ypar)
#
#                     # display the average values
# #                     print xpavg
# #                     print ypavg
#
                with open(filename_XY, 'a') as f:
                    f.write(str(xpos) + ", " + str(ypos) + "\n")
#
#
#
#                     # remove the first entry of the array to move the window
#                     xpar = np.delete(xpar, 0)
#                     ypar = np.delete(ypar, 0)


            else:
                ################# This is for the paper on the table ###########################
                # compute the distance along the tool direction from the tip position to the table top
                # the -11 is due to the fact that the origin in ~11 mm above the table top
                mag = (1 / frame.tools[0].direction[1]) * (-11 - frame.tools[0].tip_position[1])
                # print mag

                # compute the position in the table top plane using the magnitude
                xpos = frame.tools[0].tip_position[0] + mag * frame.tools[0].direction[0]
                zpos = frame.tools[0].tip_position[2] + mag * frame.tools[0].direction[2]

                # build array of values
                xpar = np.append(xpar, xpos)
                zpar = np.append(zpar, zpos)

                # define the size of the window over which to filter
#                 window = 100
#                 if xpar.size >= window:
#
#                     # average values in the window
#                     xpavg = np.mean(xpar)
#                     zpavg = np.mean(zpar)
#
#                     # display the average values
# #                     print xpavg, zpavg
#
#
                with open(filename_XZ, 'a') as f:
                    f.write(str(xpos) + ", " + str(zpos) + "\n")
#
#
#                     # remove the first entry of the array to move the window
#                     xpar = np.delete(xpar, 0)
#                     zpar = np.delete(zpar, 0)




            """xpos = np.array([xpos])
            zpos = np.array([zpos])
            plt.figure
            plt.plot(xpos, zpos, 'k.')
            plt.show()
            # plt.hold(True)"""


        else:
            count = count + 1
            if count == 30:
                print "no tool detected"
                count = 0


    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"


def average_center():
    xpar_sum = 0
    ypar_sum = 0
    time.sleep(7)
    global avg_xpar_sum, avg_ypar_sum
    if len(xpar) != 0:

        for k in range(0, len(xpar)):
            xpar_sum += xpar[k]


        for k in range(0, len(ypar)):
            ypar_sum = ypar_sum + ypar[k]


        avg_xpar_sum = xpar_sum / len(xpar)
        avg_ypar_sum = ypar_sum / len(ypar)
        print(avg_xpar_sum, avg_ypar_sum, 1)
    else:
        print('Could not detect a location')
def compute_prob(xo=0, yo=0, sd=100):
    """yo = -yo
    sd_left = (-400 - xo) / sd
    sd_right = (400 - xo) / sd
    sd_bottom = (0 - yo) / sd
    sd_top = (400 - yo) / sd
    x = np.linspace(-400, 400, 801)
    y = np.linspace(0, 400, 401)
    xx, yy = np.meshgrid(x, y)
    # xx_pdf = truncnorm.pdf(xx, sd_left, sd_right, loc=xo, scale=sd)
    # yy_pdf = truncnorm.pdf(yy, sd_bottom, sd_top, loc=yo, scale=sd)
    pdf = xx_pdf * yy_pdf
    prob = np.zeros([4, 4])
    for i in np.arange(4):
        i0 = 50 * i
        for j in np.arange(4):
            j0 = 50 * j
            prob[i, j] = pdf[i0:i0 + 50, j0:j0 + 50].sum()
            return prob
    print(prob)"""


def animate(i):  # Function that controls plotting of the xy data from leap motion
    graph_data = open('Leap_Coordinates_XY.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    sum_xs = 0
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            xs.append(x)
            ys.append(y)



    ax1.clear()
    # if np.ceil(avg_xpar_sum/200)=1:
    circle = plt.Circle((avg_xpar_sum, avg_ypar_sum), 40, fc='y')
    plt.gca().add_patch(circle)
    """for k in range(1, 10):
        if time.clock() > 5 * k - .0075 and time.clock() < 5 * k - .0075:
            plt.gca().add_patch(circle)"""

    ax1.plot(xs, ys)
    ax1.set_ylim([0, 400])
    ax1.set_xlim([-400, 400])
    ax1.set_autoscale_on(False)

    for k in range(-200, 400, 200):
        line = plt.Line2D((k, k), (0, 400), lw=2.5)
        plt.gca().add_line(line)

    for k in range(0, 400, 100):
        line = plt.Line2D((-400, 400), (k, k), lw=2.5)
        plt.gca().add_line(line)





"""def init():
    line.set_ydata(np.ma.array(x, mask=True))
    return line,"""

def main():


    # compute_prob(xo=0, yo=0, sd=100)
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()


    # Have the sample listener receive events from the controller
    controller.add_listener(listener)


    # Starts plot on run

    average_center()
    # compute_prob(xo=avg_xpar_sum, yo=avg_ypar_sum, sd=100)
    ani = animation.FuncAnimation(fig, animate, interval=1)
    controller.remove_listener(listener)
    plt.show()



    # Keep this process running until Enter is pressed
    # print "Press Enter to quit..."
    # try:
    #    sys.stdin.readline()

    # except KeyboardInterrupt:
    #    controller.remove_listener(listener)
    # finally:
        # Remove the sample listener when done
    #    controller.remove_listener(listener)
    #    print('made it')
    #    ax1.gcf().clear()


if __name__ == "__main__":
    main()

