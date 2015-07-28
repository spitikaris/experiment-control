#!/usr/bin/env python
import os

max_count = 0

max_count = input("How many image-sets were taken > ")

for folderNo in range(1,max_count+1):
    print "--------------------------------------------------------------------"
    print "Processing image "+str(folderNo)
    print "--------------------------------------------------------------------"
    os.system("./hdr hdr_src/"+str(folderNo))
    if folderNo % 2 !=0:
        os.system("mv hdr_src/"+str(folderNo)+"/fusion.png ./hdri/TI/"+str(folderNo)+".png")
    else:
        os.system("mv hdr_src/"+str(folderNo)+"/fusion.png ./hdri/SI/"+str(folderNo)+".png")

os.system("time ./panorama3 hdri/TI/")
