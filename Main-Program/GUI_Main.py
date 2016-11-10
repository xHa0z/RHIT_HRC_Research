'''
Purpose: This point of this is to give a gui/ feedback system
        for the user to see what the robot is doing and how
        to set up the board. It also displays which boxes are
        being delete. More will be added when needed.
        
Project: Robotics Arm Research 

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

                          
# Array to hold all of the boxes in
box = []
box_new = [0]*16

# Test file passes information between Cyton and Main program
with open('test.txt', 'w') as f:
    f.write('')

with open('NLP_Speech.txt', 'w') as f:
    f.write('Start')

'''
Begins the game and board. Also adds number to the boxes.
Please note that the boxes are hard coded to be a set pattern
This function doesn't currently gernerate a random sequence of 
boxes and colors. The pattern can be changed at the end function
'''
def start(canvas):
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
    for k in range(16):
        if canvas.itemcget(box[k], "fill") == "white":
            canvas.delete(box[k])
            box_new[k] = 0
            
        elif canvas.itemcget(box[k], "fill") == "red":
            box_new[k] = 1
            
        elif canvas.itemcget(box[k], "fill") == "green":
            box_new[k] = 2
            
        else:
            box_new[k] = 3
            
    box_matrix = np.reshape(box_new, (4,4))
    np.savetxt('game.txt', box_matrix, fmt='%1d')
    # Calls the function to create the grid on the canvas
    grid(canvas)
    


# This function is used to create a grid system on the canvas
def grid(canvas):
    for k in range(4):
        # Row of Lines
        canvas.create_line(0, k * 150, 600, k * 150, width=3)
        canvas.create_line(0, k * 150, 600, k * 150, width=3)
        # Column of lines
        canvas.create_line(k * 150, 0, k * 150, 600, width=3)


# To get back to the original state
def restart(canvas, box):
    for k in range(16):
        canvas.delete(box[k])

    del box[:]
    start(canvas)

# Removes the selected box that is currently being pick from a text box
def box_removal(box, data, canvas):
    number = int(data.box.get())

    canvas.delete(box[number])

def Leap_Motion(text_box, root):
    text_box.configure(background='red')
    text_box.update_idletasks()
    os.system('modular_prob_dist_sliding_window.py')
    text_box.configure(background='green')
    text_box.update_idletasks()
    
def NLP(text_box, root):
    text_box.configure(background='red')
    text_box.update_idletasks()
    os.system('streaming_windows.py')
    text_box.configure(background='green')
    text_box.update_idletasks()
    
def Matrix(text_box, root):
    text_box.configure(background='red')
    text_box.update_idletasks()
    Matrix_Flag = NLP_Main()
    text_box.configure(background='green')
#     text_box.insert(1.0, 'Box Number Selected: ' + str(box_number) + '\n' + \
#                     'Robot Status: ' + '\n' +\
#                     'NLP Speech: ' + str(NLP_Speech))
    text_box.update_idletasks()
    
    return Matrix_Flag
    
def GUI_Main():

    # Tinker is being defined and the frames are being set up
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
    NLP_Start_Button['command'] = lambda: NLP(text_box, root)
    
    Leap_Motion_Button = ttk.Button(secondary_frame,
                                     text='Start Leap Motion')
    Leap_Motion_Button.grid(row=5, column=0, sticky=W,pady=5)
    Leap_Motion_Button['command'] = lambda: Leap_Motion(text_box, root)
    
    Move_Button = ttk.Button(secondary_frame,
                                     text='Move')
    Move_Button.grid(row=6, column=0, sticky=W,pady=5)
    Move_Button['command'] = lambda: Matrix(text_box, root) 

    reset_button = ttk.Button(secondary_frame,
                                     text='Reset Board')
    reset_button.grid(row=7, column=0, sticky=W,pady=5)
    reset_button['command'] = lambda: restart(canvas, box)
    

    with open('test.txt', 'r') as f:
        if f.readline == 'done':
            box_number = f.readline()
            Robot_Status = f.readline()
        elif f.readline == '':
            Robot_Status = ''
            box_number = 'No Box Selected'
        else:
            Robot_Status = 'Standby'
            box_number = f.readline()
            if box_number == '':
                pass
            else:
                canvas.delete(box[int(box_number)])
          
    # This opens what was picked up by the NLP Speech and prints out what was said or "Didn't Catch That"
    # if the NLP didn't pick up the key words  
    with open('NLP_Speech.txt', 'r') as f:
        if MainFunctions.checkMatrix(getMatrixFromFile('out_file')) == False:
            NLP_Speech = "Didn't catch that."
        else:
            NLP_Speech = f.readline()
    text_box.update_idletasks()  
    
    # What is put into the text box
    text_box.insert(1.0, 'Box Number Selected: ' + str(box_number) + '\n' + \
                    'Robot Status: ' "+ str(Robot_Status) "+ '\n' +\
                    'NLP Speech: ' + str(NLP_Speech))
    
    
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
    probabilityMatrix, maxNumberIndex = multiplyMatrices(Leap_Matrix, Leap_Matrix)
    if maxNumberIndex == [0,0]:
        with open('test.txt', 'w') as f:
            f.write(str(0))
    elif maxNumberIndex == [0,1]:
        with open('test.txt', 'w') as f:
            f.write(str(1))
    elif maxNumberIndex == [0,2]:
        with open('test.txt', 'w') as f:
            f.write(str(2))
    elif maxNumberIndex == [0,3]:
        with open('test.txt', 'w') as f:
            f.write(str(3))
    elif maxNumberIndex == [1,0]:
        with open('test.txt', 'w') as f:
            f.write(str(4))
    elif maxNumberIndex == [1,1]:
        with open('test.txt', 'w') as f:
            f.write(str(5))
    elif maxNumberIndex == [1,2]:
        with open('test.txt', 'w') as f:
            f.write(str(6))
    elif maxNumberIndex == [1,3]:
        with open('test.txt', 'w') as f:
            f.write(str(7))
    elif maxNumberIndex == [2,0]:
        with open('test.txt', 'w') as f:
            f.write(str(8))
    elif maxNumberIndex == [2,1]:
        with open('test.txt', 'w') as f:
            f.write(str(9))
    elif maxNumberIndex == [2,2]:
        with open('test.txt', 'w') as f:
            f.write(str(10))
    elif maxNumberIndex == [2,3]:
        with open('test.txt', 'w') as f:
            f.write(str(11))
    elif maxNumberIndex == [3,0]:
        with open('test.txt', 'w') as f:
            f.write(str(12))
    elif maxNumberIndex == [3,1]:
        with open('test.txt', 'w') as f:
            f.write(str(13))
    elif maxNumberIndex == [3,2]:
        with open('test.txt', 'w') as f:
            f.write(str(14))
    elif maxNumberIndex == [3,3]:
        with open('test.txt', 'w') as f:
            f.write(str(15))
            
    with open('test.txt', 'r') as f:
            print(f.read())
            
   # resetTextFile(NLPTextFileName, NLPMatrixInit)


def main():
    
    GUI_Main()
    

if __name__ == '__main__':
    main()


