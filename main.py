import sqlite3
#import time

import gui
#import raspberry

conn = sqlite3.connect("programs.db")
cursor = conn.cursor()
cursor.execute("SELECT *, oid FROM program ORDER BY programNumber")
fetch = cursor.fetchall()
print(fetch)

print("hey")

numOfProgram = 2

def pullData(entry):


    global numOfProgram
    numOfProgram = entry



if __name__ == "__main__":

    root = gui.Gui()
    #cursor.execute("SELECT *, oid FROM program WHERE programNumber = 2 ")
    root.mainloop()

    #processor = raspberry.RaspberryConfiguration()

    ### Muss wissen in welchem Reiter ich bin!

    #processor.motorClockwise(processor.MOTOR1A , processor.MOTOR1B)

    ### Datenbank an das jeweilig ausgewählte Programm anpassen, sprich alle anderen Programme werden ab jetzt nich
    ### mehr beachtet

    print(cursor.fetchall())






    ### Muss wissen was die Werte des  Paares  Zeit und Drehzahl sind und wie viele Paare es bis zum Programende gibt
    ###processor.changePWM(Drehzahl1)
    # Zeit einstellen
    # processor.changePWM(Drehzahl1)
    #.
    #.
    #.
    #processor.changePWM(DrehzahlN)
    #processor.motorStop(processor.MOTOR1A , processor.MOTOR1B)
