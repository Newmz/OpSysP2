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
		self.order = 0 #int
		self.done = False #bool
		self.active = False #bool

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

	def insertContiguous(self, memory, freespace):
		# Contiguous add
		# loop through all memory and find
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

def defrag(memory, pList, t_memmove, time, startLocations):
	# input: the list of memory, the list of processes, the time it takes to move one unit of memory (in ms), and the current time of the sim
	# output: the number of seconds the defrag took
	# this function DOES NOT check whether or not there is enough free space to add a process.
	# It just performs the defrag and recomputes the arrival times, whether or not it's needed.

	#first, make a map of the processIDs to the processes themselves (speeds up things for later)
	pMap = {}
	for p in pList:
		pMap[p.processID] = p

	# Make list of processes moved during defrag
	outputList = []

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
			outputList.append(pMap[currentProcess].processID)


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

	for i in range(len(startLocations)):
		startLocations[i] -= diff

	print("time {0}ms: Defragmentation complete (moved {1} frames: ".format(time + timeTaken, timeTaken), end='')
	for i in outputList:
		print ("{0}".format(i), end='')
		if i != outputList[-1]:
			print (", ", end='')
	print(")")

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
		#print("Error, no memory available")
		return -10
	else:
		for i in range(startIndex, endIndex):
			# if processTable[i] != ".":
			#  	print ("Error, memory already allocated in {0}".format(i))
			if processTable[i] == ".":
				processTable[i] = targetProcess.processID
		# Return memory used
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

#Contiguous algorithm
def nextContiguous(pList):
	sorted(pList)
	tableSize = 256

	processTable = ["." for x in range(tableSize)]

	# Initialize variables
	live = True					# For simulation status
	memFree = 256				# Available Memory
	time = 0					# Elapsed in milliseconds
	completed = 0				# Number of processes completely finished


	startIndex = 0
	endIndex = 0
	startLocations = [0]

	# Start simulation
	print("time 0ms: Simulator started (Contiguous (Next Fit))")
	while live:
		# Start process removal
		# First we want to check if there are any process that need to be removed at this time step
		for process in pList:
			if process.readyToRem(time):
				process.active = False
				#this remove function returns the number of memory slots freed up
				memFree += removeProcess(processTable, process, time)
				print("time {0}ms: Process {1} removed:".format(time, process.processID))

				for f in startLocations:
					if process.endIndex == f:
						startLocations.remove(int(process.endIndex))

				process.startIndex = -1
				process.endIndex = -1
				printTable(processTable)
				if process.done:
					completed += 1
		# once all due processes have been removed, we can add new ones at this time step
		# End process removal

		# Start process insertion
		success = 0
		if len(startLocations) > 1:
			startIndex = startLocations[len(startLocations) - 1]
			endIndex = startIndex

		for process in pList:
			if process.readyToAdd(time):
				process.active = True
				freeCount = 0
				cellsChecked = 0
				i = 0
				freeTotal = 0
				#Start Next Fit Loop
				while cellsChecked < len(processTable):
					if startIndex == 256:
						startIndex = 0

					# End to beginning
					if startIndex + process.memNeeded - 1 >= len(processTable):
						startIndex = 0
						endIndex = 0
						freeCount = 0
						continue

					# Check if required memory is less than available memory
					if process.memNeeded <= freeCount:
						# Update current indices
						process.startIndex = startIndex
						process.endIndex = endIndex

						# Insert process into memory
						success = insertProcess(processTable, process, memFree, startIndex, endIndex)

						# Update most list of most recent indices
						startLocations.append(endIndex)
						break

					# Iterate through memory frames
					if processTable[i] == ".":
						freeCount += 1
						endIndex += 1
						freeTotal += 1
					else:
						freeCount = 0
						startIndex = i+1
						endIndex = i+1
					cellsChecked += 1
					i += 1

					if freeTotal >= process.memNeeded & process.memNeeded > freeCount:
						print("time {0}ms: Cannot place process {1} -- starting defragmentation".format(time, process.processID))
						defragTime = defrag(processTable, allprocesses, 1, time, startLocations)

						# Edit all process arrival/run times due to defrag
						for process in allprocesses:
							for arrUnd in process.arrivalAndRunTimes:
								if (process.active) & (time >= arrUnd[0]) & (time <= (arrUnd[0]+arrUnd[1])):
									arrUnd[1] += defragTime

						startLocations.pop(0)
						time += defragTime

						# Reset Values
						startIndex = startLocations[len(startLocations) - 1]
						endIndex = startIndex
						i = startIndex
						cellsChecked = 0
						freeCount = 0
						freeTotal = 0
						printTable(processTable)

				# End Next Fit Loop
				# Error Check
				if success > 0:
					memFree -= success
					#print("time {0}ms: Process {1} arrived (requires {2} frames)".format(time, process.processID, process.memNeeded))
					print("time {0}ms: Placed process {1}:".format(time, process.processID))
					#print (startLocations)
					printTable(processTable)
				else:
					#print (startLocations)
					print("time {0}ms: Cannot place process {1} -- skipped!".format(time, process.processID))
					# Remove set of arrival/run times
					process.arrivalAndRunTimes.pop(0)
					if len(process.arrivalAndRunTimes) == 0:
						process.done = True
						completed += 1
					printTable(processTable)
				#Reset success
				success = 0
		# End process insertion

		#if we've finished all processes (all have exited for the last time) then we are done
		if completed == len(pList):
			break
		time += 1
	print("time {0}ms: Simulator ended (Contiguous (Next Fit))".format(time))

#Contiguous algorithm
def bestContiguous(pList):
	sorted(pList)
	tableSize = 256

	processTable = ["." for x in range(tableSize)]

	# Initialize variables
	live = True					# For simulation status
	memFree = 256				# Available Memory
	time = 0					# Elapsed in milliseconds
	completed = 0				# Number of processes completely finished

	startLocations = [0]

	# Start simulation
	print("time 0ms: Simulator started (Contiguous -- Best Fit)")
	while live:
		# Start process removal
		# First we want to check if there are any process that need to be removed at this time step
		for process in pList:
			if process.readyToRem(time):
				process.active = False
				#this remove function returns the number of memory slots freed up
				memFree += removeProcess(processTable, process, time)
				print("time {0}ms: Process {1} removed:".format(time, process.processID))

				for f in startLocations:
					if process.endIndex == f:
						startLocations.remove(int(process.endIndex))
				process.startIndex = -1
				process.endIndex = -1
				printTable(processTable)
				if process.done:
					completed += 1
		# once all due processes have been removed, we can add new ones at this time step
		# End process removal

		# Start process insertion
		success = 0
		if len(startLocations) > 1:
			startIndex = startLocations[len(startLocations) - 1]
			endIndex = startIndex

		for process in pList:
			if process.readyToAdd(time):
				# Initialize variables
				process.active = True
				cellsChecked = 0
				i = 0
				freeTotal = 0
				smallestRegion = memFree

				# Start Best Fit Loop
				startIndex = 0
				endIndex = 0

				while cellsChecked < len(processTable):
					# Find smallest region
					# print("Finding Regions")
					regions = []
					startIndex = 0
					freeCount = 0
					for bestTarget in range(len(processTable)):
						# Iterate through memory frames
						if processTable[bestTarget] == ".":
							freeCount += 1
							freeTotal += 1
						else:
							if freeCount > 0:
								regions.append((freeCount, startIndex))
							freeCount = 0
							startIndex = bestTarget + 1

					if freeCount > 0:
						regions.append((freeCount, startIndex))

					# Sort regions
					regions = sorted(regions)
					# Iterate through regions and find best fit for insertion
					foundRegion = False
					for selected in range(len(regions)):
						# Free memory >= space needed && free memory < current smallestRegion
						if ((regions[selected][0] >= process.memNeeded) & (regions[selected][0] < smallestRegion)):
							# print("Found a good region on region of size {0}".format(regions[selected][0]))
							smallestRegion = regions[selected][0]
							startIndex = regions[selected][1]
							foundRegion = True
							break

					# Look for defrag if space available but no regions free
					if foundRegion == False:
						if ((freeTotal >= process.memNeeded) & (process.memNeeded >= smallestRegion)):
							print("time {0}ms: Cannot place process {1} -- starting defragmentation".format(time, process.processID))
							defragTime = defrag(processTable, allprocesses, 1, time, startLocations)

							# Edit all process arrival/run times due to defrag
							for process in allprocesses:
								for arrUnd in process.arrivalAndRunTimes:
									if (process.active) & (time >= arrUnd[0]) & (time <= (arrUnd[0]+arrUnd[1])):
										arrUnd[1] += defragTime

							startLocations.pop(0)
							time += defragTime

							# Reset Values
							startIndex = startLocations[len(startLocations) - 1]
							endIndex = startIndex
							i = startIndex
							cellsChecked = 0
							freeCount = 0
							freeTotal = 0
							printTable(processTable)

					# Update current indices
					process.startIndex = startIndex
					endIndex = startIndex + process.memNeeded
					process.endIndex = endIndex

					# Insert processes into memory
					success = insertProcess(processTable, process, memFree, startIndex, endIndex)

					# Update most list of most recent indices
					startLocations.append(endIndex)
					break

					endIndex = i+1
					cellsChecked += 1
					i += 1

				# End Next Fit Loop
				# Error Check
				if success > 0:
					memFree -= success
					print("time {0}ms: Placed process {1}:".format(time, process.processID))
					printTable(processTable)
				else:
					print("time {0}ms: Cannot place process {1} -- skipped!".format(time, process.processID))
					# Remove set of arrival/run times
					process.arrivalAndRunTimes.pop(0)
					if len(process.arrivalAndRunTimes) == 0:
						process.done = True
						completed += 1
					printTable(processTable)
				#Reset success
				success = 0
		# End process insertion

		#if we've finished all processes (all have exited for the last time) then we are done
		if completed == len(pList):
			break
		time += 1
	print("time {0}ms: Simulator ended (Contiguous -- Bext Fit)".format(time))

def getWorst(processTable, process, largestRegion, freeTotal):
	# Find largest region
	regions = []
	startIndex = 0
	freeCount = 0
	for worstTarget in range(len(processTable)):
		# Iterate through memory frames
		if processTable[worstTarget] == ".":
			freeCount += 1
			freeTotal += 1
		else:
			if freeCount > 0:
				regions.append((freeCount, startIndex))
			freeCount = 0
			startIndex = worstTarget + 1

	if freeCount > 0:
		regions.append((freeCount, startIndex))

	# Sort regions
	regions = sorted(regions, reverse=True)
	#print(regions)
	# Iterate through regions and find worst fit for insertion
	foundRegion = False
	for selected in range(len(regions)):
		# Free memory >= space needed && free memory < current largestRegion
		if ((regions[selected][0] >= process.memNeeded) & (regions[selected][0] < largestRegion)):
			# print("Found a good region on region of size {0}".format(regions[selected][0]))
			largestRegion = regions[selected][0]
			startIndex = regions[selected][1]
			foundRegion = True
			break


	return largestRegion, startIndex

#Contiguous algorithm
def worstContiguous(pList):
	sorted(pList)
	tableSize = 256

	processTable = ["." for x in range(tableSize)]

	# Initialize variables
	live = True					# For simulation status
	memFree = 256				# Available Memory
	time = 0					# Elapsed in milliseconds
	completed = 0				# Number of processes completely finished

	startLocations = [0]

	# Start simulation
	print("time 0ms: Simulator started (Contiguous -- Worst Fit)")
	while live:
		# Start process removal
		# First we want to check if there are any process that need to be removed at this time step
		for process in pList:
			if process.readyToRem(time):
				process.active = False
				#this remove function returns the number of memory slots freed up
				memFree += removeProcess(processTable, process, time)
				print("time {0}ms: Process {1} removed:".format(time, process.processID))

				for f in startLocations:
					if process.endIndex == f:
						startLocations.remove(int(process.endIndex))
				process.startIndex = -1
				process.endIndex = -1
				printTable(processTable)
				if process.done:
					completed += 1
		# once all due processes have been removed, we can add new ones at this time step
		# End process removal

		# Start process insertion
		success = 0
		if len(startLocations) > 1:
			startIndex = startLocations[len(startLocations) - 1]
			endIndex = startIndex

		for process in pList:
			if process.readyToAdd(time):
				# Initialize variables
				process.active = True
				cellsChecked = 0
				i = 0
				freeTotal = 0
				largestRegion = memFree

				# Start Worst Fit Loop
				startIndex = 0
				endIndex = 0

				while cellsChecked < len(processTable):
					largestRegion, startIndex = getWorst(processTable, process, largestRegion, freeTotal)
					# Find largest region
					regions = []
					startIndex = 0
					freeCount = 0
					for worstTarget in range(len(processTable)):
						# Iterate through memory frames
						if processTable[worstTarget] == ".":
							freeCount += 1
							freeTotal += 1
						else:
							if freeCount > 0:
								regions.append((freeCount, startIndex))
							freeCount = 0
							startIndex = worstTarget + 1

					if freeCount > 0:
						regions.append((freeCount, startIndex))

					# Sort regions
					regions = sorted(regions, reverse=True)
					#print(regions)
					# Iterate through regions and find worst fit for insertion
					foundRegion = False
					for selected in range(len(regions)):
						# Free memory >= space needed && free memory < current largestRegion
						# print(regions[selected][0])
						# print(process.memNeeded)
						# print(largestRegion)
						if ((regions[selected][0] >= process.memNeeded) & (regions[selected][0] >= largestRegion)):
							# print("Found a good region on region of size {0}".format(regions[selected][0]))
							largestRegion = regions[selected][0]
							startIndex = regions[selected][1]
							foundRegion = True
							break

					# Look for defrag if space available but no regions free
					if foundRegion == False:
						if ((freeTotal >= process.memNeeded) & (process.memNeeded >= largestRegion)):
							print("time {0}ms: Cannot place process {1} -- starting defragmentation".format(time, process.processID))
							defragTime = defrag(processTable, allprocesses, 1, time, startLocations)

							# Edit all process arrival/run times due to defrag
							for process in allprocesses:
								for arrUnd in process.arrivalAndRunTimes:
									if (process.active) & (time >= arrUnd[0]) & (time <= (arrUnd[0]+arrUnd[1])):
										arrUnd[1] += defragTime

							startLocations.pop(0)
							time += defragTime

							# Reset Values
							startIndex = startLocations[len(startLocations) - 1]
							endIndex = startIndex
							i = startIndex
							cellsChecked = 0
							freeCount = 0
							freeTotal = 0
							printTable(processTable)
							largestRegion, startIndex = getWorst(processTable, process, largestRegion, freeTotal)

					# Update current indices
					process.startIndex = startIndex
					endIndex = startIndex + process.memNeeded
					process.endIndex = endIndex

					# Insert processes into memory
					# print("Startindex = {0}".format(startIndex))
					# print("Endindex = {0}".format(endIndex))
					success = insertProcess(processTable, process, memFree, startIndex, endIndex)

					# Update most list of most recent indices
					startLocations.append(endIndex)
					break

					endIndex = i+1
					cellsChecked = 1
					i += 1

				# End Next Fit Loop
				# Error Check
				if success > 0:
					memFree -= success
					print("time {0}ms: Placed process {1}:".format(time, process.processID))
					printTable(processTable)
				else:
					# print(regions)
					# print(startIndex)
					# print(endIndex)
					print("time {0}ms: Cannot place process {1} -- skipped!".format(time, process.processID))
					# Remove set of arrival/run times
					process.arrivalAndRunTimes.pop(0)
					if len(process.arrivalAndRunTimes) == 0:
						process.done = True
						completed += 1
					printTable(processTable)
				#Reset success
				success = 0
		# End process insertion

		#if we've finished all processes (all have exited for the last time) then we are done
		if completed == len(pList):
			break
		time += 1
	print("time {0}ms: Simulator ended (Contiguous -- Bext Fit)".format(time))


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
				memFree += process.removeNonContiguous(processTable, time)
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
					print("time {0}ms: cannot place process {1} -- skipped!".format(time, process.processID))
		#if we've finished all processes (all have exited for the last time) then we are done
		if completed == len(pList):
			break
		time += 1
	print("time {0}ms: Simulator ended (Non-contiguous)".format(time))


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
		print (arrivalAndRunTimes)
		allprocesses.append(process(processID,memNeeded,arrivalAndRunTimes))

	for p in allprocesses:
		print(p)

	physical(allprocesses)
	#nextContiguous(allprocesses)
	#bestContiguous(allprocesses)
	worstContiguous(allprocesses)
	#nonContiguous(allprocesses)
	#virtualMemory()
