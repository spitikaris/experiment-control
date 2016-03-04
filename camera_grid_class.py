import serial
import time


class bcolors:
    HEADER = '\033[95m'
    SEND = '\033[94m'
    RECEIVE = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class CameraGrid:
  posx = 0
  posy = 0
  def __init__(self,acmport):
    global ser
    ser = serial.Serial(str(acmport), 57600)

  def send(self, signal, check, doneResponse):
    response = ''
    i = 0
    while check not in response:
        i+=1
        if i>10:
            print (bcolors.FAIL + "Communication error" + bcolors.ENDC)
            return
        ser.write(signal)
        time.sleep(1)
        response = ser.readline()
    print(bcolors.RECEIVE + response)
    while doneResponse not in response:
        if "aborted" in response:
            print(response+bcolors.ENDC)
            return
        response = ser.readline()
    print(bcolors.RECEIVE + response)
    print(bcolors.ENDC)

  def position(self):
    buf = "$position%&\n"
    self.send(buf, "Present position", "--")

  def release(self):
    buf = "$release%&\n"
    self.send(buf, "Releasing", "Motors turned")

  def moveto(self,x,y):
    buf = "$move_to%%%d,%d&\n" % (x,y)
    self.send(buf,"Moving", "finished")
    self.posx=x
    self.posy=y

  def moveabout(self,x,y):
    buf = "$shift_about%%%d,%d&\n" % (x,y)
    self.send(buf,"Moving", "finished")
    self.posx+=x
    self.poxy+=y

  def home(self):
    buf = "$go_home%&\n"
    self.send(buf, "home position", "home.")
    self.posx=0
    self.posy=0

  def homeNoWait(self):
    ser.write("$go_home%&\n")
    self.posx=0
    self.posy=0
