import RPi.GPIO as GPIO
import time

# Raspberry Pi 3 Pin Settings

class RaspberryConfiguration():

    def __init__(self):

        self.PWMPIN = 11 # PWM Pin connected to ENA.
        self.MOTOR1A = 16 # Connected to Input 1.
        self.MOTOR1B = 18 # Connected to Input 2.
        self.PWMPin2 = 36 #Motor 2
        self.Motor2A = 38
        self.Motor2B = 40
        self.PWMPin3 = 29#Motor 3
        self.Motor3A = 31
        self.Motor3B = 33
        self.PWMPin4 = 32 #Motor 4
        self.Motor4A = 35
        self.Motor4B = 37
        self.PWMPin5 = 22 #Motor 5
        self.Motor5A = 24
        self.Motor5B = 26
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) # We are accessing GPIOs according to their physical location

        GPIO.setup(self.PWMPin, GPIO.OUT) # We have set our pin mode to output
        GPIO.setup(self.Motor1A, GPIO.OUT)
        GPIO.setup(self.Motor1B, GPIO.OUT)
        ############################
        GPIO.setup(self.PWMPin2, GPIO.OUT) # We have set our pin mode to output
        GPIO.setup(self.Motor2A, GPIO.OUT)
        GPIO.setup(self.Motor2B, GPIO.OUT)
        ############################
        GPIO.setup(self.PWMPin3, GPIO.OUT) # We have set our pin mode to output
        GPIO.setup(self.Motor3A, GPIO.OUT)
        GPIO.setup(self.Motor3B, GPIO.OUT)
        ############################
        GPIO.setup(self.PWMPin4, GPIO.OUT) # We have set our pin mode to output
        GPIO.setup(self.Motor4A, GPIO.OUT)
        GPIO.setup(self.Motor4B, GPIO.OUT)
        ############################
        GPIO.setup(self.PWMPin5, GPIO.OUT) # We have set our pin mode to output
        GPIO.setup(self.Motor5A, GPIO.OUT)
        GPIO.setup(self.Motor5B, GPIO.OUT)

        #Now set the start speed to be LOW

        GPIO.output(self.PWMPin, GPIO.LOW) # When it will start then all Pins will be LOW.
        GPIO.output(self.Motor1A, GPIO.LOW)
        GPIO.output(self.Motor1B, GPIO.LOW)
        #############################
        GPIO.output(self.PWMPin2, GPIO.LOW) # When it will start then all Pins will be LOW.
        GPIO.output(self.Motor2A, GPIO.LOW)
        GPIO.output(self.Motor2B, GPIO.LOW)
        #############################
        GPIO.output(self.PWMPin3, GPIO.LOW) # When it will start then all Pins will be LOW.
        GPIO.output(self.Motor3A, GPIO.LOW)
        GPIO.output(self.Motor3B, GPIO.LOW)
        #############################
        GPIO.output(self.PWMPin4, GPIO.LOW) # When it will start then all Pins will be LOW.
        GPIO.output(self.Motor4A, GPIO.LOW)
        GPIO.output(self.Motor4B, GPIO.LOW)
        #############################
        GPIO.output(self.PWMPin5, GPIO.LOW) # When it will start then all Pins will be LOW.
        GPIO.output(self.Motor5A, GPIO.LOW)
        GPIO.output(self.Motor5B, GPIO.LOW)



        PwmValue = GPIO.PWM(self.PWMPin, 255) # We have set our PWM frequency to 2000.
        PwmValue2 = GPIO.PWM(self.PWMPin2, 255) # We have set our PWM frequency to 2000.
        PwmValue3 = GPIO.PWM(self.PWMPin3, 255) # We have set our PWM frequency to 2000.
        PwmValue4 = GPIO.PWM(self.PWMPin4, 255) # We have set our PWM frequency to 2000.
        PwmValue5 = GPIO.PWM(self.PWMPin5, 255) # We have set our PWM frequency to 2000.
        PwmValue.start(40) # That's the maximum value 100 %.
        PwmValue2.start(40) # That's the maximum value 100 %.
        PwmValue3.start(40) # That's the maximum value 100 %.
        PwmValue4.start(40) # That's the maximum value 100 %.
        PwmValue5.start(40) # That's the maximum value 100 %.

        # Raspberry Pi 3 Pin Settings Completed


    def motorClockwise( self , MOTORA , MOTORB):
        GPIO.output(MOTORA , GPIO.LOW)  # Motor will move in clockwise direction.
        GPIO.output(MOTORB, GPIO.HIGH)

    def motorStop( self , MotorA , MotorB):
        GPIO.output(MotorA, GPIO.LOW)  # Motor will stop.
        GPIO.output(MotorB, GPIO.LOW)

    def changePWM( self , RPM):
        PwmValue.ChangeDutyCycle(RPM)


