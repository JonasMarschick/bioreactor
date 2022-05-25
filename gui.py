# this code is python 3 compatible
# Importing Libraries

import RPi.GPIO as GPIO
import time
from tkinter import *
#import tkinter.font

# Libraries Imported successfully

# Raspberry Pi 3 Pin Settings

PWMPin = 11 # PWM Pin connected to ENA.
motor1A = 16 # Connected to Input 1.
motor1B = 18 # Connected to Input 2.

#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # We are accessing GPIOs according to their physical location

GPIO.setup(PWMPin, GPIO.OUT) # We have set our pin mode to output
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
############################


#Now set the start speed to be LOW

GPIO.output(PWMPin, GPIO.LOW) # When it will start then all Pins will be LOW.
GPIO.output(motor1A, GPIO.LOW)
GPIO.output(motor1B, GPIO.LOW)
#############################



PwmValue = GPIO.PWM(PWMPin, 255) # We have set our PWM frequency to 2000.

PwmValue.start(40) # That's the maximum value 100 %.

# Raspberry Pi 3 Pin Settings Completed

# tkinter GUI basic settings

gui = Tk()
gui.title("Spinfinity")
gui.config(background= "grey1")
#Gui.minsize(800,400)
gui.geometry( '800x400')
gui.resizable( True , True)
Grid.rowconfigure(gui , 0 , weight = 1)
Grid.columnconfigure(gui , 0 , weight = 1)

#Font1 = tkinter.font.Font(family = 'Helvetica', size = 18, weight = 'bold')

# tkinter simple GUI created

def motorClockwise():
    GPIO.output(motor1A, GPIO.LOW) # Motor will move in clockwise direction.
    GPIO.output(motor1B, GPIO.HIGH)
    
def motorAntiClockwise():
    GPIO.output(motor1A, GPIO.HIGH) # Motor will move in anti-clockwise direction.
    GPIO.output(motor1B, GPIO.LOW)

def motorStop():
    GPIO.output(motor1A, GPIO.LOW) # Motor will stop.
    GPIO.output(motor1B, GPIO.LOW)
    
def ChangePWM(self):
    PwmValue.ChangeDutyCycle(Scale1.get())
####


	
	

Button1 = Button(gui, text='Clockwise Motor ', command = motorClockwise, bg='green2', height = 2, width = 15)
Button1.grid(row=0,column=0, sticky = "NSEW" )

Button3 = Button(gui, text='Counter Clockwise ', command = motorAntiClockwise, bg='deep sky blue',  height = 2, width = 15)
Button3.grid(row=0,column=1, sticky = "NSEW" )

Button2 = Button(gui, text=' Motor  Stop', command = motorStop, bg='red', height = 2, width = 15)
Button2.grid(row=0,column=2, sticky = "NSEW" )

Text3 = Label(gui,text='Motor  RPM', bg = 'grey1', fg='#FFFFFF', height = 2, width = 15)
Text3.grid(row=1,column = 0 , columnspan=1 , sticky = "NSEW" )

Scale1 = Scale(gui, from_=40, to=100, orient = HORIZONTAL, resolution = 1, command = ChangePWM, length=250, width=15)
Scale1.grid(row=1,column=2,  sticky = "NSEW" )

########################################



gui.mainloop()
