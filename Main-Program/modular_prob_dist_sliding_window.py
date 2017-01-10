################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import Queue
import threading
import thread
import time
import sys, os, msvcrt
import circular_array
import numpy as np
from scipy.stats import truncnorm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib.pyplot import pause

global start_sensor

array_length = 120

# Creates the Circular Arrays for use later on in Code(Gish)
xpar = circular_array.CircularArray(array_length)
ypar = circular_array.CircularArray(array_length)
zpar = circular_array.CircularArray(array_length)

# Creates the Files where Data is stored(Gish)
filename_XY = "Leap_Coordinates_XY.txt"  # Stored data for x,y
filename_XZ = "Leap_Coordinates_XZ.txt"  # Stored data for x,z

count = 0


# Opens the File to write and clear the data out of the text file(Gish)
with open(filename_XY, 'w') as f:
    f.write("\n")

with open(filename_XZ, 'w') as f:
    f.write("\n")

# Creates a leap listener Object
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

        global xpar, ypar, zpar, count, avg_xpar_sum , avg_ypar_sum, start_sensor

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

                mag = (1 / frame.tools[0].direction[2]) * (-1524 - frame.tools[0].tip_position[2])
                # print mag

                # compute the position in the table top plane using the magnitude
                xpos = frame.tools[0].tip_position[0] + mag * frame.tools[0].direction[0]
                ypos = frame.tools[0].tip_position[1] + mag * frame.tools[0].direction[1]

                # build array of values
                # xpar.add_value(xpos)
                # ypar.add_value(ypos)

                start_sensor = False

                if xpos < 225 and xpos > -225:
                    start_sensor = True
                    xpar.add_value(xpos)
                else:
                    print('Please Point @ a block on the grid')
                    time.sleep(1)

                if ypos < 375 and ypos > -75:
                    start_sensor = True
                    ypar.add_value(ypos)
                else:
                    print('Please Point @ a block on the grid')
                    time.sleep(1)




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
                xpar.add_value(xpos)
                zpar.add_value(zpos)

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

class calculations(object):

    def __init__(self):
        pass
    def average_center_x(self):
        xpar_sum = 0
        avg_xpar_sum = xpar.averager_function()

        return avg_xpar_sum
    def average_center_y(self):
        ypar_sum = 0
        avg_ypar_sum = ypar.averager_function()

        return avg_ypar_sum
    def compute_prob(self, xo=0, yo=0, sd=150):
        counter = 0
        yo = -yo
        sd_left = (-150 - xo) / sd
        sd_right = (150 - xo) / sd
        sd_bottom = (0 - yo) / sd
        sd_top = (300 - yo) / sd
        x = np.linspace(-150, 150, 301)
        y = np.linspace(0, 300, 301)
        xx, yy = np.meshgrid(x, y)
        xx_pdf = truncnorm.pdf(xx, sd_left, sd_right, loc=xo, scale=sd)
        yy_pdf = truncnorm.pdf(yy, sd_bottom, sd_top, loc=yo, scale=sd)
        pdf = xx_pdf * yy_pdf
        prob = np.zeros([4, 4])
        # lowest_value = 20
        for i in np.arange(4):
            i0 = 75 * i
            for j in np.arange(4):
                j0 = 75 * j
                prob[i, j] = pdf[i0:i0 + 75, j0:j0 + 75].sum()

        return prob

def main():

    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)
    counter = 0
    while True:

        global start_sensor
        start_sensor = False
        if start_sensor is True:
            prob = calculations().compute_prob(xo=calculations().average_center_x(), yo=calculations().average_center_x() - 200, sd=50)
            print xpar.standard_deviation(array_length)
            print prob
            print
            counter += 1




            if prob.max() > .4 and counter > 100:
                break

    """circle = plt.Circle((0, 0), (xpar.standard_deviation() + ypar.standard_deviation()) / 2, fc='y')
        plt.gca().add_patch(circle)
        plt.show()"""
    """print xpar.standard_deviation()
        if (((xpar.standard_deviation() + ypar.standard_deviation()) / 2) < .01) and (xpar.index > 100):
            print xpar.standard_deviation()
            print
            break"""


    """calculations().average_center()

    print np.round(prob, 6)
    print
    print'sum of prob = %f' % prob.sum()

    """


    controller.remove_listener(listener)


if __name__ == "__main__":
    main()

