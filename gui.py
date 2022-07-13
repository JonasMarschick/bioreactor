#from tkinter import*
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as filedialog
import tkinter.tix as tix
import csv
import os
import sqlite3
from ttkthemes import ThemedTk
import threading
#import raspberry
import time
from PIL import ImageTk, Image

string = ""

class Gui(ThemedTk):

    def __init__(self):

        ThemedTk.__init__(self)

        self.choseProgram = ""
        self.count = 0
        self.count2 = 0 # has something to do with the standard unit of time, if it is in seconds or in hours
        self.theme = ""
        self.mydata = []
        self.comboBoxList = []
        self.programNumberList = []
        self.uniqueProgramNumberList = []
        self.threadAlive = False
        self.timeMode = 60 * 60
        self.timeModeList = (60 * 60 , 1 , "H" , "Sec") # normally a program should run for x hours, but for testing purposes it is more convenient to change the standard time to seconds

        self.initGui()
        self.database()
        self.centerWindow()
        self.resizable(self.frame1)
        self.resizable(self.actionButtonFrame)
        self.mode()
        self.set_theme(self.theme)

        #self.raspberry = raspberry.RaspberryConfiguration()

    def initGui(self):

        self.protocol("WM_DELETE_WINDOW", self.disable_event)

        #self.geometry("500x500")
        self.minsize(800 , 500)
        self.style = ttk.Style()
        self.title ("Spinfinity")
        #self.style = ttk.Style()
       # print(self.style.theme_names()) #Gives an option of the themes that are available
        #self.style.theme_use("alt")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand = 1  , fill = "both")

        self.frame1 = ttk.Frame(self.notebook)
       # self.frame1.config( bg = "azure")
        self.frame1.pack( fill = "both" , expand = True  )
        self.notebook.add(self.frame1 , text = "Bioreactor #1")
        self.frame2 = ttk.Frame(self.notebook )
        self.frame2.pack( fill = "both" , expand = True)
        self.notebook.add(self.frame2 , text = "Bioreactor #2")

        self.tree = ttk.Treeview( self.frame1 , columns = ("RPM" , "time") , selectmode = "extended")
        self.tree.heading("#0" , text = "Program Number")
        self.tree.heading("#1" , text = "RPM(MIN\u207B\u00B9):")
        self.tree.heading("#2" , text= "TIME(H)")
        self.tree.grid(row = 2 , column = 0  , rowspan = 4 , columnspan = 6 , sticky = "NSEW" )
        #self.database()

        label1 = ttk.Label( self.frame1 , text = ("Program" + "\n" + "Number") + ":")
        label1.grid( row = 0 , column = 0 , sticky = "W")
        self.programEntry = ttk.Entry(self.frame1 , width = 5)
        self.programEntry.grid( row = 0 , column = 1 ,  sticky = "EW" )
        self.programEntry.bind("<1>" , self.handleClickProgramEntry)


        label2 = ttk.Label(self.frame1 , text = "RPM(MIN\u207B\u00B9):")
        label2.grid( row = 0 , column = 2 )
        label3 = ttk.Label(self.frame1 , text = " Scale:")
        label3.grid( row = 1 , column = 2)
        self.rpmEntry = ttk.Entry(self.frame1 , width = 5)
        self.rpmEntry.grid( row = 0 , column = 3 ,  sticky = "EW")
        self.rpmEntry.bind("<1>" , self.handleClickRpmEntry)
        self.rpmScale = tk.Scale( self.frame1 , from_ = 0 , to = 100 , orient = tk.HORIZONTAL , resolution = 5)
        self.rpmScale.grid( row = 1 , column = 3 , sticky = "EW")

        self.label4 = ttk.Label(self.frame1, text = "TIME(H):")
        self.label4.grid ( row = 0 , column = 4)
        label5 = ttk.Label(self.frame1 , text = "Scale:")
        label5.grid( row = 1 , column = 4 )
        self.timeEntry = ttk.Entry(self.frame1 , width = 5)
        self.timeEntry.grid( row = 0  , column = 5 ,  sticky = "EW" )
        self.timeEntry.bind("<1>" , self.handleClickTimeEntry)
        self.timeScale = tk.Scale( self.frame1 , from_ = 0 , to = 100 , orient = tk.HORIZONTAL , resolution = 1)
        self.timeScale.grid( row = 1 , column = 5 , sticky = "EW")

        addButton = ttk.Button(self.frame1 , text = "Add"  , width = 5 ,
                              command = lambda : self.submitData(self.rpmEntry , self.timeEntry , self.programEntry , self.rpmScale , self.timeScale))
        addButton.grid( row = 0  , column = 6 ,  sticky = "EW" , padx = 20)
        removeButton = ttk.Button( self.frame1 , text = "Remove", width = 5 ,
                               command = lambda : self.onRemove(self.tree.selection() , self.rpmEntry , self.timeEntry , self.programEntry , self.rpmScale , self.timeScale ))
        removeButton.grid( row = 1 , column = 6 , sticky ="EW" , padx = 20)

        self.actionButtonFrame = ttk.Frame(self.frame1  , width = 5 )
        self.actionButtonFrame.grid(row = 3 , column = 6 , sticky = "EW" , padx = 20)
        self.choseProgramCombobox = ttk.Combobox(self.actionButtonFrame, values=self.comboBoxList,  text="Choose a" + "\n" + "Program", width=5)
        self.choseProgramCombobox.grid( row=0 , column=0 , columnspan = 2 ,  sticky="WE" )
        # choseProgramCombobox.bind('<<ComboboxSelected>>' , self.someFunction)
        initiateProgramButton = ttk.Button ( self.actionButtonFrame , text = "Start" + "\n" + "Program" , command = lambda : self.initiateProgram)
        initiateProgramButton.grid ( row = 1 , column = 0 , sticky = "EW")
        terminateProgramButton = ttk.Button(self.actionButtonFrame , text = "Terminate" + "\n" + "Program" , command = self.terminateProgram)
        terminateProgramButton.grid ( row = 1 , column = 1 , sticky = "EW")
        #self.style.configure(green.TProgressbar", foreground='green' , background = "black" , throughcolor = "black")
        self.progressBar = ttk.Progressbar(self.actionButtonFrame , mode = "determinate") # style = "green.TProgressbar
        self.progressBar.grid( row = 2 , column = 0 , columnspan = 2  ,  sticky = "NWE" , pady = 20)

        exportButton = ttk.Button( self.frame1 , text = "Export as" "\n" + " CSV" , command = self.export , width = 5 )
        exportButton.grid( row = 4 , column = 6 , sticky = "EW" , padx = 20 )

        modeButton = ttk.Button( self.frame1 , text = "Light/Dark" + "\n"  "mode" , command = self.mode , width = 5)
        modeButton.grid(row = 5 , column = 6 , sticky = "EW" , padx = 20)


    def onRemove(self , iids , rpmEntry , timeEntry , programEntry , rpmScale , timeScale):

        val0 = programEntry.get()
        val1 = rpmEntry.get()
        val2 = timeEntry.get()
        val3 = rpmScale.get()
        val4 = timeScale.get()

        conn = sqlite3.connect("programs.db")
        cursor = conn.cursor()
        sqlDeleteCondition = '''DELETE FROM 'program' WHERE programNumber = ? AND RPM = ? AND TIME = ? '''

        if (val0 == "" or val1 == "" or val2 == ""):

            string = str(iids[0])

            if ( string.isdigit()):

                cursor.execute(" SELECT *, oid FROM program WHERE programNumber = ?", (iids[0],))
                conn.commit()
                fetch = cursor.fetchall()

                for data in fetch:

                    cursor.execute( sqlDeleteCondition , data[0:3])
                    conn.commit()

                self.tree.delete(iids)

            else:

                for iid in iids:

                    dicValues = self.tree.item(iid)
                    parentIid = self.tree.parent(iid)
                    cursor.execute( sqlDeleteCondition , (parentIid, dicValues["values"][0] , dicValues["values"][1]))
                    conn.commit()

                    self.tree.delete(iid)

        elif (not val0 == "" and not val1 == "" and not val2 == ""):

            cursor.execute( sqlDeleteCondition , ( int(val0) , val1 , val2))
            self.tree.delete(* self.tree.get_children())
            conn.commit()
            self.loadDataBaseIntoTreeView()

        cursor.close()


    def submitData(self , rpmEntry , timeEntry , programEntry , rpmScale , timeScale):

        val0 = programEntry.get()
        val1 = rpmEntry.get()
        val2 = timeEntry.get()
        val3 = rpmScale.get()
        val4 = timeScale.get()

        conn = sqlite3.connect("programs.db")
        cursor = conn.cursor()

        if ( val3 == 0 and val4 == 0):

            if ( len(val1) == 0 or len(val2) == 0 or len(val0) == 0): # checks if all the necessary information to generate a new program subset is given

                tkMessageBox.showerror(title="WARNING", message="Please enter a program number , RPM and TIME value so that a new program subset can be created")

                return

            if ( val0 == "999" and val1 == "999" and val2 == "999"): # this is a quick fix to change the time from h to min, for testing purposes of the bioreactor

                i = 0

                if (self.count2 % 2 == 0):

                    i = 1

                else:

                    i = 0

                self.count2 += 1
                self.timeMode = self.timeModeList[i]

                self.tree.heading("#2", text= ("TIME(%(1)s)") % {"1" : self.timeModeList[ i + 2]})
                self.label4["text"] = ("TIME(%(1)s)") % {"1" : self.timeModeList[ i + 2]}

                tkMessageBox.showerror(title="WARNING",  message=( ("The standard measure of time has been changed to %(1)d seconds")  % {"1" : self.timeMode} ))

                self.easterEgg()

                return

            bol = self.tree.exists(val0)
            if (not bol):
                self.addNewProgram(val0)

            cursor.execute("INSERT INTO  'program' VALUES(:programNumber , :RPM , :TIME)",
                           {
                               'programNumber' : val0,
                               'RPM' : val1,
                               'TIME' : val2
                          })

            cursor.execute("SELECT *, oid FROM program")
            fetch = cursor.fetchall()

            for data in fetch:
                self.programNumberList.append(data[0])
            self.uniqueElementsOfList()

            conn.commit()
            cursor.close()

            self.tree.insert(val0 , index = "end" , values = (fetch[-1][1], fetch[-1][2]))

          #  programEntry.delete( 0 , "end")   # i find it anoying to always enter the program number again, if a new program is created, it will probably contain at least 2 rows of information
            rpmEntry.delete( 0 , "end")
            timeEntry.delete( 0  , "end")

        elif ( not val3 == 0 and not val4 == 0):


            if (len(val0) == 0 ): #  checks if a program  number is given

                tkMessageBox.showerror(title="WARNING", message="Please chose a program number, to which the RPM and TIME values "
                                       "should be added!")

                return

            if (not len(val1) == 0 or  not len(val2) == 0):

                if ( val1 != val3 or val2 != val4):

                    tkMessageBox.showerror(title="WARNING",  message="Please make sure that the number you entered for the parameter TIME or RPM matches the"
                                           " value selected with the corresponding scale")

                    return

            bol = self.tree.exists(val0)
            if (not bol):
                self.addNewProgram(val0)

            cursor.execute("INSERT INTO  'program' VALUES(:programNumber , :RPM , :TIME)",
                           {
                               'programNumber': val0,
                               'RPM': val3,
                               'TIME': val4
                           })

            cursor.execute("SELECT *, oid FROM program")
            conn.commit()
            fetch = cursor.fetchall()

            for data in fetch:
                self.programNumberList.append(data[0])
            self.uniqueElementsOfList()

            cursor.close()

            self.tree.insert(val0, index="end", values=(fetch[-1][1], fetch[-1][2]))

            #programEntry.delete(0, "end")
            rpmEntry.delete(0, "end")
            timeEntry.delete(0, "end")

        else:

            tkMessageBox.showerror( title = "WARNING" , message = "Please make sure that the value you selected with the"
                                                                  " RPM or TIME scale matches the value entered in the RPM or Time entry box")


    def addNewProgram(self, val0 ):

        branch = self.tree.insert("" , iid = val0 , index = "end" , text = "Progam" + str(val0))


    def centerWindow(self):

        windowWidth = self.winfo_screenwidth()
        windowHeight = self.winfo_screenheight()

        width = (windowWidth) / 3
        heigth = (windowHeight) / 3

        self.geometry('%dx%d' % (width , heigth))


    def resizable(self , frame):

        tuple = frame.grid_size()

        for i in range(tuple[0]):

            frame.columnconfigure( i , weight = 1 , minsize = 2)

        for i in range(tuple[1]):

            frame.rowconfigure( i , weight = 1 , minsize = 2 )


    def database(self):

        conn = sqlite3.connect("programs.db")
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS program (
                        programNumber INTEGER , 
                        RPM INTEGER , 
                        TIME INTEGER )''')

        self.loadDataBaseIntoTreeView()
        cursor.close()
        conn.commit()
        conn.close()


    def loadDataBaseIntoTreeView(self):

        conn = sqlite3.connect("programs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT *, oid FROM program ORDER BY programNumber")
        fetch = cursor.fetchall()

        for data in fetch:

            self.programNumberList.append(data[0])

            bol = self.tree.exists(data[0])

            if (not bol):
                self.addNewProgram(data[0])
                self.tree.insert(data[0], index="end", values=(data[1], data[2]))

            else:
                self.tree.insert(data[0], index="end", values=(data[1], data[2]))

        self.uniqueElementsOfList()

        cursor.close()
        conn.commit()
        conn.close()


    def transmitData(self):
        return


    def export(self):

        conn = sqlite3.connect("programs.db")
        cursor = conn.cursor()
        cursor.execute("SELECT *, oid FROM program ORDER BY programNumber")
        fetch = cursor.fetchall()

        if len(fetch) < 1:

            tkMessageBox.showerror("No Data" , "No data available to export!")
            return False

        file = filedialog.asksaveasfilename( initialdir = os.getcwd() , title = "Save CSV" ,
                                             filetypes = (("CSV File" , "*.csv") , ("All Files" , "*.*")))

        with open( file , mode = "w") as myfile:

            exportWriter = csv.writer( myfile , delimiter = ",")

            for row in fetch:

                exportWriter.writerow(row)
        tkMessageBox.showinfo("Data Exported" , "Your data has been exported to " + os.path.basename(file) + " successfulyy")


    def mode(self):

        scaleColor = ["grey28", "alice blue"]
        theme = ["equilux" , "adapta"]

        i = 0

        if (self.count % 2 == 0):

            i = 0

        else:

            i = 1

        self.set_theme(theme[i])
        self.rpmScale.config(bg=scaleColor[i])
        self.timeScale.config(bg=scaleColor[i])
        self.theme = theme[0]

        self.count += 1


    def initiateProgram(self):

        self.threadAlive = True


        totalTime = 0
        interval = 0

        notebookSelectedTabNumber = self.getNotebookSelectedTabNumber()
        MOTORA = self.raspberry.dicSetup["MOTOR" + str(notebookSelectedTabNumber) + "A"]
        MOTORB = self.raspberry.dicSetup["MOTOR" + str(notebookSelectedTabNumber) + "B"]
        self.raspberry.motorClockwise( MOTORA , MOTORB)

        conn = sqlite3.connect("programs.db")
        cursor = conn.cursor()
        programNumber = self.getProgramNumber()
        cursor.execute(" SELECT *, oid FROM program WHERE programNumber = ?" , (programNumber,))
        fetch = cursor.fetchall()

        for row in fetch:

            totalTime += row[2]

        interval =  int ((totalTime / 100)  * self.timeMode * 1000) # the * 1000 is necessary as the prograssbar measures everythin in miliseconds and not seconds
        self.progressBar.start([interval])

        for row in fetch:

            self.raspberry.changePWM(notebookSelectedTabNumber , row[1])
            time.sleep(row[2] * self.timeMode)

        self.progressBar.stop()

        self.raspberry.motorStop(MOTORA , MOTORB) #ll

        tkMessageBox.showinfo("Program finished",  "The program is finished!") ### fuehrt zu problemen wen das Gui vom user derminated wird, bevor das Program fertig ist


        self.thread = threading.Thread( target = startProgram)
        self.thread.start()


        self.threadAlive = False

    def getProgramNumber(self):

        stringchosenProgramCombobox = self.choseProgramCombobox.get()
        listchosenProgramCombobox = [ x for x in stringchosenProgramCombobox ]
        numchosenProgramCombobox = int(listchosenProgramCombobox[-1])

        return numchosenProgramCombobox


    def getNotebookSelectedTabNumber(self):

        notebookSelectedTabNumber = self.notebook.index(self.notebook.select())
        return notebookSelectedTabNumber


    def uniqueElementsOfList(self):

        self.comboBoxList = []

        for el in self.programNumberList:

            if el not in self.uniqueProgramNumberList:

                self.uniqueProgramNumberList.append(el)

        for el in self.uniqueProgramNumberList:

            self.comboBoxList.append("Program" + str(el))

        self.choseProgramCombobox["values"] = self.comboBoxList

        if ( not len(self.comboBoxList) == 0):

            self.choseProgramCombobox.current([0])

    def terminateProgram(self):

        MOTORA = self.raspberry.dicSetup["MOTOR" + str(notebookSelectedTabNumber) + "A"]
        MOTORB = self.raspberry.dicSetup["MOTOR" + str(notebookSelectedTabNumber) + "B"]
        self.raspberry.motorStop(MOTORA, MOTORB)

        self.threadAlive = False



    def disable_event( self):

        if ( self.threadAlive):

            tkMessageBox.showinfo("Warning!",
                                  "You can not close the gui before:" + "\n" + "\n" +
                                  "1) The program is finished " + "\n" + "\n" +
                                  "2) The program is terminated via the button 'Terminate'")

        else:

            self.destroy()

    def handleClickProgramEntry(self , event):

        self.programEntry.delete(0 , tk.END)
        global string
        string = ""
        topLevel = GuiNumberField()
        topLevel.wait_window()
        self.programEntry.insert( 0  , string)

    def handleClickRpmEntry(self , event):

        self.rpmEntry.delete(0 , tk.END)
        global string
        string = ""
        topLevel = GuiNumberField()
        topLevel.wait_window()
        self.rpmEntry.insert( 0  , string)

    def handleClickTimeEntry(self , event):

        self.timeEntry.delete(0 , tk.END)
        global string
        string = ""
        topLevel = GuiNumberField()
        topLevel.wait_window()
        self.timeEntry.insert( 0  , string)

    def easterEgg(self):

        global my_img
        top = tk.Toplevel()
        top.title("never ever gonna give you up ...")
        top.geometry( "250x250" )
        my_img = ImageTk.PhotoImage(Image.open( "/Users/jonasmarschick/Desktop/easterEgg.png"))
        tk.Label(top, image=my_img).pack()




class GuiNumberField(tk.Toplevel):  # ThemedTk

    def __init__(self):

       # ThemedTk.__init__(self)
        tk.Toplevel.__init__(self)

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

        rows = [ 2 , 3 , 4 , 5 ]
        columns = [ 0 , 1 , 2]
        number = 1

        for r in rows:
            for c in columns:

                if r == 5:

                    addButton = ttk.Button(self.frame , text = "0" , command = lambda : self.submitData("0"))
                    addButton.grid( row = 5 , column = 0 , sticky = "NESW")

                else:

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

        self.Entry.delete(0 , tk.END)
        global  string

        if len(string) < 4:
            string += text

        else:
            pass

        self.Entry.insert(0, string)

    def deleteEntry(self):

        global string
        string = ""
        self.Entry.delete(0 , "end")

    def enterEntry(self):

        global string

        if string != "":

            self.Entry.delete(0)
            self.destroy()

        else:

            pass

    def getString(self):

        global string
        return string


if __name__ == "__main__":

    execute = Gui()
    execute.mainloop()
