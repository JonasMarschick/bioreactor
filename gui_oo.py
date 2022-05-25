import tkinter as tk
from tkinter import ttk
import time
import RPi.GPIO as GPIO


class Gui(tk.Tk):
  
  def __init__(self):
    
    super().__init__()
    
    self.geometry('800x400')
    
    self.title("Spinfinity")
    
    self.resizable(True , True)
    
    self.columnconfigure( 0 , weight = 1)
    
    self.columnconfigure( 1 , weight = 1)
      
    self.columnconfigure( 2 , weight = 1)
        
    self.rowconfigure( 0 , weight = 1)
          
    self.rowconfigure( 1 , weight = 1)
    
    self.create_widgets()
    
  def create_widgets(self):
    
    clockwise_button = tkk.Button( self , text='Clockwise Motor ', command = motorClockwise, bg='green2', height = 2, width = 15)
    
    clockwise_button.grid(row=0,column=0, sticky = "NSEW" )
    
    
    anti_clockwise_button = ttk.Button(self, text='Counter Clockwise ', command = motorAntiClockwise, bg='deep sky blue',  height = 2, width = 15)
    anti_clockwise_button.grid(row=0,column=1, sticky = "NSEW" )

    motor_stop_button = ttk.Button(self, text=' Motor  Stop', command = motorStop, bg='red', height = 2, width = 15)
    motor_stop_button.grid(row=0,column=2, sticky = "NSEW" )

    motor_rpm_text = ttk.Label(self,text='Motor  RPM', bg = 'grey1', fg='#FFFFFF', height = 2, width = 15)
    motor_rpm_text.grid(row=1,column = 0 , columnspan=1 , sticky = "NSEW" )

    rpm_scale = ttk.Scale(gui, from_=40, to=100, orient = HORIZONTAL, resolution = 1, command = ChangePWM, length=250, width=15)
    rpm_scale.grid(row=1,column=2)

    
    
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


if __name__ == "__main__":
    gui = Gui()
    gui.mainloop()


    
    
    
    
  
            
    
