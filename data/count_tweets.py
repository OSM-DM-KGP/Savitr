import sys
import os

# explicitly set for 32 days
floods = [0]*32
dengue = [0]*32
situation = {'floods': floods, 'dengue': dengue}

for file in os.listdir(os.getcwd()):
	day = int(file.split('_')[-2])
	scene = file.split('_')[-3]
	print day, scene
	num_lines = sum(1 for line in open(file))
	situation[scene][day] = num_lines

for i in range(32):
	print str(i) + '\t' + str(dengue[i]) + '\t' + str(floods[i])