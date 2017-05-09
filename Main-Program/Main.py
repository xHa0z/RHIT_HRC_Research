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
import time
from threading import Thread, Event, Timer
import random
from random import *

import subprocess
from subprocess import Popen, CREATE_NEW_CONSOLE

from google.cloud import credentials
from google.cloud.speech.v1beta1 import cloud_speech_pb2 as cloud_speech
from google.rpc import code_pb2
from grpc.beta import implementations
from grpc.framework.interfaces.face import face
import pyaudio
from six.moves import queue

from mongodb_functions import *

from MainFunctions import getMatrixFromFile, \
                          multiplyMatrices, \
                          checkMatrix, \
                          resetTextFile
import MainFunctions

from Custom_Timer import TimerReset

import modular_prob_dist_sliding_window as lpp

# from modular_prob_dist_sliding_window import Leap_Matrix
from LeapPython import Controller_is_connected_get
from numpy import size



# Load all the constants and global variables 
###########################################################################################
###########################################################################################
# Array to hold all of the boxes in
box = []
box_new = [0]*16

# Counts how many boxes are remove then after 3 it ends and restarts the game,
boxes_removed = 0
read_box_selected = 0
previous_box = -1
Box_Selected = str('Nothing')
Timer_Check = 0

# Directory to store 
video_dir = 'C:/database/video/'
video_dir_db = '/database/video/'
video_dst = ''
# create the dirctory if not exists
if not os.path.exists('C:/database/video/'): 
    os.makedirs('C:/database/video/')
    
ffmpeg_cmd = ('ffmpeg -f dshow -i video="Logitech HD Webcam C615":audio="Microphone (2- CD04)" ')



with open('Game_Number_Counter.txt', 'r') as f:
        Last_Game_Number = f.read()
        video_dst = video_dir + Last_Game_Number + '.avi'
        if os.path.exists(video_dst):
            os.remove(video_dst)
            print ('old video will be replaced')
        insert_game(Last_Game_Number)
        insert_video_dir(Last_Game_Number, video_dst)

Last_Game_Number = int(Last_Game_Number)
# Test file passes information between Cyton and Main program
with open('test.txt', 'w') as f:
    f.write('')

# NLP_Speech file passes what was picked up by the NLP
with open('NLP_Speech.txt', 'w') as f:
    f.write('Tell the robot what block you want to pick up. You need to say a color and when' 
                    'you are done talking you NEED TO SAY FINISH!')

NLP_Speech = 'When talking to the robot please say a block color. End your sentence with "finish".'
    
# Test file passes information between Cyton and Main program
# with open('out_file.txt', 'w') as f:
#     f.write(str(0))

Background_Color = 'Red'

reset_array = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])    
np.savetxt('Leap_Matrix.txt', reset_array, fmt='%1d') 
np.savetxt('out_file.txt', reset_array, fmt='%1d') 

##########################################################################################
##########################################################################################
def GUI_Main(root_consent):
    # Tinker is being defined and the frames are being set up
    # The Main Frame holds the Canvas and the Secondary holds the 
    # text box and the buttons 
    
    with open('test.txt', 'w') as f:
        f.write('0')
    
    # start video recording
    video_rec_cmd = ffmpeg_cmd + video_dst
    print (video_dst)
    pipe = subprocess.Popen(video_rec_cmd, shell=True,  creationflags=CREATE_NEW_CONSOLE)
    print ("start recording")
    
    # Get rid of the consent window when the game starts
    root_consent.destroy()
    
    # Creates the
    root = Tkinter.Tk()
   
    #  make it root the entire screen
    w, h = root.winfo_screenwidth(), root.winfo_screenheight()
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (w, h))
    
      
    root.focus_set() # <-- move focus to this widget
    root.focus_force()
    root.bind("<Escape>", lambda e: e.widget.quit())
    
    main_frame = ttk.Frame(root, padding=(25, 25))
    secondary_frame = ttk.Frame(root, padding=(25, 25))
    main_frame.grid(row=0, column=0)
    secondary_frame.grid(row=0, column=1, sticky=N)
#     thrid_frame = ttk.Frame(root)
#     thrid_frame.place(x=150,y=150)
    
    # Text box to give feedback in the GUI
    text_box = Text(secondary_frame, width=65, height=10, background='red',wrap=WORD,font = ("Helvetica", 12))
    text_box.grid(row=0, column=0)
    
    instruction_box = Text(secondary_frame, width=50, height=25, background='white', wrap=WORD,font=("Helvetica", 13))
    instruction_box.grid(row=5, column=0, pady=10)
    instruction_scroll = Scrollbar(secondary_frame)
    instruction_scroll.config(command=instruction_box.yview)
    instruction_box['yscrollcommand'] = instruction_scroll.set
    instruction_scroll.grid(row=5,column=0, sticky=E)
    instruction_box.insert(1.0, '1.) Before beginning please place the blocks in the cubby holes according to how they are positioned on '
                                    'the GUI. The goal is to remove three of these blocks by using the robot to win the game.' + '\n' + '\n'
                                '2.) Place the headset on to communicate with the robot.' + '\n' + '\n'
                                '3.) Press the Run button then the screen will turn yellow then you start talking and pointing '
                                    'with the pencil over the leap motion. It might take awhile for the leap to finish'
                                    ' so please be patient! It is not broke!' + '\n' + '\n'
                                '4.) There are timeout functions so if you think that it is hung up just give it a bit and everything will'
                                    ' be chill!' + '\n' + '\n'
                                '**** IF YOU THINK THAT THIS SOFTWARE IS BROKE OR NEED TO REPORT AN ISSUE PLEASE GO TO DR. WINCK IN'
                                ' MOENCH D111 OR BY PHONE AT: 877-8098 ****')
    
    instruction_box.configure(state='disabled')
    text_box.configure(state='disabled')
    
    # The canvas for the board and grid of boxes
    canvas = Canvas(main_frame, width=600, height=600)
    canvas.grid(row=1, column=0)
    
    # Label to tell user to place blocks in cubby
    cubby_instructions = ttk.Label(main_frame, text='Set the cubby by the robot to match the grid on screen.',
                                   font=("Helvetica", 18))
    cubby_instructions.grid(row=2, column =0, sticky = S, pady = 7)
    
    cubby_label = ttk.Label(main_frame, text='Cubby Layout Shown Below',
                                   font=("Helvetica", 18))
    cubby_label.grid(row=0, column =0, sticky = S, pady = 7)
    
    # Starts up the the game board right away.
    grid_create(canvas)
    
    
    instruction_label = ttk.Label(secondary_frame, text='Instructions: ')
    instruction_label.grid(row=4, column =0, sticky = W)
    

    # This is the timer test it is functional but needs slight modifications  
    def Force_Quit():
        global Last_Game_Number
        
        try: 
#             if (Running.nlp_process.poll() == None):
            
            command = 'taskkill /F /pid ' + str(Running.nlp_process.pid)
            os.system(command)
        except: 
            print('have not ran module yet.')
#             if (Running.leap_process.poll() == None):
        try:
            command = 'taskkill /F /pid ' + str(Running.leap_process.pid)
            os.system(command)
        except: 
            print('have not ran module yet.')
               
        with open('NLP_Speech.txt', 'w') as f:
            NLP_Speech = "Nothing said yet."
            f.write(NLP_Speech)  
            
        Last_Game_Number += 1
        with open('Game_Number_Counter.txt', 'w') as f:
            f.write(str(Last_Game_Number))
             
        for k in range(16):
            canvas.delete(box[k])
     
        del box[:]
         
        boxes_removed = 0
         
        root_updater(root, text_box, canvas)
        
        root.destroy()
 
#         os.system('taskkill /im ffmpeg.exe /t /f')
        NLP_Speech = 'When talking to the robot please say a block color. End your sentence with "finish".'
        time.sleep(2)
        consent_window()
         
    def time_check():
        root.focus_set()
        time_check.close_loop = root.after(10000, Force_Quit)
        time_check.timer_root = Tkinter.Toplevel()
        timer_frame = ttk.Frame(time_check.timer_root, padding=(25, 25))
        timer_frame.grid()
        timer_label = ttk.Label(timer_frame, text='You have 10 seconds to click continue to stop the game from restarting.')
        timer_label.grid()
        Continue_Button = ttk.Button(timer_frame,
                                     text='Continue')
        Continue_Button.grid(row=2, column =0, pady=5, sticky=E)
        Continue_Button['command'] = lambda: cancel()
        
        def time_check_focus():
            time_check.timer_root.focus_force()
            time_check.timer_root.after(500, time_check_focus)
    
        time_check.timer_root.after(500, time_check_focus)
        
#         time_check.timer_root.focus_set()
#         time_check.timer_root.focus_force()
#         time_check.timer_root.focus_lastfor()
            
    
    def cancel():
        root.after_cancel(time_check.close_loop)
        time_check.timer_root.destroy()
        loop = root.after(120000, time_check)
            
    loop = root.after(180000, time_check) # ~3 minutes
    
    # The buttons for start, delete, and reset. The delete button
    # deletes the box number that you typed in the entry box.
    # Start begins the game with a clean board. Reset resets the
    # board back to the starting state to begin again.
    
    
#     NLP_Start_Button = ttk.Button(secondary_frame,
#                                      text='Start NLP')
#     NLP_Start_Button.grid(row=1, column =0, pady=5)
#     NLP_Start_Button['command'] = lambda: NLP(text_box,canvas, root)
#     
#     Leap_Motion_Button = ttk.Button(secondary_frame,
#                                      text='Start Leap Motion')
#     Leap_Motion_Button.grid(row=2, column =0, pady=5)
#     Leap_Motion_Button['command'] = lambda: Leap_Motion(text_box, canvas, root)
    buttonStyle = ttk.Style()
    buttonStyle.configure('Run.TButton',height = 10, width = 10,font = ("Helvetica", 16))
    
    Quit_Button = ttk.Button(secondary_frame,
                            text='Quit', style = 'Run.TButton')
    Quit_Button.grid(row=6, column =0, pady=5)
    Quit_Button['command'] = lambda: Quit_Button_Function(root, text_box, canvas)
    
    Run_Button = ttk.Button(secondary_frame,
                             text='RUN', style = 'Run.TButton')
    Run_Button.grid(row=1, column =0, pady=5)
    Run_Button['command'] = lambda: Running(text_box, canvas, root, Run_Button)
    
    root_updater(root, text_box, canvas)
    
    def instruction_pop_up():
        
        root_game_instructions = Tkinter.Toplevel()
        root_game_instructions.iconposition(20, 1000)
        
        instructions = ttk.Label(root_game_instructions, text='Place the blocks in the cubby as shown in the Cubby Layout. Once you are done press okay.'
                                 ,font=("Helvetica", 18))
        instructions.grid(row=0, column =0, pady=20)
        
        okay_button = ttk.Button(root_game_instructions,
                                text='Okay')
        okay_button.grid(row=1, column =0, pady=20)
        okay_button['command'] = lambda: instruction_pop_up2(root_game_instructions,instructions,okay_button)
        
        def time_check():
            root_game_instructions.focus_force()
            root_game_instructions.after(500, time_check)
    
        root_game_instructions.after(500, time_check)
    
    def instruction_pop_up2(root_game_instructions,instructions,okay_button):
        instructions.config(text='The objective is to make the robot pick up three blocks from the cubby.',
                            font=("Helvetica", 18))
        root_game_instructions.iconposition(20, 1000)
        
        
    
        okay_button['command'] = lambda: root_game_instructions.destroy()
    
    instruction_pop_up() 
    root.mainloop()


'''
Begins the game and board. Also adds number to the boxes.
Please note that the boxes are hard coded to be a set pattern
This function doesn't currently gernerate a random sequence of 
boxes and colors. The pattern can be changed at the end function
'''
def grid_create(canvas): 
    Random_Number_of_Boxes = randint(4,15) 
    Box_Postion = sample(xrange(0,15), 6)
    Box_Postion.sort()
    
    # They fill up the board by default with white boxes
    for k in range(4):
        for j in range(4):
            num = canvas.create_rectangle(25 + 150 * j, 25 + 150 * k, 125 + j * 150,
                                           125 + k * 150, fill="white")
            canvas.create_text((75 + 150 * j, 75 + 150 * k), text=(j + k * 4+1),
                                font=('Times New Roman', 20))
            box.append(num)
            
    Possible_colors = ['red','red','red','red','red','green','green','green','green','green','blue','blue','blue','blue','blue','blue']
    shuffle(Possible_colors)
    shuffle(Possible_colors)
    
    Box_index = 0
    while True:
        if Box_index == len(Box_Postion) - 1:
            break
        canvas.itemconfig(box[Box_Postion[Box_index]], fill=Possible_colors[Box_index])
        Box_index += 1
    
            
    # Manually chosen boxes and colors
#     canvas.itemconfig(box[0], fill="red")
#     canvas.itemconfig(box[6], fill="blue")
#     canvas.itemconfig(box[12], fill="blue")
#     canvas.itemconfig(box[15], fill="blue")
#     canvas.itemconfig(box[2], fill="green")
#     canvas.itemconfig(box[9], fill="green")
    
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
    insert_game_matrix(str(Last_Game_Number), str(box_matrix))
    np.savetxt('game.txt', box_matrix, fmt='%1d')
    
    print(box_new)
    
    
    # This creates the grid system on the canvas
    for k in range(4):
        # Row of Lines
        
        
        canvas.create_line(0, k * 150, 600, k * 150, width=3)
        
        # Column of lines
        canvas.create_line(k * 150, 0, k * 150, 600, width=3)
  
  
def consent_window():
    # Create the consent frame each time the game is restarted to give their consent
    # to be recorded
    try: 
        os.system('taskkill /im ffmpeg.exe /t /f')
    except: 
        print('The camera is not on!')
    root_content = Tkinter.Tk()
    
    # make it root the entire screen
#     w, h = root_content.winfo_screenwidth(), root_content.winfo_screenheight()
#     root_content.overrideredirect(1)
#     root_content.geometry("%dx%d+0+0" % (w, h))
#     
    root_content.attributes('-fullscreen', True)
    
    root_content.focus_set()
    root_content.focus()
      
#     root_content.focus_set() # <-- move focus to this widget
    root_content.bind("<Escape>", lambda e: e.widget.quit())
#     
    root_content.wm_title('Consent Window')
    consent_frame = ttk.Frame(root_content, padding = (25, 25))
    
    consent_frame.place(relx = .5,rely = .5, anchor = "center")
#   consent_frame.grid()
    
    # This is the consent box where the consent form is shown 
    
    consent_box = Text(consent_frame, width=60, height=40, background='white', wrap=WORD)
    
    
    consent_box.grid(row=0, column=1, pady=10)
    consent_scroll = Scrollbar(consent_frame)
    consent_scroll.config(command=consent_box.yview)
    consent_box['yscrollcommand'] = consent_scroll.set
    consent_scroll.grid(row=0,column=0, sticky=E)
    consent_box.insert(1.0, '                  Human-Robot Collaboration \n' 
                            '\n    You are being invited to participate in a research study about human-robot collaboration. ' 
                            'This study is being conducted by Dr. Ryder Winck and Dr. Carlotta Berry,' 
                            'from the Mechanical Engineering and Electrical and Computer Engineering Departments '
                            'at Rose-Hulman Institute of Technology. There are no known risks or costs if you decide ' 
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
                            'game, please contact Ryder Winck by email at winckrc@rose-hulman.edu. If you would like to have the data '
                            'associated with your participation deleted please be sure to remember the subject number that will be assigned '
                            'to you. \n'
                            '\n     If you have any questions about'
                            " your rights as a research subject or if you feel you've been placed at risk, you may contact the "
                            'Institutional Reviewer, Daniel Morris, by phone at (812) 877-8314, or by e-mail at morris@rose-hulman.edu. \n'
                            '\n    By clicking below you consent to participate in this study:')            
    consent_box.configure(state='disabled')
    
    # Create a button that says that they consent
    Consent_Button = ttk.Button(consent_frame,
                                     text='Consent to Terms')
    Consent_Button.grid(row=2, column =1, pady=5)
    
    
    Consent_Button['command'] = lambda: GUI_Main(root_content)
        
    Game_Number_Label = ttk.Label(consent_frame, text='Your Game number is ' + str(Last_Game_Number) + '.\n\n Please '
                                  'remember your game id. It will be displayed at the end one more time.', font=(44),
                                  foreground='red', anchor=N, justify=CENTER)
    
    Game_Number_Label.grid(row=1, column= 1, pady= 5)
    
    def time_check():
        root_content.focus_force()
        root_content.after(500, time_check)
    
    root_content.after(500, time_check)
    
    root_content.mainloop()
        

# After winning the game the restart button calls this function to start the game over
def Restart_Game(root_win, root, win_frame,text_box, canvas):
#     restart(canvas, box)
    global box, Last_Game_Number
    
    for k in range(16):
        canvas.delete(box[k])

    del box[:]
    
    root_updater(root, text_box, canvas)
    if root_win != None:
        root_win.destroy()
        
    with open('NLP_Speech.txt', 'w') as f:
        NLP_Speech = "Nothing said yet."
        f.write(NLP_Speech)   
        
#     root_updater(root, text_box, canvas)
    
    boxes_removed = 0
    
    root.destroy()
    
    Last_Game_Number += 1
    with open('Game_Number_Counter.txt', 'w') as f:
        f.write(str(Last_Game_Number))

    NLP_Speech = 'When talking to the robot please say a block color. End your sentence with "finish".'
    
    os.system('taskkill /im ffmpeg.exe /t /f')
    consent_window()
    

    
# This function is to change the text box color to red when the NLP is running then green when it is done
# Please note there is about a second and a half lag when starting the NLP
def Running(text_box, canvas, root, Run_Button): 
    global NLP_Speech
    Run_Button.config(state='disabled')
    insert_button_selection(str(Last_Game_Number), 'NLP')
    insert_button_selection(str(Last_Game_Number), 'leap_motion')
    
    
    argv = 'streaming_windows.py ' + str(Last_Game_Number)
    Running.nlp_process = subprocess.Popen(argv, shell=True)
#     
    time.sleep(3)
    Running.leap_process = subprocess.Popen('modular_prob_dist_sliding_window.py', shell=True)
    text_box.configure(background='yellow')
    text_box.update_idletasks()
    with open('NLP_Speech.txt', 'w') as f:
#         NLP_Speech = "Please say something like 'pick up the blue block finish' YOU MUST SAY FINISH!."
        NLP_Speech = ("Tell the robot what block you want to pick up. You need to say a color and when " 
                    "you are done talking you NEED TO SAY FINISH!")
        f.write(NLP_Speech)
        
    root_updater(root, text_box, canvas)
    
    
    
    
    def loop():
        global NLP_Speech
        
        if os.path.isfile('out_file.txt'):
            with open('NLP_Speech.txt', 'r') as f:
                # NLP send back a matrix filled with all -1 to indicated that it didn't understand
                if MainFunctions.checkMatrix(getMatrixFromFile('out_file.txt')) == False:
                    command = 'taskkill /F /pid ' + str(Running.nlp_process.pid)
                    os.system(command)
                    argv = 'streaming_windows.py ' + str(Last_Game_Number)
                    
                    Running.nlp_process = subprocess.Popen(argv, shell=True)                        
                    time.sleep(3)
                    NLP_Speech = ("Didn't catch that. Speak again! Be sure to say \n'block' and the block color "
                            "along with 'finish' once you are done talking.")
    
                    if os.path.isfile('out_file.txt'):
                        os.remove('out_file.txt')

                else:
                    NLP_Speech = f.readline()


        if (Running.nlp_process.poll() != None) & ( Running.leap_process.poll() != None):
            Run_Button.config(state='enabled')
            text_box.configure(background='red')
            root_updater(root, text_box, canvas)
            Matrix(text_box,canvas, root)

        else: 
#             print(Running.nlp_process.communicate())
            root_updater(root, text_box, canvas)
            running_loop = root.after(1000, loop)
    running_loop = root.after(1000, loop)

         
      
# This is to change the color of the text box to red when the matrixs are being 
# multiplied then back to green when done 
def Matrix(text_box, canvas, root):
    text_box.configure(background='yellow')
    text_box.update_idletasks()
    Matrix_Flag = Matrix_Multiplier()
    text_box.configure(background='red')
    
    Game_Check(text_box, canvas, root)
    
    text_box.update_idletasks()
    root_updater(root, text_box, canvas)
    

def Matrix_Multiplier():
    global previous_box, Box_Selected
    
    NLPTextFileName = "out_file.txt"
    NLPMatrixInit = "0,0,0,0\n0,0,0,0\n0,0,0,0\n0,0,0,0"
    
    NLPMatrix = getMatrixFromFile(NLPTextFileName)
    Leap_Matrix = getMatrixFromFile('Leap_Matrix.txt')
    insert_leap_motion_result(str(Last_Game_Number), str(Leap_Matrix))
    
    bool = checkMatrix(NLPMatrix)
    if bool == False:
        return str("Didn't catch that.")
    probabilityMatrix, maxNumberIndex = multiplyMatrices(Leap_Matrix, NLPMatrix)
    insert_decision_matrix(str(Last_Game_Number),str(probabilityMatrix))
    print('Leap_Matrix = ' + str(Leap_Matrix))

    Box_Selected = maxNumberIndex
    insert_decision_index(str(Last_Game_Number), str(maxNumberIndex))
    print(str(Box_Selected))


# this function comes after the consent window and shows a number for the game for the person to remember.
# 
def Game_Check(text_box, canvas, root):
    
    root_Game_Check = Tkinter.Tk()
    
    root_Game_Check.wm_title('Block Checker')
    Game_Check_Frame= ttk.Frame(root_Game_Check, padding = (25, 25))
    Game_Check_Frame.grid()
    
    Game_Check_Question_Label = ttk.Label(Game_Check_Frame, text='Is this the correct block ' + str(Box_Selected+1) +
                                          ' ?')
    Game_Check_Question_Label.grid(row=0, column= 0, pady= 5) 

    #Buttons to see if the box selected is correct
    Correct_Button = ttk.Button(root_Game_Check,
                                     text='Correct Block')
    Correct_Button.grid(row=1, column =0, pady=5, padx = 5)
    
    Correct_Button['command'] = lambda: Correct_Block(root_Game_Check,text_box, canvas, root)
    
    Wrong_Button = ttk.Button(root_Game_Check,
                                     text='Wrong Block')
    Wrong_Button.grid(row=1, column =1, pady=5, padx = 5)
    
    Wrong_Button['command'] = lambda: Wrong_Block(root_Game_Check,text_box, canvas, root)
    
    def time_check():
        root_Game_Check.focus_force()
        root_Game_Check.after(1000, time_check)
    
    root_Game_Check.after(1000, time_check)
    
    # This function writes to the robot file to move the robot if it is correct block picked
    def Correct_Block(root_Game_Check,text_box, canvas, root):
        global previous_box, boxes_removed, box
        
        insert_button_selection(str(Last_Game_Number), 1)
        with open('test.txt', 'w') as f:
            temp_Box_Selected = Box_Selected + 1
            f.write(str(temp_Box_Selected))
            
        # Deletes the box from the array which removes it from the screen after pressing update
        # then then it adds one to the amount of boxes removed.
        box_number = Box_Selected

        if box_number != "Nothing":
            print(box)
            print(box_new)
            print(previous_box)
            print(box_number)
            
            if box[box_number] != 0 & box_number != previous_box:
                canvas.delete(box[box_number])
                box[box_number] = 0
#                 box_new[box_number] = 0
                box_new[box_number] = 0
                print(box)
                print(box_new)
                
                box_matrix = np.reshape(box_new, (4,4))
                print(box_matrix)
                np.savetxt('game.txt', box_matrix, fmt='%1d')
                previous_box = box_number
                boxes_removed = boxes_removed + 1
                box_number = 'You got block: ' + str(box_number + 1) + ' ! Nice job! '
        #                 read_box_selected = 1
            
            elif box_number == previous_box:
                box_number = 'This was the last box that was selected. Please try again.'
            
            else:
                pass
            

        root_updater(root, text_box, canvas)      
        root_Game_Check.destroy()
        
         
    # This function does nothing and just tells the user to start over.
    def Wrong_Block(root_Game_Check, text_box, canvas, root):
        global previous_box, boxes_removed, box, NLP_Speech
    
        insert_button_selection(str(Last_Game_Number), 0)
        with open('NLP_Speech.txt', 'w') as f:
            NLP_Speech = "Click RUN again to try and get the robot to pick up the correct block."
            f.write(NLP_Speech)
        

        root_updater(root, text_box, canvas)
        root_Game_Check.destroy()
        

# This is the temporary fix to update the gui after clicking the buttons would like to have it 
# update automatically which requires multithreading
def root_updater(root, text_box, canvas):
    global boxes_removed, read_box_selected, previous_box, Box_Selected, Timer_Check
    
    text_box.configure(state='normal')
    text_box.delete('1.0', END)
             
             
    # This opens up the text file to determine the box number to put
    # in the text file and also the robot status
    with open('test.txt', 'r') as f:
        if f.readline == 'DONE':
            box_number = f.readline()
            Robot_Status = f.readline()
        else:
            Robot_Status = ''
            box_number = 'No Box Selected'
            

    # Game logic to count how many blocks are picked up and then when it reaches 3
    # a new window pops up telling the user that they won and need to press the restart
    # button on the new window.
    if boxes_removed == 3:
        boxes_removed = 0
        root_win = Tkinter.Toplevel()
        win_frame = ttk.Frame(root_win, padding = (25, 25))
        win_frame.grid()
        win_frame.focus_set()
        # Label for the win frame
        win_label = Label(win_frame, text='Congratulations on getting three blocks! You win! \n' 
                        ' Now click the restart button to begin a new game! \n'
                        '\nYour Game number is: ' + str(Last_Game_Number) + '.')
        win_label.grid(row = 0, column = 0)
        restart_button = ttk.Button(win_frame,
                                    text='Restart Game')
        restart_button.grid(row=7, column=0, sticky=W,pady=5)
        restart_button['command'] = lambda: Restart_Game(root_win, root, win_frame,text_box, canvas)
        
        def time_check():
            root_win.focus_force()
            root_win.after(500, time_check)
    
        root_win.after(500, time_check)
        
        
    # What is put into the text box
    text_box.insert(1.0, 
                    
                    'NLP Speech: ' + str(NLP_Speech) + '\n' + 'Leap Motion: ' \
                    'The leap motion is running make sure you point over the top about 6 inches with the pencil.'
                    ' If you feel it is taking  awhile it will time out after about a minute so be patient please.')
#     if Timer_Check == 1:
#         text_box.configure(background = 'blue')
#         text_box.insert(1.0, 'You have 5 seconds to click continue to stop the game from restarting.')
#     text_box.configure(background = 'yellow')
    text_box.configure(state='disabled')
    # update the GUI
    text_box.update_idletasks()
    canvas.update_idletasks()
    root.update_idletasks()
    
def Quit_Button_Function(root, text_box, canvas):
    global Last_Game_Number

    
    Root_Quit = Tkinter.Toplevel()
    
    Quit_Frame= ttk.Frame(Root_Quit, padding = (25, 25))
    Quit_Frame.grid()

    
    Delete_CheckBox_Check = BooleanVar()
    Delete_Checkbox = Checkbutton(Quit_Frame, text='Delete my data!', variable = Delete_CheckBox_Check)
    Delete_Checkbox.grid(row=1, column=0, pady=5, padx=5, sticky = W)    
    
    Delete_Label = ttk.Label(Quit_Frame, text='Are you sure you to quit? \n'
                                            'If you want your data deleted check the box and then press Quit. '
                                            'Otherwise data will be stored. \nYour Game number is: ' +
                                            str(Last_Game_Number) + '.' )
    Delete_Label.grid(row=0, column=0, pady=5, padx=5)
    
    Quit_Button_Second = ttk.Button(Quit_Frame,
                                     text='Quit')
    Quit_Button_Second.grid(row=2, column =0, pady=5, padx=5)
    
    Quit_Button_Second['command'] = lambda: Quit_Button_Function_Continue()
    
    def time_check():
        Root_Quit.focus_force()
        Root_Quit.after(1000, time_check)
    
    Root_Quit.after(1000, time_check)
    
    def Quit_Button_Function_Continue():
        global Last_Game_Number
        
        try: 
            if (Running.nlp_process.poll() == None) & ( Running.leap_process.poll() == None):
                command = 'taskkill /F /pid ' + str(Running.leap_process.pid)
                os.system(command)
                command = 'taskkill /F /pid ' + str(Running.nlp_process.pid)
                os.system(command)
        except: 
            print('have not ran module yet.')
            
        delete = False
        
        Last_Game_Number += 1
        with open('Game_Number_Counter.txt', 'w') as f:
            f.write(str(Last_Game_Number))
            
        for k in range(15):
            canvas.delete(box[k])
    
        del box[:]
        
        boxes_removed = 0
        
        with open('NLP_Speech.txt', 'w') as f:
            NLP_Speech = "Nothing said yet."
            f.write(NLP_Speech)   
        
#         root_updater(root, text_box, canvas)
        
        if str(Delete_CheckBox_Check.get()) == "True":
            os.system('taskkill /im ffmpeg.exe /t /f')
            time.sleep(2)
            os.remove(video_dst)

            delete_game(str(Last_Game_Number - 1))
            delete = True
        
        NLP_Speech = 'When talking to the robot please say a block color. End your sentence with "finish".'
        root.destroy()
        if delete == True:
            pass
        else:
            
            os.system('taskkill /im ffmpeg.exe /t /f')
        
        
        consent_window()
    

def main():
    
    consent_window()
    

if __name__ == '__main__':
    main()


