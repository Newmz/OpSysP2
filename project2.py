import sys
import os
import time


class process:
	def __init__(self, pname, mem, arrRun):
		self.processID = pname
		self.memNeeded = mem
		self.arrivalAndRunTimes = arrRun

	def __str__(self):
		retstr = "process object " + self.processID + ":\n\tMemory: "+str(self.memNeeded)+"\n\tArrival/Run Times:\n\t\t"
		for i in self.arrivalAndRunTimes:
			retstr += str(i[0]) + "/" +str(i[1]) + "\n\t\t"
		retstr = retstr[:-2]
		return retstr

def physical(allprocesses):
	print("Hello World")
	# Creates a list containing 8 lists, each of 32 items, all set to "."
	tableSize = 256
	processTable = ["." for x in range(tableSize)]

	# Print physical table
	for k in range(32):						# Top Bar
		print("=", end='')
	print("")
	for i in range(len(processTable)):		# Contents
		x = i % 32
		print("%s" %(processTable[x]), end='')
		if x == 31:
			print("")
	for k in range(32):						# Bottom Bar
		print("=", end='')
	print("")

	processTable[0]

if __name__ == '__main__':

	allprocesses = []
	allLines = open(sys.argv[1]).readlines()
	numprocesses = allLines[0]
	for i in range(1, len(allLines)):
		x = allLines[i].split()
		processID = x[0]
		memNeeded = x[1]
		arrivalAndRunTimes = []
		for j in range(2, len(x)):
			arrivalAndRunTimes.append(x[j].split('/'))
		allprocesses.append(process(processID,memNeeded,arrivalAndRunTimes))

	for p in allprocesses:
		print(p)

	physical(allprocesses)
