import RPi.GPIO as GPIO
import time

# Raspberry Pi 3 Pin Settings

class RaspberryConfiguration():

    def __init__(self):

        self.dicSetup = { "PWMPin1" : 11 , "MOTOR1A" : 16 , "MOTOR1B" : 18 ,
                     "PWMPin2" : 36 , "MOTOR2A" : 38 , "MOTOR2B" : 40,
                     "PWMPin3" : 31 , "MOTOR3A" : 31 , "MOTOR3B" : 33,
                     "PWMPin4" : 32 , "MOTOR4A" : 35 , "MOTOR4B" : 37,
                     "PWMPin5" : 22 , "MOTOR5A" : 24 , "MOTOR5B" : 26}
        
        self.listDicSetupKeys = list(self.dicSetup)

        self.list = []

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD) # We are accessing GPIOs according to their physical location

        listOfIndexofPWMPin = ( 0 , 3 , 6 , 9 , 12)
        
        self.printdic()

        for i in listOfIndexofPWMPin:
            for j in range(3):
                
                    key = str(self.listDicSetupKeys[i])
              
                    GPIO.setup( self.dicSetup[key] , GPIO.OUT)
                    GPIO.output( self.dicSetup[key] , GPIO.LOW)
                    i += 1

        for i in listOfIndexofPWMPin:

            key = str(self.listDicSetupKeys[i])
            PwmValue = GPIO.PWM(self.dicSetup[key], 255)  # We have set our PWM frequency to 2000.
            PwmValue.start(40) # That's the maximum value 100 %.
            self.list.append(PwmValue)


        '''
        print("hope not")
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
        '''

        # Raspberry Pi 3 Pin Settings Completed
        
    def printdic(self):
        
        print(self.dicSetup["MOTOR1A"])


    def motorClockwise( self , MOTORA , MOTORB):
        GPIO.output(MOTORA , GPIO.LOW)  # Motor will move in clockwise direction.
        GPIO.output(MOTORB, GPIO.HIGH)

    def motorStop( self , MotorA , MotorB):
        GPIO.output(MotorA, GPIO.LOW)  # Motor will stop.
        GPIO.output(MotorB, GPIO.LOW)

    def changePWM( self , int , RPM):
        self.list[int].ChangeDutyCycle(RPM)
