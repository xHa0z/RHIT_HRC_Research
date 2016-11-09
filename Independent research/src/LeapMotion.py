################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import sys, os

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib
import matplotlib.pyplot as plt
import pylab
from matplotlib.pyplot import pause
import time

xpar = []  # (ryder)
ypar = []
zpar = []

filename = "Leap_Coordinates.txt"  # Stored data for x,y,z

count = 0

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)


with open(filename, 'w') as f:
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

        global xpar, ypar, zpar, count

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
                mag = (1 / frame.tools[0].direction[2]) * (-424.6118 - frame.tools[0].tip_position[2])
                # print mag

                # compute the position in the table top plane using the magnitude
                xpos = frame.tools[0].tip_position[0] + mag * frame.tools[0].direction[0]
                ypos = frame.tools[0].tip_position[1] + mag * frame.tools[0].direction[1]

                # build array of values
                xpar = np.append(xpar, xpos)
                ypar = np.append(ypar, ypos)

                # define the size of the window over which to filter
                window = 500
                if xpar.size >= window:

                    # count += count

                    # average values in the window
                    xpavg = np.mean(xpar)
                    ypavg = np.mean(ypar)

                    # display the average values
                    print xpavg
                    print ypavg

                    # if count == 10:
                    with open(filename, 'a') as f:
                        f.write(str(xpavg) + ", " + str(ypavg) + "\n")


                    # remove the first entry of the array to move the window
                    xpar = np.delete(xpar, 0)
                    ypar = np.delete(ypar, 0)


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
                window = 500
                if xpar.size >= window:

                    # count += count

                    # average values in the window
                    xpavg = np.mean(xpar)
                    zpavg = np.mean(zpar)

                    # display the average values
                    print xpavg, zpavg

                    # if counter == 10:
                    with open(filename, 'a') as f:
                        f.write(str(xpavg) + ", " + str(zpavg) + "\n")
                            # count = 0

                    # remove the first entry of the array to move the window
                    xpar = np.delete(xpar, 0)
                    zpar = np.delete(zpar, 0)




            """xpos = np.array([xpos])
            zpos = np.array([zpos])
            plt.figure
            plt.plot(xpos, zpos, 'k.')
            plt.show()
            # plt.hold(True)"""


        else:
            print "no tool detected"
        """
########
        # Get the x-z position of where you are pointing on the table surface (ryder)
        for finger in frame.hands[0].fingers:
            # time.sleep(0.5)
            if finger.type == 1:
                # print the current location and orientation of the index finger
                print finger.tip_position
                print finger.direction

                # compute the distance along the index finger direction from the tip position to the table top
                # the -11 is due to the fact that the origin in ~11 mm above the table top
                mag = (1 / finger.direction[1]) * (-11 - finger.tip_position[1])
                print mag

                # compute the position in the table top plane using the magnitude
                xpos = finger.tip_position[0] + mag * finger.direction[0]
                zpos = finger.tip_position[2] + mag * finger.direction[2]
                print xpos
                print zpos
        """
########

        """ print "Frame id: %d, timestamp: %d, hands: %d, fingers: %d, tools: %d, gestures: %d" % (
              frame.id, frame.timestamp, len(frame.hands), len(frame.fingers), len(frame.tools), len(frame.gestures()))

        # Get hands
        for hand in frame.hands:

            handType = "Left hand" if hand.is_left else "Right hand"

            print "  %s, id %d, position: %s" % (
                handType, hand.id, hand.palm_position)

            # Get the hand's normal vector and direction
            normal = hand.palm_normal
            direction = hand.direction

            # Calculate the hand's pitch, roll, and yaw angles
            print "  pitch: %f degrees, roll: %f degrees, yaw: %f degrees" % (
                direction.pitch * Leap.RAD_TO_DEG,
                normal.roll * Leap.RAD_TO_DEG,
                direction.yaw * Leap.RAD_TO_DEG)

            # Get arm bone
            arm = hand.arm
            print "  Arm direction: %s, wrist position: %s, elbow position: %s" % (
                arm.direction,
                arm.wrist_position,
                arm.elbow_position)

            # Get fingers
            for finger in hand.fingers:

                print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
                    self.finger_names[finger.type],
                    finger.id,
                    finger.length,
                    finger.width)

                # Get bones
                for b in range(0, 4):
                    bone = finger.bone(b)
                    print "      Bone: %s, start: %s, end: %s, direction: %s" % (
                        self.bone_names[bone.type],
                        bone.prev_joint,
                        bone.next_joint,
                        bone.direction)

        # Get tools
        for tool in frame.tools:

            print "  Tool id: %d, position: %s, direction: %s" % (
                tool.id, tool.tip_position, tool.direction)

        # Get gestures
        for gesture in frame.gestures():
            if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                circle = CircleGesture(gesture)

                # Determine clock direction using the angle between the pointable and the circle normal
                if circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/2:
                    clockwiseness = "clockwise"
                else:
                    clockwiseness = "counterclockwise"

                # Calculate the angle swept since the last frame
                swept_angle = 0
                if circle.state != Leap.Gesture.STATE_START:
                    previous_update = CircleGesture(controller.frame(1).gesture(circle.id))
                    swept_angle =  (circle.progress - previous_update.progress) * 2 * Leap.PI

                print "  Circle id: %d, %s, progress: %f, radius: %f, angle: %f degrees, %s" % (
                        gesture.id, self.state_names[gesture.state],
                        circle.progress, circle.radius, swept_angle * Leap.RAD_TO_DEG, clockwiseness)

            if gesture.type == Leap.Gesture.TYPE_SWIPE:
                swipe = SwipeGesture(gesture)
                print "  Swipe id: %d, state: %s, position: %s, direction: %s, speed: %f" % (
                        gesture.id, self.state_names[gesture.state],
                        swipe.position, swipe.direction, swipe.speed)

            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                keytap = KeyTapGesture(gesture)
                print "  Key Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        keytap.position, keytap.direction )

            if gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                screentap = ScreenTapGesture(gesture)
                print "  Screen Tap id: %d, %s, position: %s, direction: %s" % (
                        gesture.id, self.state_names[gesture.state],
                        screentap.position, screentap.direction )

        if not (frame.hands.is_empty and frame.gestures().is_empty):
            print ""
"""
    def state_string(self, state):
        if state == Leap.Gesture.STATE_START:
            return "STATE_START"

        if state == Leap.Gesture.STATE_UPDATE:
            return "STATE_UPDATE"

        if state == Leap.Gesture.STATE_STOP:
            return "STATE_STOP"

        if state == Leap.Gesture.STATE_INVALID:
            return "STATE_INVALID"



def main():


    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    def animate():
        pullData = open('Leap_Coordinates.txt', "r").read()
        dataArray = pullData.split('\n')
        xar = []
        yar = []
        for eachLine in dataArray:
            if len(eachLine) > 1:
                x, y = eachLine.split(',')
                xar.append(int(x))
                yar.append(int(y))
                ax1.clear()
                ax1.plot(xar, yar)
    plt.show()
    ani = animation.FuncAnimation(fig, animate, interval=100)





    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        # controller.remove_listener(listener)
        ani = animation.FuncAnimation(fig, animate, interval=100)

        plt.show()



if __name__ == "__main__":
    main()
