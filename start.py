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
	print "(4) Move forward"
	print "(5) Move backward\n"
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
		

user_input = 1
ser = serial.Serial('/dev/ttyACM0', 9600)
while (user_input!=0):
	user_input = menu()
	
	if user_input == 1:
		print("Starting direct control mode...")
		connect ('1')
		ser.write('2')
		raw_input("Direct control mode is active. Hit RETURN to exit.")
		print("Waiting for shutdown...")
		waitForArduino('stopped')
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
		wall = input("Which wall shall be moved? (1) | (2) | (B)oth")
		connect('4')
		if wall == 1:
			print "Moving wall 1..."
			send('1', 'wall..check')
		elif wall == 2:
			ser.write('2')
		elif wall == 'B':
			ser.write('3')
		position = input("How many steps?: ")
		ser.write(len(str(position)))
		waitForArduino('digit_length..check');
		ser.write(position)
		waitForArduino('position..check')
		waitForArduino('done')
		print('Position was set.')
	elif user_input == 5:
		wall = input("Which wall shall be moved? (1) | (2) | (B)oth")
		connect('5')
		if wall == 1:
			ser.write('1')
		elif wall == 2:
			ser.write('2')
		elif wall == 'B':
			ser.write('3')
		waitForArduino('wall..check')
		position = input("How many steps?: ")
		ser.write(len(str(position)))
		waitForArduino('digit_length..check');
		ser.write(position)
		waitForArduino('position..check')
		waitForArduino('done')
		print('Position was set.')

		
			
