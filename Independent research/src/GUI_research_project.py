"""
<describe what this module has/does>

Created on Sep 25, 2016.
Written by: gishbd.
"""

import Tkinter
from Tkinter import Tk
import time
# import LeapMotion

def main():

    root = Tkinter.Tk()
    mainframe = Tkinter.Frame(root)
    mainframe.grid()

    global dog
    dog = True
    shape_objects = Tkinter.Frame(mainframe, borderwidth=10, relief='groove')
    square = Tkinter.Radiobutton(shape_objects, text='Square',
                             value='square')
    circle = Tkinter.Radiobutton(shape_objects, text='Circle',
                             value='circle')
    triangle = Tkinter.Radiobutton(shape_objects, text='Triangle',
                             value='triangle')

    button = Tkinter.Button(mainframe, text='Reset the other widgets')

    radio_observer = Tkinter.StringVar()
    for radio in [square, circle, triangle]:
        radio['variable'] = radio_observer  # They all need the SAME observer

    for radio in [square, circle, triangle]:
        radio['command'] = lambda: radiobutton_changed(radio_observer)
    c = 0
    for widget in [shape_objects, button]:
        widget.grid(row=0, column=c, padx=20)
        c = c + 1

    for radio in [square, circle, triangle]:
        radio.grid(sticky='w')


    correct_button = Tkinter.Button(root, text='Correct')
    correct_button['command'] = lambda: print_things()
    correct_button.grid()
    def print_things():
        if dog == True:
            print('You are Correct')

        else:
            print('You chose Incorrectly')



    triangle = Tkinter.PhotoImage(file="Trianglemovoing.gif")
    print(triangle)
    block_layout = Tkinter.Frame(root, height=400, width=400)
    block_layout.grid()



    for k in range(0, 4):
        for n in range(0, 4):
            button = Tkinter.Button(block_layout, height=5, width=10)


            button.grid(row=n, column=k)


    root.mainloop()



def radiobutton_changed(radiobutton_observer):
    print('The Robot is searching for a', radiobutton_observer.get())

#-----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
