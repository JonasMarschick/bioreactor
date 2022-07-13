from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
#import tkinterFont


class GuiNumberField(ThemedTk):

    def __init__(self):

        ThemedTk.__init__(self)

        self.string = ""

        self.title("Number Entry")
        self.geometry("400x400")
        self.frame = ttk.Frame(self)
        self.frame.pack(fill="both", expand=True)

        self.initGui()
        self.generateButtons()
        self.resizable(self.frame) # This function should always be initiliazed last, as if not the gui isn't scalable. Try swapping line 17 and 18 and look what happens

    def initGui(self):

        self.Entry = ttk.Entry(self.frame , width = "5"  , justify = tk.CENTER , font = ( None , 50 , "bold")) #, font = tkfont.Font( family = "Helvetica" , size = 36 , weigth = "bold"))
        self.Entry.grid( row = 0 , column = 0 , columnspan = 2 , rowspan = 2 , sticky = "NESW")

        enterButton = ttk.Button(self.frame , text = "Enter" , command = lambda : self.enterEntry())
        enterButton.grid( row = 0 , column = 2 , sticky = "NESW")
        deleteButton = ttk.Button(self.frame , text = "Delete" , command = lambda : self.deleteEntry())
        deleteButton.grid( row = 1 , column = 2 , sticky = "NESW")

    def generateButtons(self):

        rows = [ 2 , 3 , 4 ]
        columns = [ 0 , 1 , 2]
        number = 1

        for r in rows:
            for c in columns:


                addButton = ttk.Button(self.frame , text = str(number) , command = lambda number = number : self.submitData( str(number) ))
                addButton.grid( row = r , column = c , sticky = "NESW")

                number += 1

    def resizable(self , frame):

        tuple = frame.grid_size()

        for i in range(tuple[0]):

            frame.columnconfigure( i , weight = 1 , minsize = 2)

        for i in range(tuple[1]):

            frame.rowconfigure( i , weight = 1 , minsize = 2 )

    def submitData(self , text):

        self.Entry.delete(0)
        self.string = text
        self.Entry.insert( 0 , self.string)

    def deleteEntry(self):

        self.Entry.delete(-1)


    def enterEntry(self):

        if self.string != "":

            self.Entry.delete(0)
            self.destroy()

        else:

            pass





if __name__ == "__main__":

    app = GuiNumberField()
    app.mainloop()