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
ser = serial.Serial('/dev/ttyACM3', 57600)

def init():
    global ser
    ser = serial.Serial('/dev/ttyACM0', 57600)
def initWithACMPort(acmport):
    path = '/dev/ttyACM'+str(acmport)
    global ser
    ser = serial.Serial(path, 57600)

def send(signal, check, doneResponse):
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

def position():
    buf = "$position%&\n"
    send(buf, "Present position", "--")

def release():
    buf = "$release%&\n"
    send(buf, "Releasing", "Motors turned")

def moveto(x,y):
    buf = "$move_to%%%d,%d&\n" % (x,y)
    send(buf,"Moving", "finished")

def moveabout(x,y):
    buf = "$shift_about%%%d,%d&\n" % (x,y)
    send(buf,"Moving", "finished")

def home():
    buf = "$go_home%&\n"
    send(buf, "home position", "home.")

def homeNoWait():
    ser.write("$go_home%&\n")
