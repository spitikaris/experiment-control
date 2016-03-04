import camera_grid as cg
import time
import os
import gphoto2 as gp
import serial
import logging
import os
import subprocess
import sys

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

def one_photo_0(shutterspeed, filename):
    print filename
    os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=" + str(shutterspeed) + "--force-overwrite --capture-image-and-download --filename='"+filename+".jpg'")
    #os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=" + str(shutterspeed) + " --capture-image 2>/dev/null")


def init_camera():
    camera = gp.check_result(gp.gp_camera_new())
    context = gp.gp_context_new()
    gp.check_result(gp.gp_camera_init(camera, context))
    return (camera, context)



def one_photo(camera, context, value, filename):
    # get configuration tree
    config = gp.check_result(gp.gp_camera_get_config(camera, context))
    # find the capture target config item
    shutterspeed = gp.check_result(
        gp.gp_widget_get_child_by_name(config, 'shutterspeed'))
    # check value in range
    count = gp.check_result(gp.gp_widget_count_choices(shutterspeed))
    if value < 0 or value >= count:
        print('Parameter out of range')
        return 1
    # set value
    speedvalue = gp.check_result(gp.gp_widget_get_choice(shutterspeed, value))

    gp.check_result(gp.gp_widget_set_value(shutterspeed, speedvalue)) # set config gp.check_result(gp.gp_camera_set_config(camera, config, context))
    print('Capturing image (shutterspeed=%d)' % value)
    file_path = gp.check_result(gp.gp_camera_capture(
        camera, gp.GP_CAPTURE_IMAGE, context))

    target = filename+".jpg"

    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name,
            gp.GP_FILE_TYPE_NORMAL, context))
    gp.check_result(gp.gp_file_save(camera_file, target))


def exit_camera():
    gp.check_result(gp.gp_camera_exit(camera, context))



class ArduinoCommunicator:
    ser = serial.Serial('/dev/ttyACM0', 9600)
    def __init__(self, port, controlMode):
        if controlMode == "shear":
            os.system("(cd /home/piti_se/Arduino/controlledShear/; ino upload -p "+port+")")
        elif controlMode == "direct":
            os.system("(cd /home/piti_se/Arduino/StepperControlIno/; ino upload -p "+port+")")
        elif controlMode == "singleWall":
            os.system("(cd /home/piti_se/Arduino/GotoIno/; ino upload -p "+port+")")
        elif controlMode == "decompression":
            os.system("(cd /home/piti_se/Arduino/controlledDecompression/; ino upload -p "+port+")")
        self.ser = serial.Serial(port, 9600)
        print cg.bcolors.UNDERLINE+"experiment control is mounted on port "+str(port)+cg.bcolors.ENDC
        time.sleep(3);
    def send(self, signal, check, doneResponse):
        response = ''
        i = 0
        while check not in response:
            i+=1
            if i>10:
                print (cg.bcolors.FAIL + "Communication error" + cg.bcolors.ENDC)
                return
            self.ser.write(signal)
            time.sleep(1)
            response = self.ser.readline()
        print(cg.bcolors.RECEIVE + response)
        while doneResponse not in response:
            if "aborted" in response:
                print(response+cg.bcolors.ENDC)
                return
            response = self.ser.readline()
        print(cg.bcolors.RECEIVE + response)
        print(cg.bcolors.ENDC)
    def shear(self, steplength):
        buf = "$shear%%%d&\n" % steplength
        self.send(buf,"Shearing", "done")
    def compress(self, steplength):
        buf = "$compress%%%d&\n" % steplength
        self.send(buf, "Compressing...", "done.")
    def agitate(self, forSeconds):
        buf = "$agitate%%%d&\n" % forSeconds
        self.send(buf, "Agitating...", "done")
    def turn_holder(self, position):
        if position == "open":
            positionNo = 65
        elif position == "left-handed":
            positionNo = 155
        elif position == "right-handed":
            positionNo = 155
        buf = "$turn_holder_to_pos%%%d&\n" % positionNo
        self.send(buf,"Turning to", "done.")
    def turn_holder_to(self, position):
        buf = "$turn_holder_to_pos%%%d&\n" % position
        self.send(buf,"Turning to", "done.")


def take_photo2(grid,prefix,dark,arduino,reverse=0):
    if dark == 0:
        speed = 32 # 32 for only LED
    else:
        speed = 14
    os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed=" + str(speed));
    cam, cont = init_camera()
    cg.init()
    #cg.moveto(grid.corner[0],grid.corner[1])
    time.sleep(1)
    ctr = 0
    y_i = range(0,len(grid.points_in_y()))[::pow(-1,reverse)]
    if reverse == 1:
        ctr = len(grid.points_in_y())*len(grid.points_in_x())-1
    for i,y in enumerate(grid.points_in_y()[::pow(-1,reverse)]):
        x_i = range(0,len(grid.points_in_x()))[::pow(-1,i)*pow(-1,reverse)]
        for j,x in enumerate(grid.points_in_x()[::pow(-1,i)*pow(-1,reverse)]):
            cg.moveto(x,y)
            print "at pos: x=%d,y=%d" % (x_i[j],y_i[i])
            one_photo(cam, cont, speed, prefix+"_x"+str(x_i[j])+"y"+str(y_i[i]))
            if reverse == 0:
                ctr = ctr+1
            else:
                ctr = ctr-1


def take_photo(grid,prefix):
    cg.initWithACMPort(3)
    cg.moveto(grid.corner[0],grid.corner[1])
    time.sleep(1)
    ctr = 0
    for i in grid.points_in_x():
        for j in grid.points_in_y()[::pow(-1,ctr)]:
            cg.moveto(i,j)
            os.system("sispmctl -o 1")
            # #turn_holder('uncover')
            os.system("sispmctl -o 2")
            os.system("sispmctl -f 3")
            one_photo(lisspeed,prefix+str(ctr))
            ctr = ctr+1
            #time.sleep(5)
            # os.system("sispmctl -f 1")
            # os.system("sispmctl -f 2")
            # os.system("sispmctl -o 3")
    #turn_holder('right-handed')
#     os.system("gphoto2 --set-config-index /main/capturesettings/shutterspeed="+str(disspeed)+" --capture-image-and-download --filename='"+expName+"/"+expName+str(ctr)+"LH.jpg' 2>/dev/null")
    #turn_holder('left-handed')
    #take_photo(disspeed,expName+"/"+expName+str(ctr)+".jpg")
