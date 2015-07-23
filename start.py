#!/usr/bin/python
import os
import time
import serial


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
	print("Connecting to Arduino...")
	response = ''
	while 'Hello Pi' not in response:
		ser.write(item)
		response = ser.readline()
		print "Arduino: " + response
	print("Connection established.")


def send (signal, check):
	response = ''
	while check not in response:
		print "Sending signal " + signal + "..."
		ser.write(signal)
		response = ser.readline()
		print str(response)

def waitForArduino (word):
	response = ''
	while word not in response:
		ser.write('0')
		response = ser.readline()

def init ():
	print("Initializing Arduino...")
	print("Moving camera holder to start position")
	send('4','turning_holder..done')

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
	elif user_input == 2:
		connect('2')
		print("Compression experiment...")
		expName = raw_input("Enter name of experiment: ")
		os.system("mkdir "+expName)
		steps = input ("Total amount of steps: ")
		stepsPerStep = input ("Steps per step: ")
		sidelength = input ("Container sidelength: ")
		sidelength = sidelength/100
		STEPSPERCM = 1000.
		init()
		position = 0
	        f = open(expName + '/cVolume.dd', 'w')
		ctr=0
		while position < steps:
			print "Current position: " + str(position)
			print("Taking photos...")
			os.system("sudo sispmctl -o 1")
			os.system("sudo sispmctl -o 2")
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=23 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			ctr = ctr+1
			time.sleep(2)
			os.system("sispmctl -f 1")
			os.system("sispmctl -f 2")
			send('4','turning_holder..done')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=19 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			ctr=ctr+1
			time.sleep(2)
			send('4', 'turning_holder..done')
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
		mode = 3
		send('0', 'stopping compression')
		connect('3')
		print("Decompression experiment...")
		expName = raw_input("Enter name of experiment: ")
		os.system("mkdir "+expName)
		steps = input ("Total amount of steps: ")
		stepsPerStep = input ("Steps per step: ")
		sidelength = input ("Container sidelength: ")
		sidelength = sidelength/100
		STEPSPERCM = 1000.
		init()
		position = 0
	        f = open(expName + '/cVolume.dd', 'w')
		ctr=0
		while position < steps:
			print "Current position: " + str(position)
			print("Taking photos...")
			os.system("sispmctl -o 1")
			os.system("sispmctl -o 2")
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=23 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			ctr = ctr+1
			time.sleep(2)
			os.system("sispmctl -f 1")
			os.system("sispmctl -f 2")
			send('4','turning_holder..done')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=19 --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
			ctr=ctr+1
			time.sleep(2)
			send('4', 'turning_holder..done')
			print("Going to new position...")
			for i in range(1, stepsPerStep+1, 1):
				send('6', 'step..done');
				position = position + 1
				time.sleep(1)
				sidelength = sidelength + 1./(STEPSPERCM*100)
			f.write(str(sidelength*sidelength)+'\n')
			send('5', 'agitation..done')
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
		ctr=0
		print "HDRI capture mode"
		if mode != 4:
			os.system("(cd /home/pi/Documents/Arduino/DecompressionIno/; ino upload)")
                        print "Establishing connection to Arduino..."
                        time.sleep(3);
                        ser = serial.Serial('/dev/ttyACM0', 9600)
		connect('3')
		send('4','turning_holder..done')
		print "Enter shutter time choices. Press 'c' to continue: "
		enteredNo = raw_input("Next number (c to exit): ")
		shutterTimes = []
		while enteredNo != "c":
			shutterTimes.append(enteredNo)
			enteredNo = raw_input("Next number (c to exit): ")
                print("shutter time choices are ")
                print ', '.join(shutterTimes)
		os.system("mkdir hdr_src")
                button = "0"
		while button != "q":
			ctr=ctr+1
			os.system("mkdir hdr_src/"+str(ctr))
			os.system("cp list.txt hdr_src/"+str(ctr)+"/")
			os.system("sudo sispmctl -o 1")
			os.system("sudo sispmctl -o 2")
			os.system("sudo sispmctl -f 3")
			for i in shutterTimes:
                            print "gphoto2 --set-config-index /main/capturesettings/shutterspeed="+i+" --capture-image-and-download --filename='hdr_src/"+str(ctr)+"/"+i+".jpg' 2>/dev/null"
                            os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+i+" --capture-image-and-download --filename='hdr_src/"+str(ctr)+"/"+i+".jpg' 2>/dev/null")
			ctr=ctr+1
			os.system("mkdir hdr_src/"+str(ctr))
			os.system("cp list.txt hdr_src/"+str(ctr)+"/")
			send('4','turning_holder..done')
			os.system("sudo sispmctl -f 1")
			os.system("sudo sispmctl -f 2")
			os.system("sudo sispmctl -o 3")
			time.sleep(1)
			shctr=1
			for i in shutterTimes:
				shctr = shctr+1
				os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+i+" --capture-image-and-download --filename='hdr_src/"+str(ctr)+"/"+i+".jpg' 2>/dev/null")
			send('4','turning_holder..done')
			button = raw_input("Press any button to continue but 'q' for leaving");
	elif user_input == 5:
		if mode != 5:
			os.system("(cd /home/pi/Documents/Arduino/Ino/; ino upload)")
		mode = 5
		print "Uploading single wall control"
