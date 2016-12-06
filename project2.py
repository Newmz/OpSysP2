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
	processTable, bytesRemoved = removeProcess(processTable, allprocesses[0])
	printTable(processTable)

	# Start Sim Loop
	while live:


		live = False
	# End Sim Loop
# End physical representation


# printTable,
#	input: a processTable
#	output: prints processTable and returns 0 on success
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

# insertProcess,
#	input: a processTable and targetProcess,
#	output: processTable with targetProcess inserted.
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

# removeProcess
#	input: a processTable and targetProcess,
#	output: processTable with targetProcess removed.
# Start process deletion
def removeProcess(processTable, targetProcess):
	# Initialize counter for # of bytes removed
	bytesRemoved = 0

	# Loop through processTable and remove matching processID
	for i in range(len(processTable)):
		if processTable[i] == targetProcess.processID:
			processTable[i] = "."
			bytesRemoved += 1

	return processTable, bytesRemoved
# End process deletion

# Handles all the virtual memory functions
#   reads in vitual memory frames
#   runs three algorithms:
#       Optimal (OPT)
#       Least-Recently Used (LRU)
#       Least-Frequently Used (LFU)
def virtualMemory():
	#Read input file for vitual memory frames
	frames = []
	frames = open(sys.argv[2]).read()
	framearray = frames.split()

	OPT(framearray)
	print()
	LRU(framearray)
	print()
	LFU(framearray)

# Simulates optimal algorithm for virtual memory
def OPT(framearray, F = 3):
	print("Simulating OPT with fixed frame size of {0}".format(F))

	mem = []
	numfaults = 0
	for i in range(len(framearray)):
		# Frame not already in memory 
		if framearray[i] not in mem:
			# No page fault
			if len(mem) < 3:
				mem.append(framearray[i])
				print("referencing page {0} [mem:".format(framearray[i]), end='')
				for y in mem:
					print(" {0}".format(y), end='')
				for n in range(len(mem), 3):
					print(" .", end='')
				print("] PAGE FAULT (no victim page)")

			# Page fault
			else:
				numfaults += 1
				# Read memory into new array
				longest = []
				for x in mem:
					longest.append(x)

				# Step forward to find fututre uses
				for j in range(i + 1, len(framearray)):
					if len(longest) == 1:
						break
					elif framearray[j] in longest:
						longest.pop(longest.index(framearray[j]))

				#Tiebreaker
				if len(longest) != 1:
					longest = [min(longest)]

				mem[mem.index(longest[0])] = framearray[i]
				print("referencing page {0} [mem:".format(framearray[i]), end='')
				for x in mem:
					print(" {0}".format(x), end='')
				print("] PAGE FAULT (victim page {0})".format(longest[0]))
	print("End of OPT simulation ({0} page faults)".format(numfaults))


# Simulates Least-Recently Used algorithm for virtual memory
def LRU(framearray, F  = 3):
	print("Simulating LRU with fixed frame size of {0}".format(F))

	mem = []
	numfaults = 0
	for i in range(len(framearray)):
		# Frame not already in memory 
		if framearray[i] not in mem:
			# No page fault
			if len(mem) < 3:
				mem.append(framearray[i])
				print("referencing page {0} [mem:".format(framearray[i]), end='')
				for y in mem:
					print(" {0}".format(y), end='')
				for n in range(len(mem), 3):
					print(" .", end='')
				print("] PAGE FAULT (no victim page)")

			# Page fault
			else:
				numfaults += 1
				# Read memory into new array
				oldest = []
				for x in mem:
					oldest.append(x)

				# Step backwards to find past uses
				for j in range( i-1, -1, -1):
					if len(oldest) == 1:
						break
					elif framearray[j] in oldest:
						oldest.pop(oldest.index(framearray[j]))

				mem[mem.index(oldest[0])] = framearray[i]
				print("referencing page {0} [mem:".format(framearray[i]), end='')
				for x in mem:
					print(" {0}".format(x), end='')
				print("] PAGE FAULT (victim page {0})".format(oldest[0]))
	print("End of LRU simulation ({0} page faults)".format(numfaults))

# Simulates Least-Frequently Used algorithm for virtual memory
def LFU(framearray, F = 3):
	print("Simulating LFU with fixed frame size of {0}".format(F))

	mem = []
	uses = []
	numfaults = 0
	for i in range(len(framearray)):
		# Frame not already in memory 
		if framearray[i] not in mem:
			# No page fault
			if len(mem) < 3:
				mem.append(framearray[i])
				uses.append(1)
				print("referencing page {0} [mem:".format(framearray[i]), end='')
				for y in mem:
					print(" {0}".format(y), end='')
				for n in range(len(mem), 3):
					print(" .", end='')
				print("] PAGE FAULT (no victim page)")

			# Page fault
			else:
				numfaults += 1
				# Find index of smallest with tiebreaker
				leastidx = 0
				for j in range(len(uses)):
					if uses[j] < uses[leastidx] or (uses[j] == uses[leastidx] and mem[j] < mem[leastidx]):
						leastidx = j

				victim = mem[leastidx]
				mem[leastidx] = framearray[i]
				uses[leastidx] = 1
				print("referencing page {0} [mem:".format(framearray[i]), end='')
				for x in mem:
					print(" {0}".format(x), end='')
				print("] PAGE FAULT (victim page {0})".format(victim))

		# Frame already in memory
		else:
			# Increment uses
			uses[mem.index(framearray[i])] += 1

	print("End of LFU simulation ({0} page faults)".format(numfaults))


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

	virtualMemory()
