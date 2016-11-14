'''
Purpose: This point of this is to give a gui/ feedback system
        for the user to see what the robot is doing and how
        to set up the board. It also displays which boxes are
        being delete. More will be added when needed.
        
Project: Robotics Arm Research 

Files:
    game.txt - This is the file to send the game board  state to the NLP
    Leap_Matrix.txt - The output matrix probablity from the Leap Motion
    Leap_Motion.txt - Unknown
    requirements.txt - This is for the Google NLP Server and authentication.
    test.txt - This file is to send the box number to the robot and for the robot to
                send back done to the main program.
    NLP_Speech.txt - This file is what gets picked up by the NLP. 
    out_file.txt - this is the output matrix from the NLP.
    
Color Code:
    1 = Red Block
    2 = Green Block
    3 = Blue Block
    
Author: Devon Adair
Date Created: 10/31/2016

Last Modified Date: 11/4/2016
'''

from __future__ import division
from __future__ import print_function

import Tkinter
from Tkinter import *
import ttk
import numpy as np
import Leap

import contextlib
import re
import signal
import threading
import json
import os
import datetime
import sys
import signal
import datetime
from threading import Thread


from google.cloud import credentials
from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from google.rpc import code_pb2
from grpc.beta import implementations
from grpc.framework.interfaces.face import face
import pyaudio
from six.moves import queue


from MainFunctions import getMatrixFromFile, \
                          multiplyMatrices, \
                          checkMatrix, \
                          resetTextFile
import MainFunctions

import modular_prob_dist_sliding_window as lpp
from LeapPython import Controller_is_connected_get

# Array to hold all of the boxes in
box = []
box_new = [0]*16

# Counts how many boxes are remove then after 3 it ends and restarts the game,
boxes_removed = 0
read_box_selected = 0

# Test file passes information between Cyton and Main program
with open('test.txt', 'w') as f:
    f.write('')

# NLP_Speech file passes what was picked up by the NLP
with open('NLP_Speech.txt', 'w') as f:
    f.write('Nothing')
    
# Test file passes information between Cyton and Main program
with open('out_file.txt', 'w') as f:
    f.write(str(0))
 
with open('Box_Selected.txt', 'w') as f:
    f.write('')   
'''
Begins the game and board. Also adds number to the boxes.
Please note that the boxes are hard coded to be a set pattern
This function doesn't currently gernerate a random sequence of 
boxes and colors. The pattern can be changed at the end function
'''
def start(canvas):
    # They fill up the board by default and the color is white.
    for k in range(4):
        for j in range(4):
            num = canvas.create_rectangle(25 + 150 * j, 25 + 150 * k, 125 + j * 150,
                                           125 + k * 150, fill="white")
            canvas.create_text((75 + 150 * j, 75 + 150 * k), text=(j + k * 4),
                                font=('Times New Roman', 20))
            box.append(num)
            
    # Manually chosen boxes and colors
    canvas.itemconfig(box[0], fill="red")
    canvas.itemconfig(box[6], fill="blue")
    canvas.itemconfig(box[12], fill="blue")
    canvas.itemconfig(box[15], fill="blue")
    canvas.itemconfig(box[2], fill="green")
    canvas.itemconfig(box[9], fill="green")
    
    # Deletes the boxes that were originally there and not the chosen ones
    # Color Code:
    #     0 = White Block (Default)
    #     1 = Red Block
    #     2 = Green Block
    #     3 = Blue Block
    for k in range(16):
        if canvas.itemcget(box[k], "fill") == "white":
            canvas.delete(box[k])
            box[k] = 0
            box_new[k] = 0
            
        elif canvas.itemcget(box[k], "fill") == "red":
            box_new[k] = 1
            
        elif canvas.itemcget(box[k], "fill") == "green":
            box_new[k] = 2
            
        else:
            box_new[k] = 3
    
    
    # This reshapes the two d array of boxes to matrix and saves it to the 
    # game text file.
    box_matrix = np.reshape(box_new, (4,4))
    np.savetxt('game.txt', box_matrix, fmt='%1d')
    
    # Calls the function to create the grid on the canvas
    grid(canvas)
    


# This function is used to create a grid system on the canvas
def grid(canvas):
    for k in range(4):
        # Row of Lines
        canvas.create_line(0, k * 150, 600, k * 150, width=3)
        
        # Column of lines
        canvas.create_line(k * 150, 0, k * 150, 600, width=3)


# To get back to the original state
def restart(canvas, box):
    for k in range(16):
        canvas.delete(box[k])

    del box[:]
    start(canvas)

# After winning the game the restart button calls this function to start the game over
def Restart_Game(root_win, root, win_frame,text_box, canvas, box):
    restart(canvas, box)
    root_updater(root, text_box, canvas)
    root_win.destroy()
    
# This function is to change the text box color to red for when the Leap Motion Starts
def Leap_Motion(text_box, canvas, root):
    text_box.configure(background='red')
    text_box.update_idletasks()
    os.system('modular_prob_dist_sliding_window.py')
    text_box.configure(background='green')
    text_box.update_idletasks()
    
    root_updater(root, text_box, canvas)
    
# This function is to change the text box color to red when the NLP is running then green when it is done
# Please note there is about a second and a half lag when starting the NLP
def NLP(text_box,canvas, root):
    text_box.configure(background='red')
    text_box.update_idletasks()
    os.system('streaming_windows.py')
    text_box.configure(background='green')
    text_box.update_idletasks()
    
    root_updater(root, text_box, canvas)
    
# This is to change the color of the text box to red when the matrixs are being 
# multiplied then back to green when done 
def Matrix(text_box, canvas, root):
    text_box.configure(background='red')
    text_box.update_idletasks()
    Matrix_Flag = NLP_Main()
    text_box.configure(background='green')
    text_box.update_idletasks()
    
    root_updater(root, text_box, canvas)
    return Matrix_Flag

# This is the temporary fix to update the gui after clicking the buttons would like to have it 
# update automatically which requires multithreading
def root_updater(root, text_box, canvas):
    global boxes_removed, read_box_selected
    text_box.delete('1.0', END)
    if os.path.isfile('NLP_Speech.txt') != True:
         with open('NLP_Speech.txt', 'w') as f:
             f.write('Nothing')
             
             
    # This opens up the text file to determine the box number to put
    # in the text file and also the robot status
    with open('test.txt', 'r') as f:
        if f.readline == 'DONE':
            box_number = f.readline()
            Robot_Status = f.readline()
        else:
            Robot_Status = ''
            box_number = 'No Box Selected'
            
    with open('Box_Selected.txt', 'r') as f:
        text = f.readline()
        
        if text != '':
            # Deletes the box from the array which removes it from the screen after pressing update
            # then then it adds one to the amount of boxes removed.
            box_number = int(text)
            if box[box_number] != 0:
                canvas.delete(box[box_number])
                boxes_removed = boxes_removed + 1
                read_box_selected = 1
        else:
            Robot_Status = 'Standby'
            box_number = f.readline()
                 
    if read_box_selected == 1:
        read_box_selected = 0
        with open('Box_Selected.txt', 'w') as f:
            f.write('')
            
    # This opens what was picked up by the NLP Speech and prints out what was said or "Didn't Catch That"
    # if the NLP didn't pick up the key words  
    with open('NLP_Speech.txt', 'r') as f:
        # NLP send back a matrix filled with all -1 to indicated that it didn't understand
        if MainFunctions.checkMatrix(getMatrixFromFile('out_file')) == False:
            NLP_Speech = "Didn't catch that."
        else:
            NLP_Speech = f.readline() 
    
    # This checks to see if the Leap is connected or not then writes it to the text
    # box inside the GUI
    controller = Leap.Controller()
    controller_active = controller.is_connected
    
    if controller_active == False:
        controller_active = 'Disconnected'
        
    else:
        controller_active = 'Connected'
    
    # Game logic to count how many blocks are picked up and then when it reaches 3
    # a new window pops up telling the user that they won and need to press the restart
    # button on the new window.
    if boxes_removed == 3:
        boxes_removed = 0
        root_win = Tkinter.Toplevel()
        win_frame = ttk.Frame(root_win, padding = (25, 25))
        win_frame.grid()
        # Label for the win frame
        win_label = Label(win_frame, text='Congradulations on getting three blocks! You win!' 
                        ' Now click the restart button to be a new game!')
        win_label.grid(row = 0, column = 0)
        restart_button = ttk.Button(win_frame,
                                    text='Restart Game')
        restart_button.grid(row=7, column=0, sticky=W,pady=5)
        restart_button['command'] = lambda: Restart_Game(root_win, root, win_frame,text_box, canvas, box)
        
    # What is put into the text box
    text_box.insert(1.0, 'Box Number Selected: ' + str(box_number) + '\n' + \
                    'Robot Status: ' + str(Robot_Status) + '\n' +\
                    'NLP Speech: ' + str(NLP_Speech) + '\n' + 'Leap Motion: ' \
                    + str(controller_active))
    
    # update the GUI
    text_box.update_idletasks()
    canvas.update_idletasks()
    root.update_idletasks()
    
    
       
def GUI_Main():
    # Tinker is being defined and the frames are being set up
    # The Main Frame holds the Canvas and the Secondary holds the 
    # text box and the buttons
    root = Tkinter.Tk()
    main_frame = ttk.Frame(root, padding=(25, 25))
    secondary_frame = ttk.Frame(root, padding=(25, 25))
    main_frame.grid(row=0, column=0)
    secondary_frame.grid(row=0, column=1, sticky=N)

    # Text box to give feedback in the GUI
    text_box = Text(secondary_frame, width=50, height=5, background='green')
    text_box.grid(row=0, column=0)
    

    # The canvas for the board and grid of boxes
    canvas = Canvas(main_frame, width=600, height=600)
    canvas.grid()
    
    # Starts up the the game board right away.
    start(canvas)
    
    
    # The buttons for start, delete, and reset. The delete button
    # deletes the box number that you typed in the entry box.
    # Start begins the game with a clean board. Reset resets the
    # board back to the starting state to begin again.
    
    NLP_Start_Button = ttk.Button(secondary_frame,
                                     text='Start NLP')
    NLP_Start_Button.grid(row=4, column=0, sticky=W,pady=5)
    NLP_Start_Button['command'] = lambda: NLP(text_box,canvas, root)
    
    Leap_Motion_Button = ttk.Button(secondary_frame,
                                     text='Start Leap Motion')
    Leap_Motion_Button.grid(row=5, column=0, sticky=W,pady=5)
    Leap_Motion_Button['command'] = lambda: Leap_Motion(text_box,canvas, root)
    
    Move_Button = ttk.Button(secondary_frame,
                                     text='Move')
    Move_Button.grid(row=6, column=0, sticky=W,pady=5)
    Move_Button['command'] = lambda: Matrix(text_box,canvas, root) 

    reset_button = ttk.Button(secondary_frame,
                                     text='Reset Board')
    reset_button.grid(row=7, column=0, sticky=W,pady=5)
    reset_button['command'] = lambda: root_updater(root, text_box, canvas)
    
    refresh_button = ttk.Button(secondary_frame,
                                     text='Refresh Button')
    refresh_button.grid(row=4, column=1, sticky=W,pady=5)
    refresh_button['command'] = lambda: root_updater(root, text_box, canvas)
    
    
    root_updater(root, text_box, canvas)
#     root.after(2000, root_updater(root, text_box, canvas))
#     root.after(500, canvas)
    root.mainloop()
    
def NLP_Main():
    # stopStatement = false
    NLPTextFileName = "out_file"
    NLPMatrixInit = "0,0,0,0\n0,0,0,0\n0,0,0,0\n0,0,0,0"
    
    # while stopStatement == false:
    NLPMatrix = getMatrixFromFile(NLPTextFileName)
    Leap_Matrix = getMatrixFromFile('Leap_Matrix')
    
    bool = checkMatrix(NLPMatrix)
    if bool == False:
        return str("Didn't catch that.")
    probabilityMatrix, maxNumberIndex = multiplyMatrices(Leap_Matrix, NLPMatrix)
    if maxNumberIndex == [0,0]:
        x = 0
    elif maxNumberIndex == [0,1]:
        x = 1
    elif maxNumberIndex == [0,2]:
        x = 2
    elif maxNumberIndex == [0,3]:
        x = 3
    elif maxNumberIndex == [1,0]:
        x = 4
    elif maxNumberIndex == [1,1]:
        x = 5
    elif maxNumberIndex == [1,2]:
        x = 6
    elif maxNumberIndex == [1,3]:
        x = 7
    elif maxNumberIndex == [2,0]:
        x = 8
    elif maxNumberIndex == [2,1]:
        x = 9
    elif maxNumberIndex == [2,2]:
        x = 10
    elif maxNumberIndex == [2,3]:
        x = 11
    elif maxNumberIndex == [3,0]:
        x = 12
    elif maxNumberIndex == [3,1]:
        x = 13
    elif maxNumberIndex == [3,2]:
        x = 14
    elif maxNumberIndex == [3,3]:
        x = 15
            
#     with open('test.txt', 'r') as f:
#         print(f.read())
    if box[x] != 0:
        with open('test.txt', 'w') as f:
            f.write(str(x))
        with open('Box_Selected.txt', 'w') as f:
            f.write(str(x)) 
    else:
        with open('Box_Selected.txt', 'w') as f:
            f.write(str(x)) 
   # resetTextFile(NLPTextFileName, NLPMatrixInit)


def main():
    
    GUI_Main()
    

if __name__ == '__main__':
    main()


