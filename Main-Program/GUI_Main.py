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
previous_box = -1
Box_Selected = str('Nothing')
Game_ID_Number = 1
Last_Game_Number = -1

# Test file passes information between Cyton and Main program
with open('test.txt', 'w') as f:
    f.write('')

# NLP_Speech file passes what was picked up by the NLP
with open('NLP_Speech.txt', 'w') as f:
    f.write('Nothing')
    
# Test file passes information between Cyton and Main program
with open('out_file.txt', 'w') as f:
    f.write(str(0))
 
# with open('Box_Selected.txt', 'w') as f:
#     f.write('')  

reset_array = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])    
np.savetxt('Leap_Matrix.txt', reset_array, fmt='%1d') 
'''
Begins the game and board. Also adds number to the boxes.
Please note that the boxes are hard coded to be a set pattern
This function doesn't currently gernerate a random sequence of 
boxes and colors. The pattern can be changed at the end function
'''
def grid_create(canvas):  
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
  
  
def consent_window():
    # Create the consent frame each time the game is restarted to give their consent
    # to be recorded
    root_content = Tkinter.Tk()
    consent_frame = ttk.Frame(root_content, padding = (25, 25))
    consent_frame.grid()
    
    # This is the consent box where the consent form is shown 
    consent_box = Text(consent_frame, width=50, height=15, background='white', wrap=WORD)
    consent_scroll = Scrollbar(consent_frame)
    consent_scroll.config(command=YView)
    consent_box.config(yscrollcommand=consent_scroll.set)
    consent_box.grid(row=0, column=1, pady=10)
    consent_scroll.grid(row=0,column=0, sticky=E)
    consent_box.insert(1.0, '            Human-Robot Collaboration \n' 
                            '\n    You are being invited to participate in a research study about human-robot collaboration. ' 
                            'This study is being conducted by Dr. Ryder Winck and Dr. Carlotta Berry,' 
                            'from the Mechanical Engineering and Electrical and Computer Engineering Departments '
                            'at Rose-Hulman Institute of Technology. There are no known risks or costs if you decide' 
                            'to participate in this research study. The information you provide will be used to improve '
                            'algorithms that allow robots to interpret human behavior improving their ability to interact'
                            ' with humans. The information collected may not benefit you directly, but the information learned'
                            ' in this study should improve human-robot interaction. \n'
                            '\n    Your participation in this study will be in the form of a game played with the robot.'
                            ' There will be audio and video recordings of you collected as you participate in this game.'
                            ' The data collected as you play the game will be anonymous. Should the data be published, '
                            'no individual information will be disclosed. Your participation in this study is voluntary.'
                            ' You may withdraw from participation at any time by simply clicking the button to end the game. \n'
                            '\n    If you have any questions about the study, or wish to withdraw from the study after completing a '
                            'game, please contact Ryder Winck by email at winckrc@rose-hulman.edu. If you have any questions about'
                            " your rights as a research subject or if you feel you've been placed at risk, you may contact the "
                            'Institutional Reviewer, Daniel Morris, by phone at (812) 877-8314, or by e-mail at morris@rose-hulman.edu. \n'
                            '\n    By clicking below you consent to participate in this study:')            
    consent_box.configure(state='disabled')
    
    # Create a button that says that they consent
    Consent_Button = ttk.Button(consent_frame,
                                     text='Consent to Terms')
    Consent_Button.grid(row=1, column =1, pady=5)
    
    
    Consent_Button['command'] = lambda: GUI_Main(root_content)
    
    with open('Game_Number_Counter.txt', 'r') as f:
        Last_Game_Number = f.read()
        
    if Last_Game_Number == -1:
        Last_Game_Number == 'file currupted'
        
    Game_Number_Label = ttk.Label(consent_frame, text='Your Game number is ' + str(Last_Game_Number) + '. Please '
                                  'remember your game id. It will be displayed at the end one more time.')
    Game_Number_Label.grid(row=2, column= 1, pady= 5)
    
    root_content.mainloop()
        

# this function comes after the consent window and shows a number for the game for the person to remember.
# (Not yet implemented)
def Game_Check():
    root_Game_Check = Tkinter.Tk()
    Game_Check_Frame= ttk.Frame(root_Game_Check, padding = (25, 25))
    Game_Check_Frame.grid()
    
    Game_Check_Question_Label = ttk.Label(Game_Check_Frame, text='Is this the correct block ' + str(Box_Selected) +
                                          ' ?')
    Game_Check_Question_Label.grid(row=0, column= 0, pady= 5) 

    #Buttons to see if the box selected is correct
    Correct_Button = ttk.Button(root_Game_Check,
                                     text='Correct Block')
    Correct_Button.grid(row=1, column =0, pady=5, padx = 5)
    
    Correct_Button['command'] = lambda: Correct_Block(root_Game_Check)
    
    Wrong_Button = ttk.Button(root_Game_Check,
                                     text='Wrong Block')
    Wrong_Button.grid(row=1, column =1, pady=5)
    
    Wrong_Button['command'] = lambda: Wrong_Block(root_Game_Check)
    
# This function writes to the robot file to move the robot if it is correct block picked
def Correct_Block(Root_Game_Check):
        with open('test.txt', 'w') as f:
            f.write(str(Box_Selected))
            
        Root_Game_Check.destroy()
        
# This function does nothing and just tells the user to start over.
def Wrong_Block(Root_Game_Check):
    Root_Game_Check.destroy()
    
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
    

# After winning the game the restart button calls this function to start the game over
def Restart_Game(root_win, root, win_frame,text_box, canvas, box):
    restart(canvas, box)
    root_updater(root, text_box, canvas)
    root_win.destroy()
    root.destroy()
    
    Last_Game_Number += 1
    with open('Game_Number_Counter.txt', 'w') as f:
        f.write(str(Last_Game_Number))
    consent_window()
    
# This function is to change the text box color to red for when the Leap Motion Starts
def Leap_Motion(text_box, canvas, root):
    text_box.configure(background='red')
    text_box.update_idletasks()
    os.system('modular_prob_dist_sliding_window.py')
    text_box.configure(background='green')
    text_box.update_idletasks()
    
    root_updater(root, text_box, canvas)
    
    Matrix(text_box,canvas, root)
    
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
    Game_Check()
#     return Matrix_Flag

# This is the temporary fix to update the gui after clicking the buttons would like to have it 
# update automatically which requires multithreading
def root_updater(root, text_box, canvas):
    global boxes_removed, read_box_selected, previous_box, Box_Selected
    
    text_box.configure(state='normal')
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
            
#     with open('Box_Selected.txt', 'r') as f:
#         text = f.readline()
#         
#         if text != '':
#             # Deletes the box from the array which removes it from the screen after pressing update
#             # then then it adds one to the amount of boxes removed.
#             box_number = int(text)
#             if box[box_number] != 0:
#                 canvas.delete(box[box_number])
#                 box[box_number] = 0
#                 previous_box = box_number
#                 boxes_removed = boxes_removed + 1
#                 read_box_selected = 1
#             
#                  
#             elif box_number == previous_box:
#                 box_number = 'This was the last box that was selected. Please try again.'
#             
#             else:
#                 pass
#             
#         else:
#             Robot_Status = 'Standby'
#             box_number = f.readline()
            
    if Box_Selected != str('Nothing'):
            # Deletes the box from the array which removes it from the screen after pressing update
            # then then it adds one to the amount of boxes removed.
            box_number = Box_Selected
            if box[box_number] != 0:
                canvas.delete(box[box_number])
                box[box_number] = 0
                previous_box = box_number
                boxes_removed = boxes_removed + 1
                read_box_selected = 1
            
                 
            elif box_number == previous_box:
                box_number = 'This was the last box that was selected. Please try again.'
            
            else:
                pass
            
    else:
        Robot_Status = 'Standby'
        box_number = Box_Selected
                 
#     if read_box_selected == 1:
#         read_box_selected = 0
#         Box_Selected = str('Nothing')
#         with open('Box_Selected.txt', 'w') as f:
#             f.write('')
            
    # This opens what was picked up by the NLP Speech and prints out what was said or "Didn't Catch That"
    # if the NLP didn't pick up the key words  
    with open('NLP_Speech.txt', 'r') as f:
        # NLP send back a matrix filled with all -1 to indicated that it didn't understand
        if MainFunctions.checkMatrix(getMatrixFromFile('out_file')) == False:
            NLP_Speech = "Didn't catch that. Please click the NLP button again and try again."
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
        win_label = Label(win_frame, text='Congratulations on getting three blocks! You win!' 
                        ' Now click the restart button to begin a new game!')
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
    text_box.configure(state='disabled')
    # update the GUI
    text_box.update_idletasks()
    canvas.update_idletasks()
    root.update_idletasks()
    
    
       
def GUI_Main(root_consent):
    # Tinker is being defined and the frames are being set up
    # The Main Frame holds the Canvas and the Secondary holds the 
    # text box and the buttons
    root_consent.destroy()
    root = Tkinter.Tk()
    main_frame = ttk.Frame(root, padding=(25, 25))
    secondary_frame = ttk.Frame(root, padding=(25, 25))
    main_frame.grid(row=0, column=0)
    secondary_frame.grid(row=0, column=1, sticky=N)
#     thrid_frame = ttk.Frame(root)
#     thrid_frame.place(x=150,y=150)
    
    # Text box to give feedback in the GUI
    text_box = Text(secondary_frame, width=65, height=5, background='green')
    text_box.grid(row=0, column=0)
    
    instruction_box = Text(secondary_frame, width=50, height=15, background='white', wrap=WORD)
    scr = Scrollbar(secondary_frame)
    scr.config(command=YView)
    instruction_box.config(yscrollcommand=scr.set)
    instruction_box.grid(row=5, column=0, pady=10)
    scr.grid(row=5,column=0, sticky=E)
    instruction_box.insert(1.0, '1.) Please place the blocks in the cubby holes according to how they are positioned on '
                                    'the GUI.' + '\n' + '\n'
                                '2.) Press the Start NLP button to begin talking to the robot. When you are done pause for a '
                                    'moment and then say "finish". ' 
                                    "Once you are done if it says that it didn't hear you you need to press the button again"
                                    ' and try talking to the robot again until it hears you.' + '\n' + '\n'
                                '3.) Next hit the Leap Motion button and point to the the cubby spot (with the pencil) that you would like'
                                    "selected. Again if it says that it didn't detected which cubby you need to hit the "
                                    'button again and point to the cubby spot.' + '\n' + '\n'
                                '4.) Once the program has heard you and found the box that you want please click the move button'
                                    ' to see the robot move to the block that you picked and move it.' + '\n' + '\n'
                                '5.) After you have successfully removed three blocks you win and can restart the game!')
    
    instruction_box.configure(state='disabled')
    text_box.configure(state='disabled')
    
    # The canvas for the board and grid of boxes
    canvas = Canvas(main_frame, width=600, height=600)
    canvas.grid()
    
    # Starts up the the game board right away.
    grid_create(canvas)
    
    #Labels with numbers to tell user to select which button
#     one_label = ttk.Label(secondary_frame, text='1.')
#     one_label.place(x=250,y=112)
#     
#     two_label = ttk.Label(secondary_frame, text='2.')
#     two_label.place(x=230, y=152)
#     
#     three_label = ttk.Label(secondary_frame, text='3.')
#     three_label.place(x=250, y=192)
    
    instruction_label = ttk.Label(secondary_frame, text='Instructions: ')
    instruction_label.grid(row=4, column =0, sticky = W)
    
    # The buttons for start, delete, and reset. The delete button
    # deletes the box number that you typed in the entry box.
    # Start begins the game with a clean board. Reset resets the
    # board back to the starting state to begin again.
    
    NLP_Start_Button = ttk.Button(secondary_frame,
                                     text='Start NLP')
    NLP_Start_Button.grid(row=1, column =0, pady=5)
    NLP_Start_Button['command'] = lambda: NLP(text_box,canvas, root)
    
    Leap_Motion_Button = ttk.Button(secondary_frame,
                                     text='Start Leap Motion')
    Leap_Motion_Button.grid(row=2, column =0, pady=5)
    Leap_Motion_Button['command'] = lambda: Leap_Motion(text_box,canvas, root)
    
    Move_Button = ttk.Button(secondary_frame,
                                     text='Quit')
    Move_Button.grid(row=6, column =0, pady=5)
#     Move_Button['command'] = lambda: pass
    
    root_updater(root, text_box, canvas)
    root.mainloop()
    
def NLP_Main():
    global previous_box, Box_Selected
    
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
    if probabilityMatrix == [[0]]:
        return

    i = maxNumberIndex[0] 
    k = maxNumberIndex[1] 
    x = i * 4 + k
           
    Box_Selected = x
    print(str(Box_Selected))
#     if box[x] != 0:
#         with open('test.txt', 'w') as f:
#             f.write(str(x))
#         Box_Selected = x
# #         with open('Box_Selected.txt', 'w') as f:
# #             f.write(str(x)) 
#     else:
#         Box_Selected = x
# #         with open('Box_Selected.txt', 'w') as f:
# #             f.write(str(x)) 
#    # resetTextFile(NLPTextFileName, NLPMatrixInit)


def main():
    
    consent_window()
    

if __name__ == '__main__':
    main()


