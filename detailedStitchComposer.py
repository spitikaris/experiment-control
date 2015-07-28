#!/usr/bin/env python
import os

max_count = 0
max_count = input("How many images > ")
even = 0
even = input("Are the image numbers even (1) or odd (0)? > ")
directory = "./"
directory = raw_input("Where are the images located > ")

fileList = ""
for i in range(1,max_count):
	if (i+even) % 2 != 0: 
		fileList = fileList + directory + str(i) + ".png "

print "./sd --features orb "+fileList
os.system("./sd --features orb "+fileList)
