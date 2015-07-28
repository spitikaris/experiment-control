#!/usr/bin/env python
import os

max_count = 0
max_count = input("How many image-sets were taken > ")

for imageNo in range(1, max_count):
	if imageNo % 2 !=0:
		os.system("mv hdri/"+str(imageNo)+".png hdri/TI/"+str(imageNo)+".png");
	else:
		os.system("mv hdri/"+str(imageNo)+".png hdri/SI/"+str(imageNo)+".png");


