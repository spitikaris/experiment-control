from VariableDefs import *
from control_functions import *
from camera_grid import homeNoWait
import time
import os

class bcolors:
    HEADER = '\033[95m'
    SEND = '\033[94m'
    RECEIVE = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def brightfield():
    os.system("sispmctl -o 1")
    os.system("sispmctl -o 2")
    os.system("sispmctl -f 3")
def darkfield():
    os.system("sispmctl -f 1")
    os.system("sispmctl -f 2")
    os.system("sispmctl -o 3")

def shear():
    homeNoWait()
    arduino = ArduinoCommunicator('/dev/ttyACM2')
    print("Shear experiment...")
    exp = experimentGrapper();
    exp.steplength = input ("Steplength: ")
    exp.no_steps = input ("Number of steps: ")
    tiling = input ("Photo-tiles per dimension: ")
    photogrid = photoframe(exp,tiling)
    position = 0
    cstep = 0
    saveSetup(exp);
    ctr=0
    while cstep < exp.no_steps:
        print "Current position: " + str(position)
        brightfield()
        arduino.turn_holder("open")
        take_photo2(photogrid, exp.photoPrefix()+"step"+str(cstep)+"_ti",0, arduino)
        darkfield()
        arduino.turn_holder("right-handed")
        take_photo2(photogrid, exp.photoPrefix()+"step"+str(cstep)+"_di",1, arduino,reverse=1)
        print("Going to new position...")
        arduino.shear(exp.steplength)
        position = position + exp.steplength
        cstep = cstep+1
        time.sleep(2)
        arduino.agitate(20)
        time.sleep(2)
    os.system("sispmctl -f 3")
    print ("Source light turned off")
    os.system("sudo -u piti_se cp -r "+exp.name+ "/* /mnt/cluster/gamma/piti_se/Data/fna/"+exp+"/")
    raw_input("Press RETURN to move the walls to the initial position...")
    os.system("entangle &")
    raw_input("Please take pictures of the final Volume first")
    os.system("sispmctl -o 1")
    os.system("sispmctl -f all")
    homeNoWait()
    print ("Motor and Stepper power turned off")

def decompression():
    homeNoWait()
    arduino = ArduinoCommunicator('/dev/ttyACM2')
    print("Decompression experiment...")
    exp = experimentGrapper();
    exp.steplength = input ("Steplength: ")
    exp.no_steps = input ("Number of steps: ")
    tiling = input ("Photo-tiles per dimension: ")
    photogrid = photoframe(exp,tiling)
    position = 0
    cstep = 0
    saveSetup(exp);
    ctr=0
    while cstep < exp.no_steps:
        print "Current position: " + str(position)
        brightfield()
        arduino.turn_holder("open")
        take_photo2(photogrid, exp.photoPrefix()+"step"+str(cstep)+"_ti",0, arduino)
        darkfield()
        arduino.turn_holder("right-handed")
        take_photo2(photogrid, exp.photoPrefix()+"step"+str(cstep)+"_di",1, arduino,reverse=1)
        print("Going to new position...")
        arduino.compress(-exp.steplength)
        position = position + exp.steplength
        cstep = cstep+1
        time.sleep(2)
        arduino.agitate(20)
        time.sleep(2)
    os.system("sispmctl -f 3")
    print ("Source light turned off")
    os.system("sudo -u piti_se cp -r "+exp.name+ "/* /mnt/cluster/gamma/piti_se/Data/fna/"+exp+"/")
    raw_input("Press RETURN to move the walls to the initial position...")
    os.system("entangle &")
    raw_input("Please take pictures of the final Volume first")
    os.system("sispmctl -o 1")
    os.system("sispmctl -f all")
    homeNoWait()
    print ("Motor and Stepper power turned off")
