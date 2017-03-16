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
    
Author: BRYAN GISH
Date Created: 3/11/2016

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
from LeapPython import Controller_is_connected_get
#
#
#
class consent_window():
    
    def __init__(self,master):
        
        self.lastGameNumber = open('Game_Number_Counter.txt','r').read()
        self.root_content = master
        self.root_content.wm_title('Consent Window')
        self.consent_frame = ttk.Frame(self.root_content, padding = (25, 25))
        self.consent_frame.grid()
        self.cssts()
    
    def fullScreen():
    
        w, h = root_content.winfo_screenwidth(), root_content.winfo_screenheight()
        root_content.overrideredirect(1)
        root_content.geometry("%dx%d+0+0" % (w, h))
          
        root_content.focus_set() # <-- move focus to this widget
        root_content.bind("<Escape>", lambda e: e.widget.quit())
    
    def cssts(self):
    
    
    # This is the consent box where the consent form is shown 

        consent_box = Text(self.consent_frame, width=50, height=15, background='white', wrap=WORD)
        consent_box.focus()
        consent_box.grid(row=0, column=1, pady=10)
        consent_scroll = Scrollbar(self.consent_frame)
        consent_scroll.config(command=consent_box.yview)
        consent_box['yscrollcommand'] = consent_scroll.set
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
        Consent_Button = ttk.Button(self.consent_frame,
                                         text='Consent to Terms')
        Consent_Button.grid(row=2, column =1, pady=5)
        
        
        Consent_Button['command'] = lambda: gameBoardAndBlocks(self.root_content,5)
            
        Game_Number_Label = ttk.Label(self.consent_frame, text='Your Game number is ' + str(self.lastGameNumber) + '.\n\n Please '
                                      'remember your game id. It will be displayed at the end one more time.', font=(44),
                                      foreground='red', anchor=N, justify=CENTER)
        
        Game_Number_Label.grid(row=1, column= 1, pady= 5)
    
        self.root_content.mainloop()
        

class gameBoardAndBlocks:
      
    def __init__(self,size,master):
        consent_window.__init__(self, master)
        self.counter = 0
        self.timer = 0
        self.currentBlock = 0
        self.box = []
        self.master = master
        self.lastGameNumber = open('Game_Number_Counter.txt','r').read()
        
        self.main_frame = ttk.Frame(self.master, padding=(25, 25))
        self.main_frame.grid()
        
        self.canvas = Canvas(self.main_frame, width=600, height=600)
        self.canvas.grid()
        self.createGrid()
        self.positionBlocks()
    
        
    def createCanvas(self,size):
        self.canvas = Canvas(self.main_frame, width=600, height=600)
        self.canvas.grid()
         
    def createGrid(self):
        for k in range(4):
        # Row of Lines
            self.canvas.create_line(0, k * 150, 600, k * 150, width=3)
        # Column of lines
            self.canvas.create_line(k * 150, 0, k * 150, 600, width=3)      
         
    def positionBlocks(self):
        box_new = [0]*16
        #Random_Number_of_Boxes = randint(5,15) 
        Box_Postion = sample(xrange(0,15), 6)#Random_Number_of_Boxes)#
        print(Box_Postion)
        Box_Postion.sort()
        Possible_colors = ['red','red','red','red','red','green','green','green','green','green','blue','blue','blue','blue','blue','blue']
        shuffle(Possible_colors)
        shuffle(Possible_colors)
        
        for k in range(4):
            for j in range(4):
                num = self.canvas.create_rectangle(25 + 150 * j, 25 + 150 * k, 125 + j * 150,
                                           125 + k * 150, fill="white")
                self.canvas.create_text((75 + 150 * j, 75 + 150 * k), text=(j + k * 4),
                                font=('Times New Roman', 20))
                self.box.append(num)
            
        Box_index = 0
        while True:
            if Box_index == len(Box_Postion) - 1:
                break
            self.canvas.itemconfig(self.box[Box_Postion[Box_index]], fill=Possible_colors[Box_index])
            Box_index += 1
        
        for k in range(16):
            if self.canvas.itemcget(self.box[k], "fill") == "white":
                self.canvas.delete(self.box[k])
                self.box[k] = 0
                box_new[k] = 0
                
            elif self.canvas.itemcget(self.box[k], "fill") == "red":
                box_new[k] = 1
                
            elif self.canvas.itemcget(self.box[k], "fill") == "green":
                box_new[k] = 2
                
            else:
                box_new[k] = 3
        
    # This reshapes the two d array of boxes to matrix and saves it to the 
    # game text file.
        box_matrix = np.reshape(box_new, (4,4))
        #insert_game_matrix(str(self.lastGameNumber), str(box_matrix))
        np.savetxt('game.txt', box_matrix, fmt='%1d')
   
def main():
    
    root = Tk()
    
    consentTerms = consent_window(root)
    #gui = gameBoardAndBlocks(5,root)
    root.mainloop()
     
if __name__ == "__main__":
    main()

 