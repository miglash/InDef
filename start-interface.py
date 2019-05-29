# implement the default mpl key bindings
import matplotlib
import matplotlib.animation as animation
matplotlib.use("TkAgg")

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
#from matplotlib.backends import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk

#Random definitions of text
LARGE_FONT=("Verdana",24)
NORMAL_FONT=("Verdana",12)

formfig = Figure(figsize=(5,5), dpi = 100)
a = formfig.add_subplot(111) #1x1 plot with chart 1

#Interface is a tk.Tk (inheritence relationship) 
#This is where all the frames are getting pushed up
class Interface(tk.Tk):

      #Initializes the class -- a method/not a function
      #Self is implied (if you don't use it, still passed)
      def __init__(self, *args, **kwargs):

          #Initializes a parent
          tk.Tk.__init__(self, *args, **kwargs)
          #tk.Tk.iconbitmap(self,"path17.png")
          tk.Tk.wm_title(self, "InDef - An in-depth Defect analysis tool")

          #Is the first Frame
          container = tk.Frame(self)
          container.pack(side="top", fill="both", expand=True)
          container.grid_rowconfigure(0, weight=1)
          container.grid_columnconfigure(0, weight=1)

          self.frames = {}

          for aframe in (StartPage, GenerateData, ParseData, ManualData, LinkFolders, GraphData):
              thisframe = aframe(container,self)
              self.frames[aframe] = thisframe

              thisframe.grid(row = 0, column = 0, sticky="nsew")

          self.show_frame(StartPage)

      def show_frame(self, page):

          frame = self.frames[page]
          frame.tkraise()


##------------------------------ Pages ------------------------------------------------------------

#A given page only inherits from a tk.Frame
#This is a Frame that lets you chose between analysis OR
#Generation of input data
class StartPage(tk.Frame):

      def __init__(self,parent,controler):
          tk.Frame.__init__(self,parent)

          self.grid_rowconfigure(2, weight=1)
          self.grid_rowconfigure(4, weight=1)
          self.grid_columnconfigure(0, weight=1)
          self.grid_columnconfigure(1, weight=1)
          self.grid_columnconfigure(2, weight=1)
          self.grid_columnconfigure(3, weight=1)

          #Titeling the start page
          Titlelabel = tk.Label(self, text="Welcome to InDef!", font=LARGE_FONT)
          Titlelabel.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky='ew')
          Explabel = tk.Label(self, text="A simple tool for in-depth analysis of supercell defect formation energy calculations", font=NORMAL_FONT)
          Explabel.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky='ew')

          imgFold = tk.PhotoImage(file="images/folder.png")

          #lambda: makes the function not run immedietely on compilation
          # create the image button, image is above (top) the optional text
          hostbutton = tk.Button(self, compound=tk.TOP, width=165, height=165, image=imgFold,
          text="I only have the host structure", bg='green', command=lambda: controler.show_frame(GenerateData))
          hostbutton.grid(row = 3, column = 1, sticky='ns')

          databutton = tk.Button(self, compound=tk.TOP, width=165, height=165, image=imgFold,
          text="I already have defect data", bg='green', command=lambda: controler.show_frame(ParseData))
          databutton.grid(row = 3, column = 2, sticky='ns')

          # save the button images from garbage collection 
          hostbutton.image = imgFold
          databutton.image = imgFold


#Page that will eventually allow you to upload your host structure
#In order to generate defect data
#To be implemented
class GenerateData(tk.Frame):

      def __init__(self,parent,controler):
          tk.Frame.__init__(self,parent)

          self.grid_rowconfigure(0, weight=1)
#          self.grid_rowconfigure(1, weight=1)
          self.grid_columnconfigure(0, weight=1)
          warnlabel = tk.Label(self, text="Defect generation currently UNAVAILABLE", font=LARGE_FONT)
          warnlabel.grid(row = 0, column = 0,pady=10,padx=10)

          returnButton = tk.Button(self, text = "Return", command=lambda: controler.show_frame(StartPage))
          returnButton.grid(row = 1, column = 1, pady=10,padx=10)


#Page that allows you to chose between automated data parsing
#Or manual data input
class ParseData(tk.Frame):

      def __init__(self,parent,controler):
          tk.Frame.__init__(self,parent)

          self.grid_rowconfigure(0, weight=1)
          self.grid_rowconfigure(1, weight=1)
          self.grid_rowconfigure(2, weight=1)
          self.grid_rowconfigure(3, weight=1)
          self.grid_columnconfigure(0, weight=1)
          self.grid_columnconfigure(1, weight=1)

          descrlabel = tk.Label(self, text="The anticipated folder hierarchy for the code to automatically parse your calculations:", font=NORMAL_FONT)
          descrlabel.grid(row = 0, column = 0, columnspan=2, pady=10,padx=10)

          imghierch = tk.PhotoImage(file="images/hierarchy.png")
          imglabel = tk.Label(self,image=imghierch)
          imglabel.image = imghierch
          imglabel.grid(row = 1, column = 0, columnspan=2, pady=20,padx=0)

          descrlabel2 = tk.Label(self, text="Folders shown in green are mandatory. If the above hierarchy is obayed, simply continue with parsing.", font=NORMAL_FONT)
          descrlabel2.grid(row = 2, column = 0, columnspan=2, pady=10,padx=10)

          #Parse: calls the inner workings of the code to be implemented
          parsebutton = tk.Button(self, width=18, height=2, text="Continue with parsing", command=parse_calculations)
          parsebutton.grid(row = 3, column = 0, pady=10,padx=10)

          addbutton = tk.Button(self, width=18, height=2, text="Add data manually", command=lambda: controler.show_frame(ManualData))
          addbutton.grid(row = 3, column = 1, pady=10,padx=10)

          returnButton = tk.Button(self, text = "Return", command=lambda: controler.show_frame(StartPage))
          returnButton.grid(row = 4, column = 2, pady=10,padx=10)

##Page that allows you to input your defect calculation data manually
##Or by selecting the folders from which to parse
class ManualData(tk.Frame):


      def __init__(self,parent,controler):

          def process_input():
           
              #Validate manual input
              valid = False

              print("First Name: %s\nLast Name: %s" % (1.0, bulkEnentry.get()) )

              if valid:
                 controler.show_frame(GraphData)

          def parse_folders():
              
              #Validate folder input
              valid = False

              bf=bulkfld.get()
              rf=reffld.get()
              df=deffld.get()

              if (len(bf) == 0 or len(df) == 0):
                 bulkfld.insert(10,'Field Required')
                 deffld.insert(10,'Field Required')
              if valid:
                 controler.show_frame(GraphData)

          tk.Frame.__init__(self,parent)

          self.grid_columnconfigure(1, weight=1)
          explabel = tk.Label(self, text="Please select the folders from which to parse the calculations:", font=NORMAL_FONT)
          explabel.grid(row=0,column=0, pady=10,padx=10)

          bulklbl = tk.Label(self, text="Bulk directory:", width=20, font=NORMAL_FONT)
          bulklbl.grid(row=1, column=0, padx=5, pady=5)
          bulkfld = tk.Entry(self)
          bulkfld.grid(row=1,column=1, padx=5, sticky='we')

          reflbl = tk.Label(self, text="Reference directory:", width=20, font=NORMAL_FONT)
          reflbl.grid(row=2, column=0, padx=5, pady=5)
          reffld = tk.Entry(self)
          reffld.grid(row=2,column=1, padx=5, sticky='we')

          deflbl = tk.Label(self, text="Defects directory:", width=20, font=NORMAL_FONT)
          deflbl.grid(row=3, column=0, padx=5, pady=5)
          deffld = tk.Entry(self)
          deffld.grid(row=3,column=1, padx=5, sticky='we')

          button1 = tk.Button(self, width=15, height=3, text="Parse folders", command=parse_folders)
          button1.grid(row=4,column=3, pady=10,padx=10)

          explabel = tk.Label(self, text="OR input each required data field manually (units = eV):", font=NORMAL_FONT)
          explabel.grid(row=5,column=0, pady=10,padx=10)
 
          bulkEnlbl = tk.Label(self, text="Bulk Energy:", width=20, font=NORMAL_FONT)
          bulkEnlbl.grid(row=6, column=0, padx=5, pady=5)
          bulkEnentry = tk.Entry(self)
          bulkEnentry.grid(row=6,column=1, padx=5, sticky='we')

          bulkVBMlbl = tk.Label(self, text="VBM Energy (bulk):", width=20, font=NORMAL_FONT)
          bulkVBMlbl.grid(row=7, column=0, padx=5, pady=5)
          bulkVBMentry = tk.Entry(self)
          bulkVBMentry.grid(row=7,column=1, padx=5, sticky='we')

          defEnlbl = tk.Label(self, text="Defect cell Energy:", width=20, font=NORMAL_FONT)
          defEnlbl.grid(row=8, column=0, padx=5, pady=5)
          defEnentry = tk.Entry(self)
          defEnentry.grid(row=8,column=1, padx=5, sticky='we')

          Ecorlbl = tk.Label(self, text="Corrections:", width=20, font=NORMAL_FONT)
          Ecorlbl.grid(row=9, column=0, padx=5, pady=5)
          Ecorentry = tk.Entry(self)
          Ecorentry.grid(row=9,column=1, padx=5, sticky='we')

          button1 = tk.Button(self, width=15, height=3, text="Process Data", command=process_input)
          button1.grid(row=10,column=3, pady=10,padx=10)

     

class LinkFolders(tk.Frame):

      def __init__(self,parent,controler):
          tk.Frame.__init__(self,parent)

          self.grid_rowconfigure(0, weight=1)
#          self.grid_rowconfigure(1, weight=1)
          self.grid_columnconfigure(0, weight=1)
          warnlabel = tk.Label(self, text="This feature is currently UNAVAILABLE", font=LARGE_FONT)
          warnlabel.grid(row = 0, column = 0,pady=10,padx=10)

          returnButton = tk.Button(self, text = "Return", command=lambda: controler.show_frame(StartPage))
          returnButton.grid(row = 1, column = 1, pady=10,padx=10)


class GraphData(tk.Frame):
      
      def __init__(self,parent,controler):
          tk.Frame.__init__(self,parent)

          label = tk.Label(self, text="Welcome to InDef!", font=LARGE_FONT)
          label.pack(pady=10,padx=10)
          
          label = tk.Label(self, text="A simple tool for in-depth analysis of supercell defect formation energy calculations", font=NORMAL_FONT)
          label.pack(pady=10,padx=10)

          label= tk.Label(self, text="Formation Energies", font=LARGE_FONT)
          label.pack(pady=10,padx=10)

          label= tk.Label(self, text="EFx = Del. E - \sum ni mui + qu eps_F + Ecor", font=LARGE_FONT)
          label.pack(pady=10,padx=10)

          label= tk.Label(self, text="Formation Enthalpies", font=LARGE_FONT)
          label.pack(pady=10,padx=10)

          label= tk.Label(self, text="HFx(Vf) = EFx (Vf) + P Vf", font=LARGE_FONT)
          label.pack(pady=10,padx=10)

          canvas = FigureCanvasTkAgg(formfig, self)
          canvas.show()
          canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

          toolbar = NavigationToolbar2TkAgg(canvas, self)
          toolbar.update()

          canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

def animate(i):
    pull_data = open("sampledata.txt",'r').read()
    dataList = pull_data.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
           x, y=eachLine.split(',')
           xList.append(int(x))
           yList.append(int(y))

    a.clear()
    a.plot(xList,yList)

def parse_calculations():
    print('Ha :P')

#---------------------------------------- Initializing the Interface ------------------------------

app = Interface()
app.geometry("1600x1000")
ani = animation.FuncAnimation(formfig, animate, interval = 1000)
app.mainloop()




#class Window(tk.Frame):
#
#     def __init__(self, master = None):
#         tk.Frame.__init__(self, master)
#         
#         self.master=master
#
#         self.init_window()
#
#     def init_window(self):
# 
#         self.master.title("InDef")
#         self.pack(fill=BOTH, expand=1)
#
#         #quitButton = Button(self, text = "Love Me", command=self.client_love)
#         #quitButton.place(x=0,y=0)
#
#         menu = tk.Menu(self.master)
#         self.master.config(menu=menu)
#
#         file = tk.Menu(menu)
#
#         file.add_command(label='Add More', command=self.client_add_data)
#         file.add_command(label='Save Plot', command=self.client_save_plot)
#         file.add_command(label='Save Plot Data', command=self.client_save_data)
#         file.add_command(label='Exit', command=self.client_exit)
# 
#         edit = tk.Menu(menu)
#
#         edit.add_command(label='Undo', command=self.client_undo)
#
#         menu.add_cascade(label='File', menu=file)
#         menu.add_cascade(label='Edit', menu=edit)
#
#     def client_exit(self):
#
#         exit()
#
#     def client_add_data(self):
#
#         exit()
#
#     def client_save_plot(self):
#
#         exit()
#
#     def client_undo(self):
#
#         exit()
#
#     def client_save_data(self):
#
#         exit()
