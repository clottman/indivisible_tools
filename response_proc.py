#!/usr/bin/env python3

import tkinter as tk
import tkinter.filedialog as tkF
from tkinter import messagebox
import itertools
import sys

root = tk.Tk()
root.withdraw()
root.update()
read_file = tkF.askopenfilename()

write_file = input("Enter output filename:")

writing = "Writing - press releases, email, calling scripts, speeches"
public = "Public Speaking"

allSkillOptions = [writing, public] #...

if write_file[-4:] != ".csv":
	write_file = write_file + ".csv"

print("Now converting " +read_file)

responseLines = []

try: 
	with open(read_file, 'r') as rf: 

		 
		# Skip first lines: start=1, stop=None
		for line in itertools.islice(rf, 1, None):  
			person_response = line.split("\n")
			#responseLines.append(split_line)
			#print(person_response[0])
			columns_in_response = person_response[0].split("\",\"")
			for column in columns_in_response:
				print(column)
				print("\n")
			print("\n")
#				if (len(split_line) > 2):
#					wf.write(split_line[2] + ",\n")
	

#print(responseLines)
	print("\n\n\n\n")
	for person in responseLines:
		print(person)
		print("\n")

except IndexError:
	print("Some line had the wrong # of columns. Unable to continue")
except :
	print("Unable to process this file. :(")
	raise


#with open(write_file, 'w') as wf:
	#for line in itertools.islice(rf, 0, 1):
#		wf.write(line)

		### write more output here
#		print("All done! Output located at " + write_file + "\n")





input("Press any key to exit")


	

