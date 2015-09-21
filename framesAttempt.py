__author__ = 'Nathan'
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import os
import re

TITLE_FONT = ("Helvetica", 18, "bold")

class samApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_title("Black section finder")
        self.iconbitmap(r'BMF.ico')
        #self.configure(background='green')
        self.top =tk.Frame(self)#,back='red')
        self.bottom=tk.Frame(self)#,back='blue')
        self.top.grid(row=0)
        self.bottom.grid(row=1)
        self.geometry("400x250")
        self.resizable(width=False, height=False)

        self.frames={}
        for F in (Single,Multiple,Usage):
            frame = F(self.bottom,self)
            #frame.config(background='blue')
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky='nsew')
        #print(self.frames.keys())

        #top_spacer=tk.Label(self,text="space")#,expand=1)
        #top_spacer.grid(row=0)
        usage_bt = tk.Button(self.top,text="Usage",command=lambda: self.set_frame(Usage,usage_bt,buttons))
        usage_bt.grid(row=0,sticky='nw',padx=5,pady=5)
        single_bt = tk.Button(self.top,text="PSingle mode", command=lambda: self.set_frame(Single,single_bt,buttons))
        #.config(relief="sunken")
        single_bt.grid(row=0,column=1,sticky='w',pady=5,padx=5)
        multiple_bt = tk.Button(self.top,text="Multiple mode",command=lambda: self.set_frame(Multiple,multiple_bt,buttons))
        multiple_bt.grid(row=0,column=2,sticky='ne',pady=5,padx=5)
        buttons={single_bt,multiple_bt,usage_bt}

        self.set_frame(Usage,None,None)
        usage_bt.config(relief="sunken")
        #self.set_frame(Multiple,None,None)


    def set_frame(self,c,bt,buttons):
        if bt:
            bt.config(relief="sunken")
            for other_bt in buttons:
                if not other_bt is bt:
                    other_bt.config(relief="raised")
        frame=self.frames[c]
        frame.tkraise()

class Usage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        info_string="This is an application to process .edl files. There are two modes. \n\nSINGLE MODE: " \
                    "One .edl file is processed, and the output is written to a file whose name is provided" \
                    " by the user. The file will be located in the same folder as the .edl file. \n\nMULTIPLE MODE: " \
                    " An entire folder is specified by the user. All .edl files in that folder will be" \
                    " processed, and .txt files with the same names will be produced as output. The output folder" \
                    " be placed in the user-specific folder, and will be named \"CONVERTED\"."
        info=tk.Label(self,text=info_string,wraplength=350,anchor='w',justify='left',font=('TkDefaultFont',10))
        info.pack(padx=5)

class Single(tk.Frame):
    def __init__(self,parent,controller):

        self.input_file=""
        self.short_in_file_name=tk.StringVar()
        self.short_in_file_name.set("None")

        self.input_file_dir=""

        tk.Frame.__init__(self,parent)

        #label = tk.Label(self,text="Process a single file")
        #label.grid()

        info = tk.Label(self,text="The output file will be created in the same folder as the input file.\n"
                                  "Please give the output file an appropriate extension (probably .txt)",fg="blue",relief="groove",width=55,height=4,justify="left")
        info.grid(row=2,columnspan=2,padx=5,pady=5)

        get_in_file_button=tk.Button(self,text="Choose file",command = lambda: self.choose_input_file())
        get_in_file_button.grid(row=3, column=1, pady=5, padx=5)

        in_label=tk.Label(self,text="Input file:")
        in_label.grid(row=4,sticky='e',pady=5,padx=5)

        in_file=tk.Label(self,textvariable = self.short_in_file_name,width=40,relief = "groove")
        in_file.grid(row=4,column=1,pady=5,padx=5)
        out_label=tk.Label(self,text="Output file:")
        out_label.grid(row=5,sticky='e',pady=5,padx=5)
        out_file=tk.Entry(self,width=47)
        out_file.grid(row=5,column=1,pady=5,padx=5)

        go=tk.Button(self,text="Process",command=lambda: processSingle(self.input_file,self.input_file_dir+'/'+out_file.get()))
        go.grid(column=1,pady=5,padx=5)

    def choose_input_file(self):
        self.input_file=askopenfilename()

        if not self.input_file=="":
            self.short_in_file_name.set(self.input_file)
            self.input_file_dir='/'.join(self.short_in_file_name.get().split('/')[:-1])

            while len(self.short_in_file_name.get())>50:
                #print(self.short_in_file_name.get())
                split_name=self.short_in_file_name.get().split('/')
                split_name.pop(0)
                self.short_in_file_name.set("..."+'/'.join(split_name))





class Multiple(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.input_dir=""
        self.short_in_dir_name=tk.StringVar()
        self.short_in_dir_name.set("None")

        self.input_dir=""

        tk.Frame.__init__(self,parent)
        #label = tk.Label(self,text="Process a single file")
        #label.grid()

        info = tk.Label(self,text="The output will be placed into a new folder in the same folder that the input "
                                  "files were found in. Only .edl files will be converted.\n"
                                  "The output from each file will be a .txt file with the same name."
                                  " For example, foo.edl will become foo.txt",fg="blue",relief="groove",width=55,height=4,wraplength=390,justify="left")
        info.grid(row=2,columnspan=2,pady=5,padx=5)
        get_in_file_button=tk.Button(self,text="Choose folder",command = lambda: self.choose_input_folder())
        get_in_file_button.grid(row = 3,column=1,pady=5,padx=5)

        in_label=tk.Label(self,text="Input folder:")
        in_label.grid(row=4,sticky='e',pady=5,padx=5)

        in_file=tk.Label(self,textvariable = self.short_in_dir_name,width=40,relief = "groove")
        in_file.grid(row=4,column=1,pady=5,padx=5)
        out_label=tk.Label(self)
        out_label.grid(row=5,sticky='we',pady=5,padx=5)
        #out_file=tk.Entry(self,width=25)
        #out_file.grid(row=5,column=1,pady=5,padx=5)

        go=tk.Button(self,text="Process",command=lambda: processFolder(self.input_dir))
        go.grid(column=1,pady=5,padx=5)

    def choose_input_folder(self):
        self.input_dir=askdirectory()

        if not self.input_dir=="":
            self.short_in_dir_name.set(self.input_dir)

            while len(self.short_in_dir_name.get())>50:
                print(self.short_in_dir_name.get())
                split_name=self.short_in_dir_name.get().split('/')
                split_name.pop(0)
                self.short_in_dir_name.set("..."+'/'.join(split_name))

def processFolder(dir_path):

    #print(dir_path)
    fileNames=[]
    midTimes=[]
    newpath = dir_path+'/CONVERTED'
    #print("n",newpath)



    for fileName in os.listdir(dir_path):
        if fileName[-4:]==".edl":
            fileNames.append(fileName)
            #print(dir_path+'/'+fileName)
            midTime=getBlackMidpoints(dir_path+'/'+fileName)
            midTimes.append(midTime)
    if len(fileNames)==0:
        messagebox.showerror("No .edl files found","The folder you chose does not contain any .edl files.\n"
                             "Please choose another folder and try again")
    else:
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        printProcessedFiles(dir_path,fileNames,midTimes)

def printProcessedFiles(dir_path,fileNames,midTimes):
    lens = [len(x) for x in fileNames]
    maxLen=max(lens)



    for i in range(len(fileNames)):
        justTheName=fileNames[i][:-4]
        #while len(fileNames[i])<maxLen:
            #fileNames[i]=fileNames[i]+' '
        #fileNames[i]=fileNames[i]+"-->"+justTheName+".txt"

        #print(fileNames[i], "converted to |  ", justTheName+".txt")
        printOutput(dir_path+'/CONVERTED/'+justTheName+".txt",midTimes[i])
    processed_files="\n".join(fileNames)

    messagebox.showinfo("Processed files","Conversion complete\nNames of processed files:\n"+
                        processed_files+"\nOutput stored in:\n"+ dir_path+"/CONVERTED")
    app.mainloop()

def processSingle(inputName,outputName):
    #print("out",outputName)
    validInput = False
    while not validInput:
        try:
            midTimes=getBlackMidpoints(inputName)
        except IOError:
            messagebox.showerror("No input file chosen","You did not choose a file to process.\nPlease click the \"Choose file\" button")
            break
        try:
            printOutput(outputName,midTimes)
            validInput = True
            messagebox.showinfo("Single file complete","Processing Complete\nOutput file:\n "+ outputName)
        except IOError:
            messagebox.showerror("No output file name given","No output file name given.\n Please enter an output file name.")

            break

    #print("Output file:\n ", os.getcwd()+"\\"+outputName)

def printOutput(outputFile,midTimes):
    try:
        outputFile=open(outputFile,'w')
    except IOError:
        raise
    for i in range(len(midTimes)):
        outLine = ' User ' + str(midTimes[i]) + ' V1  red\n'
        outputFile.write(outLine)
    outputFile.close()

def getBlackMidpoints(fileName):
    midTimes=[]
    inputFile=open(fileName,'r')
    outlist=[]
    lineNums=[]
    for line in inputFile:
        line=line.split()

        if len(line)==8:
            lineNum=line[0]
            if re.search(r".*_BLACK?",line[1]):

                if line[2]=='V':

                    startTime=line[6]
                    startTime=startTime.split(':')

                    midTime=computeMid(startTime)
                    midTimes.append(midTime)
                    lineNums.append(lineNum)
    #return [lineNums,midTimes]
    return midTimes

def computeMid(time):
    time = [int(x) for x in time]
    if time[3]<13:
        time[3]+=12
    else:
        time[2]+=1
        time[3]+=12
    for i in range(len(time)):
        time[i]=str(time[i])

        while len(time[i])<2:
            time[i]='0'+time[i]

    time=':'.join(time)

    return time

if __name__=="__main__":
    app=samApp()
    app.mainloop()


