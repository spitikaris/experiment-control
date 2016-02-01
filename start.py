#!/usr/bin/python
import os
import time
import serial
from PIL import Image
from PIL.ExifTags import TAGS

#Constants:
lisspeed = 26 # 32 for only LED
disspeed = 12


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
        print "(4) Start Shear experiment"
        print "(5) Start HR image capture"
        print "(6) Single Wall movement"
	print "(7) GoTo Position"
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
	send('3', 'turning_holder..done')
    time.sleep(2)



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
#        print(bgcolors.HEADER + "Initializing x-y-stage" + bcolors.ENDC)

def setupFile(sidelength1, sidelength2,steps,stepsPerStep):
	s = open(expName + '/setup.ini', 'w')
	s.write('sidelength1='+str(sidelength1))
	s.write('sidelength2='+str(sidelength2))
	s.write('(LI)shutterspeed='+str(lisspeed))
	s.write('(DI)shutterspeed='+str(disspeed))
	s.write('totalSteps='+str(steps))
	s.write('diff='+str(stepsPerStep))
	s.close()


mode=0
user_input = 1
ser = serial.Serial('/dev/ttyACM0', 9600)
while (user_input!=0):
	user_input = menu()

	if user_input == 1:
		print("Starting direct control mode...")
		if (mode != 1):
			os.system("(cd /home/piti_se/Arduino/StepperControlIno/; ino upload)")
                        ser = serial.Serial('/dev/ttyACM0', 9600)
                        time.sleep(3)
		mode = 1
		print("Direct control is active.")
		uin = raw_input("Enter filename  to take a photo or <q> to quit...")
		if uin != 'q':
                        turn_holder('uncover')
			os.system("sispmctl -o 1")
			os.system("sispmctl -o 2")
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+uin+".jpg' 2>/dev/null")
			time.sleep(5)
			os.system("sispmctl -f 1")
			os.system("sispmctl -f 2")
                        turn_holder('right-handed')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+uin+"RH.jpg' 2>/dev/null")
                        time.sleep(5)
			turn_holder('left-handed')
			os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=18 --capture-image-and-download --filename='"+uin+"LH.jpg' 2>/dev/null")
                        send('0','exit')
	elif user_input == 2:
		if mode != 2:
			os.system("(cd /home/piti_se/Arduino/CompressionIno/; ino upload)")
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
			os.system("(cd /home/piti_se/Arduino/DecompressionIno/; ino upload)")
                        ser = serial.Serial('/dev/ttyACM0', 9600)
                        time.sleep(3);
		mode = 3
		connect('1')
		print("Decompression experiment...")
		expName = raw_input("Enter name of experiment: ")
		os.system("mkdir "+expName)
		steps = input ("Total amount of steps: ")
		stepsPerStep = input ("Steps per step: ")
		sidelength1 = input ("Container sidelength 1 [cm]: ")
		sidelength2 = input ("Container sidelength 2 [cm]: ")
		sidelength1 = sidelength1/100
		sidelength2 = sidelength2/100
		sidelength = sidelength1
		STEPSPERCM = 1000.
		position = 0
		g = open(expName + '/cVolume.d', 'w')
		f = open(expName + '/setup.dd', 'w')
		f.write("Experiment title:\t "+expName+"\n\n")
		f.write("Sidelength1 [m]: "+str(sidelength1)+"\n");
		f.write("Sidelength2 [m]: "+str(sidelength2)+"\n");
		f.write("Container volume [m^2]:\t "+str(sidelength1*sidelength2)+"\n")
		f.write("Number of steps: "+str(steps)+"\n");
		f.write("Stepsize: "+str(stepsPerStep)+"\n");
		f.close()
		ctr=0
		while position < steps:
		    print "Current position: " + str(position)
		    os.system("sispmctl -o 1")
		    turn_holder('uncover')
		    os.system("sispmctl -o 2")
		    os.system("sispmctl -f 3")
		    os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=" + str(lisspeed) + " --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
		    ctr = ctr+1
		    time.sleep(5)
		    os.system("sispmctl -f 1")
		    os.system("sispmctl -f 2")
		    os.system("sispmctl -o 3")
		    turn_holder('right-handed')
		    os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+str(disspeed)+ " --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+"LH.jpg' 2>/dev/null")
		    turn_holder('left-handed')
		    os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+str(disspeed)+" --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
		    ctr=ctr+1
		    time.sleep(2)
		    print("Going to new position...")
		    for i in range(1, stepsPerStep+1, 1):
			send('6', 'step..done');
			position = position + 1
			time.sleep(1)
			sidelength = sidelength + 1./(STEPSPERCM*100)
			g.write(str(sidelength*sidelength)+'\n')
		    send('8', 'agitation..done')
		send('4','turning_holder..done')
		send('0', 'stopping compression')
		os.system("sispmctl -f 3")
		print ("Source light turned off")
		os.system("sispmctl -f 4")
		print ("Motor and Stepper power turned off")
		os.system("sudo -u piti_se cp -r "+expName+ "/* /mnt/cluster/gamma/piti_se/Data/fna/"+expName+"/")
	elif user_input == 7:
	    if mode != 7:
		os.system("(cd /home/piti_se/Arduino/GotoIno/; ino upload)")
		ser = serial.Serial('/dev/ttyACM0', 9600)
		time.sleep(3);
	    mode = 7
	    connect('1')


        elif user_input == 4:
            if mode != 4:
                os.system("(cd /home/piti_se/Arduino/ShearIno/; ino upload)")
                ser = serial.Serial('/dev/ttyACM0', 9600)
                time.sleep(3);
            mode = 4
            connect('1')
            print("Shear experiment...")
            expName = raw_input("Enter name of experiment: ")
            os.system("mkdir "+expName)
            steps = input ("Total amount of steps: ")
            stepsPerStep = input ("Steps per step: ")
            sidelength1 = input ("Container sidelength 1 [cm]: ")
            sidelength2 = input ("Container sidelength 2 [cm]: ")
            sidelength1 = sidelength1/100
            sidelength2 = sidelength2/100
            STEPSPERCM = 1000.
            position = 0
            f = open(expName + '/setup.dd', 'w')
            f.write("Experiment title:\t "+expName+"\n\n")
            f.write("Sidelength1 [m]: "+str(sidelength1)+"\n");
            f.write("Sidelength2 [m]: "+str(sidelength2)+"\n");
            f.write("Container volume [m^2]:\t "+str(sidelength1*sidelength2)+"\n")
            f.write("Number of steps: "+str(steps)+"\n");
            f.write("Stepsize: "+str(stepsPerStep)+"\n");
            f.close()
            ctr=0
            while position < steps:
                print "Current position: " + str(position)
                print("Taking photos...")
                os.system("sispmctl -o 1")
                turn_holder('uncover')
                os.system("sispmctl -o 2")
                os.system("sispmctl -f 3")
                os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+str(lisspeed)+" --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
                ctr = ctr+1
                time.sleep(5)
                os.system("sispmctl -f 1")
                os.system("sispmctl -f 2")
                os.system("sispmctl -o 3")
                turn_holder('right-handed')
           #     os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+str(disspeed)+" --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+"LH.jpg' 2>/dev/null")
                turn_holder('left-handed')
                os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+str(disspeed)+" --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+".jpg' 2>/dev/null")
                ctr=ctr+1
                time.sleep(2)
                print("Going to new position...")
                for i in range(1, stepsPerStep+1, 1):
                    send('6', 'step..done');
                    position = position + 1
                    time.sleep(1)
                send('8', 'agitation..done')
                os.system("sispmctl -o 1")
            send('4','turning_holder..done')
            os.system("sispmctl -f 3")
            print ("Source light turned off")
            os.system("sudo -u piti_se cp -r "+expName+ "/* /mnt/cluster/gamma/piti_se/Data/fna/"+expName+"/")
            raw_input("Press RETURN to move the walls to the initial position...")
            os.system("entangle &")
            raw_input("Please take pictures of the final Volume first")
            os.system("sispmctl -o 1")
            send('7', 'returned');
            os.system("sispmctl -f all")
            print ("Motor and Stepper power turned off")
	elif user_input == 5:
                X_TOT = 1140
                Y_TOT = 1140
                x_steps = 5
		ctr=0
		print "HDRI capture mode"
		if mode != 5:
			os.system("(cd /home/piti_se/Arduino/hdriIno/; ino upload)")
                        print "Establishing connection to Arduino..."
                        ser = serial.Serial('/dev/ttyACM0', 9600)
                        time.sleep(3);
		connect('8')
                init(1)
#                turn_holder('uncover')
#		print "Enter shutter time choices. Press 'c' to continue: "
#		enteredNo = raw_input("Next number (c to exit): ")
#		shutterTimes = []
#		while enteredNo != "c":
#			shutterTimes.append(enteredNo)
#			enteredNo = raw_input("Next number (c to exit): ")
#                print("shutter time choices are ")
#                print ', '.join(shutterTimes)
                x_steps = input("Number of steps in x-direction: ")
                y_steps = input("Number of steps in y-direction: ")
#		os.system("mkdir hdr_src")
                button = "0"
                print bcolors.WARNING + "Prepare (10 sec)..." + bcolors.ENDC
                time.sleep(10);
                ctr = 0
		while button != "q":
                    for y in range(1,y_steps):
                        for x in range(1,x_steps):
                            ctr=ctr+1
        #			os.system("mkdir hdr_src/"+str(ctr))
                            #os.system("cp list.txt hdr_src/"+str(ctr)+"/")
        #			os.system("sudo sispmctl -o 1")
        #			os.system("sudo sispmctl -o 2")
        #			os.system("sudo sispmctl -f 3")
                            time.sleep(1)
        #			for i in shutterTimes:
        #                            os.system("gphoto2 --set-config-index \
        #                                    /main/capturesettings/shutterspeed="+i+" \
        #                                    --capture-image-and-download \
        #                                    --filename='hdr_src/"+str(ctr)+"/"+i+".jpg' \
        #                                    2>/dev/null")
        #                        writeLists("hdr_src/"+str(ctr)+"/")
                            ctr=ctr+1
        #                        os.system("mkdir hdr_src/"+str(ctr))
                            #os.system("cp list.txt hdr_src/"+str(ctr)+"/")
        #                        turn_holder('cover')
        #                        os.system("sudo sispmctl -f 1")
        #                        os.system("sudo sispmctl -f 2")
        #                        os.system("sudo sispmctl -o 3")
                            time.sleep(3)
        #                        for i in shutterTimes:
        #                                os.system("gphoto2 --set-config-index \
        #                                        /main/capturesettings/shutterspeed="+i+" \
        #                                        --capture-image-and-download \
        #                                        --filename='hdr_src/"+str(ctr)+"/"+i+".jpg' \
        #                                        2>/dev/null")
        #                        writeLists("hdr_src/"+str(ctr)+"/")
        #                        turn_holder('uncover')
                            x_stepper.step(int(X_TOT/x_steps), Adafruit_MotorHAT.BACKWARD,
                                    Adafruit_MotorHAT.DOUBLE);
                            time.sleep(1)
                        x_stepper.step(int(X_TOT-X_TOT/x_steps), Adafruit_MotorHAT.FORWARD, \
                                Adafruit_MotorHAT.DOUBLE);
                        y_stepper.step(int(Y_TOT/y_steps), Adafruit_MotorHAT.FORWARD, \
                                Adafruit_MotorHAT.DOUBLE);
                    y_stepper.step(int(Y_TOT-Y_TOT/y_steps), Adafruit_MotorHAT.BACKWARD, \
                            Adafruit_MotorHAT.DOUBLE);
                    print "Waiting for confirmation..."
                    send('1',"button_pressed..done")
                    #button = raw_input("Press any button to continue but 'q' for leaving");

	elif user_input == 6:
		if mode != 6:
			os.system("(cd /home/piti_se/Arduino/SingleWallIno/; ino upload)")
		mode = 6
		print "Uploading single wall control"
