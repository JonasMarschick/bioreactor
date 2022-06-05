from tkinter import*
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


class Gui(ThemedTk):

    def __init__(self):

        ThemedTk.__init__(self)

        self.choseProgram = ""
        self.count = 0
        self.theme = ""
        self.mydata = []
        self.comboBoxList = []
        self.programNumberList = []
        self.uniqueProgramNumberList = []
        self.threadAlive = False

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


        self.style = ttk.Style()
        self.title ("Spinfinity")
        self.geometry("900x900")
        #self.style = ttk.Style()
       # print(self.style.theme_names()) #Gives an option of the themes that are available
        #self.style.theme_use("alt")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand = 1  , fill = "both")
        #print(self.notebook.get_themes())

        self.frame1 = ttk.Frame(self.notebook)
       # self.frame1.config( bg = "azure")
        self.frame1.pack( fill = "both" , expand = True  )
        self.notebook.add(self.frame1 , text = "Bioreactor #1")
        self.frame2 = ttk.Frame(self.notebook )
        self.frame2.pack( fill = "both" , expand = True)
        self.notebook.add(self.frame2 , text = "Bioreactor #2")

        self.tree = ttk.Treeview( self.frame1 , columns = ("RPM" , "time") , selectmode = "extended")
        self.tree.heading("#0" , text = "Program Number")
        self.tree.heading("#1" , text = "RPM")
        self.tree.heading("#2" , text= "TIME")
        self.tree.grid(row = 2 , column = 0  , rowspan = 4 , columnspan = 6 , sticky = "NSEW" )
        #self.database()

        label1 = ttk.Label( self.frame1 , text = ("Program" + "\n" + "Number") + ":")
        label1.grid( row = 0 , column = 0 , sticky = "W")
        programEntry = ttk.Entry(self.frame1 , width = 5)
        programEntry.grid( row = 0 , column = 1 ,  sticky = "EW" )


        label2 = ttk.Label(self.frame1 , text = "RPM:")
        label2.grid( row = 0 , column = 2 )
        label3 = ttk.Label(self.frame1 , text = " Scale:")
        label3.grid( row = 1 , column = 2)
        rpmEntry = ttk.Entry(self.frame1 , width = 5)
        rpmEntry.grid( row = 0 , column = 3 ,  sticky = "EW")
        self.rpmScale = Scale( self.frame1 , from_ = 0 , to = 100 , orient = HORIZONTAL , resolution = 5)
        self.rpmScale.grid( row = 1 , column = 3 , sticky = "EW")

        label4 = ttk.Label(self.frame1, text = "TIME(H):")
        label4.grid ( row = 0 , column = 4)
        label4 = ttk.Label(self.frame1 , text = "Scale:")
        label4.grid( row = 1 , column = 4 )
        timeEntry = ttk.Entry(self.frame1 , width = 5)
        timeEntry.grid( row = 0  , column = 5 ,  sticky = "EW" )
        self.timeScale = Scale( self.frame1 , from_ = 0 , to = 100 , orient = HORIZONTAL , resolution = 1)
        self.timeScale.grid( row = 1 , column = 5 , sticky = "EW")

        addButton = ttk.Button(self.frame1 , text = "Add"  , width = 5 ,
                              command = lambda : self.submitData(rpmEntry , timeEntry , programEntry , self.rpmScale , self.timeScale))
        addButton.grid( row = 0  , column = 6 ,  sticky = "EW" , padx = 20)
        removeButton = ttk.Button( self.frame1 , text = "Remove", width = 5 ,
                               command = lambda : self.onRemove(self.tree.selection() , rpmEntry , timeEntry , programEntry , self.rpmScale , self.timeScale ))
        removeButton.grid( row = 1 , column = 6 , sticky ="EW" , padx = 20)

        self.actionButtonFrame = ttk.Frame(self.frame1  , width = 5 )
        self.actionButtonFrame.grid(row = 3 , column = 6 , sticky = "EW" , padx = 20)
        self.choseProgramCombobox = ttk.Combobox(self.actionButtonFrame, values=self.comboBoxList,  text="Choose a" + "\n" + "Program", width=5)
        self.choseProgramCombobox.grid( row=0 , column=0 , columnspan = 2 ,  sticky="WE" )
        # choseProgramCombobox.bind('<<ComboboxSelected>>' , self.someFunction)
        initiateProgramButton = ttk.Button ( self.actionButtonFrame , text = "Start" + "\n" + "Program" , command = lambda : threading.Thread( target = self.initiateProgram).start())
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

            if ( len(val1) == 0 or len(val2) == 0 or len(val0) == 0): # checks if the input of the entry buttons is valid

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

            programEntry.delete( 0 , "end")
            rpmEntry.delete( 0 , "end")
            timeEntry.delete( 0  , "end")

        elif ( not val3 == 0 and not val4 == 0):

            if (len(val0) == 0): # checks if the input of the entry buttons is valid

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

            programEntry.delete(0, "end")
            rpmEntry.delete(0, "end")
            timeEntry.delete(0, "end")

        else:

            tkMessageBox.showerror( title = "WARNING" , message = "Please make sure that the value you selected with the RPM or TIME scale matches the value entered in the RPM or Time entry box")


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

        if ( self.count % 2 == 0):

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

        #interval = (totalTime / 100)  * 60 * 60 * 1000 # time in hours
        interval =  int ((totalTime / 100)  * 1000) # time in seconds

        for row in fetch:
            
            print(row)
            self.progressBar.start([interval])
            self.raspberry.changePWM(notebookSelectedTabNumber , row[1])
            time.sleep(row[2])
           
        self.progressBar.stop()

        self.raspberry.motorStop(MOTORA , MOTORB) #ll

        tkMessageBox.showinfo("Program finished",  "The program is finished!") ### fuehrt zu problemen wen das Gui vom user derminated wird, bevor das Program fertig ist

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

if __name__ == "__main__":

    execute = Gui()
    execute.mainloop()
