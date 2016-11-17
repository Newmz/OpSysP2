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
	