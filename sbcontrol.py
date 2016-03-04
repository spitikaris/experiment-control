#!/usr/bin/python

from Tkinter import *
from control_functions import *
import os
import camera_grid_class as cg

class App():

  def InitCg(self):
    self.CameraStage=cg.CameraGrid(self.cgPort.get())
    self.CameraStage.homeNoWait()
    self.position()

  def CtrlInit(self):
    self.CtrlArduino=ArduinoCommunicator(self.ctrlPort.get(),'shear')

  def __init__(self):
    top = Tk()

    master = Frame(top)
    master.pack()
# Select correct Arduino
    arduinoSelectorFrame = Frame(master)
    arduinoSelectorFrame.pack(side=BOTTOM)
    Label(arduinoSelectorFrame, text='Camera Grid port: ', borderwidth=2).grid(row=0,column=0, sticky=W)
    Label(arduinoSelectorFrame, text='Control port: ', borderwidth=2).grid(row=1,column=0, sticky=W)
    availablePorts = os.popen("ls /dev/ttyA*").read().split('\n')
    self.cgPort = StringVar(arduinoSelectorFrame)
    self.ctrlPort = StringVar(arduinoSelectorFrame)
    e1 = apply(OptionMenu, (arduinoSelectorFrame, self.cgPort) + tuple(availablePorts)).grid(row=0,column=1)
    e2 = apply(OptionMenu, (arduinoSelectorFrame, self.ctrlPort) + tuple(availablePorts)).grid(row=1,column=1)
    cgInit = Button(arduinoSelectorFrame, text="Apply", command = self.InitCg).grid(row=0,column=2)
    Button(arduinoSelectorFrame, text="Apply", command = self.CtrlInit).grid(row=1,column=2)
# ---

# Move Camera Stage
    self.cameraMovementFrame = Frame(cgInit)
    self.cameraMovementFrame.pack()
    Label(self.cameraMovementFrame, text='Go to position :', borderwidth=2).grid(row=1, column=0, sticky=W)
    self.p1 = Entry(self.cameraMovementFrame, bd=2)    
    self.p1.grid(row=1,column=1)
    self.p2 = Entry(self.cameraMovementFrame, bd=2)
    self.p2.grid(row=1,column=2)
    goto=Button(self.cameraMovementFrame, text="Go",command = self.CameraGoToPos).grid(row=1,column=3)
    hB=Button(self.cameraMovementFrame, text="Find home position", command=self.InitCg).grid(row=2,column=0)
    stopB=Button(self.cameraMovementFrame, text="STOP",command = self.StopCamera).grid(row=2,column=1)
# Control experimental Setup
    ctrlFrame = Frame(cgInit)
    ctrlFrame.pack()
    Label(ctrlFrame, text="Light conditions: ", borderwidth=2).pack(side=LEFT)
    self.bf = IntVar()
    self.df = IntVar()
    Checkbutton(ctrlFrame, text="Brightfield", variable=self.bf, onvalue=1, offvalue=0, width=20,command=self.toggleBrightfield).pack(side=RIGHT)
    c2=Checkbutton(ctrlFrame, text="Darkfield", variable=self.df, onvalue=1, offvalue=0, width=20,command=self.toggleDarkfield).pack(side=RIGHT)
    ctrlHolder = Frame(cgInit)
    ctrlHolder.pack()
    l=Label(ctrlHolder, text="Turn holder to position: ", borderwidth=2).grid(row=0,column=1)
    self.holderPos=Entry(ctrlHolder, bd=2)
    self.holderPos.grid(row=0,column=2)
    Button(ctrlHolder, text="Go", command=self.turn_holder).grid(row=0,column=3)
    



# ---

  def turn_holder(self):
    self.CtrlArduino.turn_holder_to(int(self.holderPos.get()))
  def toggleDarkfield(self):
    if self.df.get()==1:
      os.system("sispmctl -o 3")
    else:
      os.system("sispmctl -f 3")
  def toggleBrightfield(self):
    if self.bf.get()==0:
      os.system("sispmctl -f 1")
      os.system("sispmctl -f 2")
    else:
      os.system("sispmctl -o 1")
      os.system("sispmctl -o 2")

  def StopCamera(self):
    tmpx=self.CameraStage.posx
    tmpy=self.CameraStage.posy
    self.CameraStage=cg.CameraGrid(self.cgPort.get())
    self.CameraStage.posx=tmpx
    self.CameraStage.posy=tmpy
    self.position()

  def CameraGoToPos(self):
    self.CameraStage.moveto(int(self.p1.get()), int(self.p2.get()))
    self.position()

  def position(self):
    Label(self.cameraMovementFrame, text="Current Position: %d,%d"%(self.CameraStage.posx,self.CameraStage.posy), borderwidth=2).grid(row=0,column=0)
# ---


program = App()
mainloop()
