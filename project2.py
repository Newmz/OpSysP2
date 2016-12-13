import sys
import os
import time


class process:
	def __init__(self, pname, mem, arrRun):
		self.processID = pname #string
		self.memNeeded = mem #int
		self.arrivalAndRunTimes = arrRun #list(list(int,int)) ---> [[0,1], [1,2], ..... , [x,y]]
		self.startIndex = -1 #int
		self.endIndex = -1 #int
		self.pageTable = [] #list(int)
		self.done = False #bool
		self.hasEntered = False

	def __str__(self):
		retstr = "process object " + self.processID + ":\n\tMemory: "+str(self.memNeeded)+"\n\tArrival/Run Times:\n\t\t"
		for i in self.arrivalAndRunTimes:
			retstr += str(i[0]) + "/" +str(i[1]) + "\n\t\t"
		retstr = retstr[:-2]
		return retstr

	def __lt__(self, other):
		return self.processID < other.processID


	# given a representation of memory (the '.' list), and the number of free slots available,
	# add a process non-contiguously to the memory.
	# return -1 if there isn't enough space, or the number of memory slots used otherwise.
	def insertNonContiguous(self, memory, freespace):
		# non-contiguous add
		# loop through all memory and find the first x open slots (however many are necessary)
		# for each one, change the memory's letter to the process letter and change the process'
		# page table to include it.
		# the page table should look like this:
		#		self.pageTable[0] = <physical memory index>
		
		if freespace < self.memNeeded:
			#failure, so must skip process
			#print("process {0} failure in adding".format(self.processID))
			return -1
		else:
			temp = 0
			for page in range(len(memory)):
				if temp == self.memNeeded:
					break
				if memory[page] == '.':
					memory[page] = self.processID
					self.pageTable.append(page)
					temp+=1
			return self.memNeeded

	def removeNonContiguous(self, memory, time):
		#go through memory, removing anything that has processID, and clear the page Table
		pagesCleared = 0
		while len(self.pageTable) > 0:
			memory[self.pageTable.pop()] = '.'
			pagesCleared +=1
		#if this was the last time the process leaves the simulation, mark it 'finished'
		if time == self.arrivalAndRunTimes[-1][1] + self.arrivalAndRunTimes[-1][0]:
			self.done = True
		return pagesCleared


	def readyToAdd(self, time):
		# returns true if the process is to be added at the given time, false otherwise
		for at in range(len(self.arrivalAndRunTimes)):
			if self.arrivalAndRunTimes[at][0] == time:
				
				print("time {0}ms: Process {1} arrived (requires {2} frames)".format(time, self.processID, self.memNeeded))
				return True
		return False

	def readyToRem(self, time):
		# returns true if the process is to be removed at the given time, false otherwise
		for at in self.arrivalAndRunTimes:
			if at[0]+at[1] == time:
				return True
		return False

def defrag(memory, pList, t_memmove, time):
	# input: the list of memory, the list of processes, the time it takes to move one unit of memory (in ms), and the current time of the sim
	# output: the number of seconds the defrag took
	# this function DOES NOT check whether or not there is enough free space to add a process.
	# It just performs the defrag and recomputes the arrival times, whether or not it's needed. 

	#first, make a map of the processIDs to the processes themselves (speeds up things for later)
	pMap = {}
	for p in pList:
		pMap[p.processID] = p

	#keep track of the lowest index of free memory and the time it has taken to defrag so far
	firstFreeLoc = None
	timeTaken = 0

	unit = 0
	while unit < len(memory):
		if memory[unit] != '.':
			#if we find a used slot of memory, we shift that process down
			if firstFreeLoc == None:
				#print("\t skipping")
				unit +=1
				continue

			start = unit
			currentProcess = memory[unit]
			diff = start - firstFreeLoc  # offset by which we shift the process
			pMap[currentProcess].startIndex -= diff
			pMap[currentProcess].endIndex -= diff

			while unit < start + pMap[currentProcess].memNeeded and unit < len(memory):
				#print(start, diff, unit)
				memory[unit-diff] = currentProcess
				memory[unit] = '.'
				timeTaken += t_memmove
				unit+=1
				#diff+=1

			#printTable(memory)
			firstFreeLoc += pMap[currentProcess].memNeeded
		else:
			if firstFreeLoc == None:
				#print("\tFFL is now {0}".format(unit))
				firstFreeLoc = unit
			unit += 1
			continue

	#this part will increase the arrival times of all processes accordingly (namely, if they enter during defrag,
	#they are pushed back by the length of the defrag).
	for p in pList:
		for arrivals in p.arrivalAndRunTimes:
			if arrivals[0] > time:
				arrivals[0] += timeTaken
	return timeTaken





# Start physical representation
def physical(allprocesses):

	sorted(allprocesses)
	tableSize = 256

	processTable = ["." for x in range(tableSize)]

	# Initialize variables
	live = True					# For simulation status
	memFree = 256				# Available Memory
	time = 0					# Elapsed in milliseconds
	completed = 0				# Number of processes completely finished
	scanStart = 0

	while live:
		#	GENERAL pseudocode
		#
		#	at current timestep:
		#		if any processes need to be removed, remove them (I wrote a class function that checks whether or need it needs to be removed)
		#		if any processes need to be added, try to add them (I also wrote a class function for this check)
		#			if there lacks space then skip it
		#			if there is space but not a contiguous block, then defrag
		#		if the number of completed processes is equal to the length of allprocesses, then live = false
		live = False


		#live = False
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
#	output: The number of units of memory used.
# Start process insertion
def insertProcess(processTable, targetProcess, memFree, startIndex, endIndex):
	# Decrement memory required
	memLeft = (targetProcess.memNeeded)

	# Loop through processTable and add processID between indices
	if memLeft > memFree:
		print("Error, no memory available")
		return -1
	else:
		for i in range(startIndex, endIndex):
			if processTable[i] != ".":
				print ("Error, memory already allocated in {0}".format(i))
			else:
				processTable[i] = targetProcess.processID

	return targetProcess.memNeeded


# removeProcess
#	input: a processTable and targetProcess and the time of sim,
#	output: the number of units of memory freed.
# Start process deletion
def removeProcess(processTable, targetProcess, time):
	# Initialize counter for # of bytes removed
	bytesRemoved = 0

	# Loop through processTable and remove matching processID
	for i in range(len(processTable)):
		if processTable[i] == targetProcess.processID:
			processTable[i] = "."
			bytesRemoved += 1

	# PETER, this code is new. when a process is removed for the last time, its "done" bool is set to True.
	# check to see if a process is 'done' every time you remove a process (outside this function).
	# see non-contiguous for an example
	if time == targetProcess.arrivalAndRunTimes[-1][1] + targetProcess.arrivalAndRunTimes[-1][0]:
		targetProcess.done = True

	return bytesRemoved


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


#Non contiguous algorithm
def nonContiguous(pList):
	sorted(pList)
	tableSize = 256

	processTable = ["." for x in range(tableSize)]

	# Initialize variables
	live = True					# For simulation status
	memFree = 256				# Available Memory
	time = 0					# Elapsed in milliseconds
	completed = 0				# Number of processes completely finished

	print("time 0ms: Simulator started (Non-contiguous)")
	while live:
		#first we want to check if there are any process that need to be removed at this time step
		for process in pList:
			if process.readyToRem(time):
				#this remove function returns the number of memory slots freed up
				success = process.removeNonContiguous(processTable, time)
				memFree += success
				if (success):
					print("time {0}ms: Process {1} removed:".format(time, process.processID))
					printTable(processTable)
				if process.done:
					completed += 1
		#once all due processes have been removed, we can add new ones at this time step
		for process in pList:
			if process.readyToAdd(time):
				success = process.insertNonContiguous(processTable, memFree)
				if success > 0:
					memFree -= success
					print("time {0}ms: Placed process {1}:".format(time, process.processID))
					printTable(processTable)
				else:
					print("time {0}ms: Cannot place process {1} -- skipped!".format(time, process.processID))
					printTable(processTable)
		#if we've finished all processes (all have exited for the last time) then we are done
		if completed == len(pList):
			break
		time += 1
	print("time {0}ms: Simulator ended (Non-contiguous)".format(time), end="")


if __name__ == '__main__':
	
	#this first bit parses the file with all of the process info
	allprocesses = []
	allLines = open(sys.argv[1]).readlines()
	numprocesses = allLines[0]
	for i in range(1, len(allLines)):
		x = allLines[i].split()
		processID = x[0]
		memNeeded = int(x[1])
		arrivalAndRunTimes = []
		for j in range(2, len(x)):
			t = x[j].split('/')
			t[0] = int(t[0])
			t[1] = int(t[1])
			arrivalAndRunTimes.append(t)
		allprocesses.append(process(processID,memNeeded,arrivalAndRunTimes))

	#

	physical(allprocesses)
	nonContiguous(allprocesses)
	#virtualMemory()
