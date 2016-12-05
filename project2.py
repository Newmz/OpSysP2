import sys
import os
import time


class process:
	def __init__(self, pname, mem, arrRun):
		self.processID = pname
		self.memNeeded = mem
		self.arrivalAndRunTimes = arrRun
		self.startIndex = -1
		self.endIndex = -1

	def __str__(self):
		retstr = "process object " + self.processID + ":\n\tMemory: "+str(self.memNeeded)+"\n\tArrival/Run Times:\n\t\t"
		for i in self.arrivalAndRunTimes:
			retstr += str(i[0]) + "/" +str(i[1]) + "\n\t\t"
		retstr = retstr[:-2]
		return retstr

# Start physical representation
def physical(allprocesses):

	# Single, one dimensional character array that will store only letters
	# Creates a 256 characters, all set to "."
	tableSize = 256

	processTable = ["." for x in range(tableSize)]

	# Initialize variables
	live = True					# For simulation status
	memFree = 256				# Available Memory
	time = 0					# Elapsed in milliseconds
	completed = 0				# Number of processes completely finished

	processTable = insertProcess(processTable, allprocesses[0], memFree, 0, 44)
	printTable(processTable)
	processTable = removeProcess(processTable, allprocesses[0])
	printTable(processTable)

	# Start Sim Loop
	while live:


		live = False
	# End Sim Loop
# End physical representation

# Start printTable
def printTable(processTable):
	# Print physical table
	for k in range(32):						# Top Bar
		print("=", end='')
	print("")
	for i in range(len(processTable)):		# Contents
		x = i % 32
		print("%s" %(processTable[i]), end='')
		if x == 31:
			print("")
	for k in range(32):						# Bottom Bar
		print("=", end='')
	print("")

	return 0
# End printTable

# Start process insertion
def insertProcess(processTable, targetProcess, memFree, startIndex, endIndex):

	# Decrement memory required
	memLeft = (int)(targetProcess.memNeeded)

	# Loop through processTable and add processID between indices
	if memLeft > memFree:
		print("Error, no memory available")
	else:
		for i in range(startIndex, endIndex):
			if processTable[i] != ".":
				print ("Error, memory already allocated in {1}".format(i))
			else:
				processTable[i] = targetProcess.processID

	return processTable
# End process insertion

def removeProcess(processTable, targetProcess):

	# Initialize counter for # of bytes removed
	bytesRemoved = 0

	# Loop through processTable and remove matching processID
	for i in range(len(processTable)):
		if processTable[i] == targetProcess.processID:
			processTable[i] = "."
			bytesRemoved += 1

	return processTable
# End process deletion



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
