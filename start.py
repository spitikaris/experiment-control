#!/usr/bin/python
import os
import time
import serial
from PIL import Image
from PIL.ExifTags import TAGS
import RPi.GPIO as GPIO

#Raspberry Motorshield
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
import atexit

#Initializing Camera Motor
mh=Adafruit_MotorHAT(addr=0x60)
def turnOffMotors():
    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
    mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

class bcolors:
    HEADER = '\033[95m'
    SEND = '\033[94m'
    RECEIVE = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def writeLists (D):
    outfile = open(D+"list.txt",'w')
    for f in os.listdir(D):
        if f.endswith(".jpg"):

            img = Image.open(D+f)
            exif_data = {}
            info = img._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag,tag)
                exif_data[decoded] = value

            nominator = exif_data["ExposureTime"][1]/exif_data["ExposureTime"][0]

            outfile.write(f  +"\t" +str(nominator)+"\n")
    outfile.close()

def menu ():
	print "--------------------------------------------------------------"
	print "Stress-Birefringence Experimental Control Ver 0.2"
	print "MAIN MENU"
	print "--------------------------------------------------------------"
	print "(1) Direct Control"
	print "(2) Start Compression experiment"
	print "(3) Start Decompression experiment"
	print "(4) Start HR image capture"
	print "(0) Exit\n"

	return input("Your selection: ")

def connect (item):
	print(bcolors.HEADER + "Connecting to Arduino..."+bcolors.ENDC)
        print(bcolors.HEADER + "Sending "+ item + bcolors.ENDC)
	response = ''
	while 'Hello Pi' not in response:
		ser.write(item)
		response = ser.readline()
		print bcolors.RECEIVE + "Arduino: " + response + bcolors.ENDC
	print("Connection established.")


def send (signal, check):
	response = ''
	while check not in response:
		print bcolors.SEND + "Sending signal " + signal + "..." + bcolors.ENDC
		ser.write(signal)
		response = ser.readline()
		print bcolors.RECEIVE + str(response) + bcolors.ENDC
        print bcolors.RECEIVE + "Signal received." + bcolors.ENDC

Servo=[]
def turn_holder (aim):
    print(bcolors.HEADER + "Turning camera holder" + bcolors.ENDC)
    if aim=='uncover':
        send('4','turning_holder..done')
    elif aim=='right-handed':
        send('5','turning_holder..done')
    elif aim=='left-handed':
	send('51', 'turning_holder..done')



def waitForArduino (word):
	response = ''
	while word not in response:
		ser.write('0')
		response = ser.readline()
def init (stage):
	print(bcolors.HEADER + "Initializing Arduino...")
        if stage:
	    print("Moving camera holder to start position")
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.setup(40,GPIO.OUT)
        Servo=GPIO.PWM(40,50)
	#send('4','turning_holder..done' + bcolors.ENDC)
        Servo.start(7)
        time.sleep(1)
        Servo.stop()
        Servo.start(10)
        for Counter in range(20):
            time.sleep(0.01);
        Servo.stop()
        print(bgcolors.HEADER + "Initializing x-y-stage" + bcolors.ENDC)



x_stepper = mh.getStepper(200,1)
x_stepper.setSpeed(200)
mode=0
user_input = 1
ser = serial.Serial('/dev/ttyACM0', 9600)
while (user_input!=0):
	user_input = menu()

	if user_input == 1:
		print("Starting direct control mode...")
		if (mode != 1):
			os.system("(cd /home/pi/Documents/Arduino/StepperControlIno/; ino upload)")
		mode = 1
		print("Direct control is active.")
		uin = raw_input("Enter filename  to take a photo or <q> to quit...",'s')
		if uin != 'q':
                        turn_holder('uncover')
			os.system("sispmctl -o 1")
			os.system("sispmctl -o 2")
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+uin+".jpg 2>/dev/null")
			time.sleep(5)
			os.system("sispmctl -f 1")
			os.system("sispmctl -f 2")
                        turn_holder('cover')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+uin+"RH.jpg' 2>/dev/null")
			turn_holder('left-handed')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+uin+"LH.jpg' 2>/dev/null")
	elif user_input == 2:
		if mode != 2:
			os.system("(cd /home/pi/Documents/Arduino/CompressionIno/; ino upload)")
                        ser = serial.Serial('/dev/ttyACM0', 9600)
                        time.sleep(3);
		mode = 2
		connect('7')
		print("Compression experiment...")
		expName = raw_input("Enter name of experiment: ")
		os.system("mkdir "+expName)
		steps = input ("Total amount of steps: ")
		stepsPerStep = input ("Steps per step: ")
		sidelength = input ("Container sidelength: ")
		sidelength = sidelength/100
		STEPSPERCM = 1000.
		position = 0
	        f = open(expName + '/cVolume.dd', 'w')
		ctr=0
		while position < steps:
			print "Current position: " + str(position)
			print("Taking photos...")
                        turn_holder('uncover')
			os.system("sispmctl -o 1")
			os.system("sispmctl -o 2")
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=23 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			ctr = ctr+1
			time.sleep(2)
			os.system("sispmctl -f 1")
			os.system("sispmctl -f 2")
                        turn_holder('cover')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=19 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			ctr=ctr+1
			time.sleep(2)
			print("Going to new position...")
			for i in range(1, stepsPerStep+1, 1):
				send('6', 'step..done');
				position = position + 1
				time.sleep(1)
				sidelength = sidelength - 1./(STEPSPERCM*100)
			f.write(str(sidelength*sidelength)+'\n')
			send('5', 'agitation..done')
       	 	f.close()
		raw_input("Press RETURN to move the walls to the initial position...")
		send('7', 'returned');
		send('4','turning_holder..done')
		send('0', 'stopping decompression')
		os.system("sudo sispmctl -f 3")
		print ("Source light turned off")
		os.system("sudo sispmctl -f 4")
		print ("Motor and Stepper power turned off")
		print("Enter password on mp-tresca to copy images in home directory")
		os.system("scp -r "+expName+ " spitikaris@mp-tresca:FNA/data/")
	elif user_input == 3:
		if mode != 3:
			os.system("(cd /home/pi/Documents/Arduino/DecompressionIno/; ino upload)")
                        ser = serial.Serial('/dev/ttyACM0', 9600)
                        time.sleep(3);
		mode = 3
		connect('3')
                send('3','Procedure_started')
		print("Decompression experiment...")
		expName = raw_input("Enter name of experiment: ")
		os.system("mkdir "+expName)
		steps = input ("Total amount of steps: ")
		stepsPerStep = input ("Steps per step: ")
		sidelength = input ("Container sidelength: ")
		sidelength = sidelength/100
		STEPSPERCM = 1000.
		position = 0
	        f = open(expName + '/cVolume.dd', 'w')
		ctr=0
		while position < steps:
			print "Current position: " + str(position)
			print("Taking photos...")
                        turn_holder('uncover')
			os.system("sispmctl -o 1")
			os.system("sispmctl -o 2")
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			ctr = ctr+1
			time.sleep(5)
			os.system("sispmctl -f 1")
			os.system("sispmctl -f 2")
                        turn_holder('cover')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			turn_holder('left-handed')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+"LH.jpg' 2>/dev/null")
			ctr=ctr+1
			time.sleep(2)
			print("Going to new position...")
			for i in range(1, stepsPerStep+1, 1):
				send('6', 'step..done');
				position = position + 1
				time.sleep(1)
				sidelength = sidelength + 1./(STEPSPERCM*100)
			f.write(str(sidelength*sidelength)+'\n')
			send('8', 'agitation..done')
       	 	f.close()
		raw_input("Press RETURN to move the walls to the initial position...")
		send('7', 'returned');
		send('4','turning_holder..done')
		send('0', 'stopping compression')
		os.system("sudo sispmctl -f 3")
		print ("Source light turned off")
		os.system("sudo sispmctl -f 4")
		print ("Motor and Stepper power turned off")
		print("Enter password on mp-tresca to copy images in home directory")
		os.system("scp -r "+expName+ " spitikaris@mp-tresca:FNA/data/")
	elif user_input == 4:
                X_TOT = 1140
                Y_TOT = 1140
                x_steps = 5
		ctr=0
		print "HDRI capture mode"
		if mode != 4:
			os.system("(cd /home/pi/Documents/Arduino/hdriIno/; ino upload)")
                        print "Establishing connection to Arduino..."
                        ser = serial.Serial('/dev/ttyACM0', 9600)
                        time.sleep(3);
		connect('8')
                turn_holder('uncover')
		print "Enter shutter time choices. Press 'c' to continue: "
		enteredNo = raw_input("Next number (c to exit): ")
		shutterTimes = []
		while enteredNo != "c":
			shutterTimes.append(enteredNo)
			enteredNo = raw_input("Next number (c to exit): ")
                print("shutter time choices are ")
                print ', '.join(shutterTimes)
                x_steps = input("Number of steps in x-direction: ")
		os.system("mkdir hdr_src")
                button = "0"
                print bcolors.WARNING + "Prepare (10 sec)..." + bcolors.ENDC
                time.sleep(10);
                ctr = 0 
		while button != "q":
                    for x in range(1,x_steps):
			ctr=ctr+1
			os.system("mkdir hdr_src/"+str(ctr))
			#os.system("cp list.txt hdr_src/"+str(ctr)+"/")
			os.system("sudo sispmctl -o 1")
			os.system("sudo sispmctl -o 2")
			os.system("sudo sispmctl -f 3")
                        time.sleep(1)
			for i in shutterTimes:
                            os.system("gphoto2 --set-config-index \
                                    /main/capturesettings/shutterspeed="+i+" \
                                    --capture-image-and-download \
                                    --filename='hdr_src/"+str(ctr)+"/"+i+".jpg' \
                                    2>/dev/null")
                        writeLists("hdr_src/"+str(ctr)+"/")
                        ctr=ctr+1
                        os.system("mkdir hdr_src/"+str(ctr))
                        #os.system("cp list.txt hdr_src/"+str(ctr)+"/")
                        turn_holder('cover')
                        os.system("sudo sispmctl -f 1")
                        os.system("sudo sispmctl -f 2")
                        os.system("sudo sispmctl -o 3")
                        time.sleep(3)
                        for i in shutterTimes:
                                os.system("gphoto2 --set-config-index \
                                        /main/capturesettings/shutterspeed="+i+" \
                                        --capture-image-and-download \
                                        --filename='hdr_src/"+str(ctr)+"/"+i+".jpg' \
                                        2>/dev/null")
                        writeLists("hdr_src/"+str(ctr)+"/")
                        turn_holder('uncover')
                        x_stepper.step(int(X_TOT/x_steps), Adafruit_MotorHAT.BACKWARD,
                                Adafruit_MotorHAT.DOUBLE);
                        time.sleep(1)
                    x_stepper.step(int(X_TOT-X_TOT/x_steps), Adafruit_MotorHAT.FORWARD, \
                            Adafruit_MotorHAT.DOUBLE);
                    print "Waiting for confirmation..."
                    send('1',"button_pressed..done")
                    #button = raw_input("Press any button to continue but 'q' for leaving");

	elif user_input == 5:
		if mode != 5:
			os.system("(cd /home/pi/Documents/Arduino/Ino/; ino upload)")
		mode = 5
		print "Uploading single wall control"
