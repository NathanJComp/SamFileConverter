import os
def computeMid(time):
	time = [int(x) for x in time]
	if time[3]<13:
		time[3]+=12
	else:
		time[2]+=1
		time[3]+=12
	for i in range(len(time)):
		time[i]=str(time[i])
		
		while len(time[i])<2:
			time[i]='0'+time[i]
	
	time=':'.join(time)
	
	return time

def findBlack(fileName):
	midTimes=[]
	inputFile=open(fileName,'r')
	outlist=[]
	for line in inputFile:
		line=line.split()
		
		if len(line)==8:
			if line[1]=='HAW_BLAC':
				
				if line[2]=='V':
					
					startTime=line[6]
					startTime=startTime.split(':')
					
					midTime=computeMid(startTime)
					midTimes.append(midTime)
					
	return midTimes

def printOutput(outputFile, midTimes):
	try:
		outputFile=open(outputFile,'w')
	except IOError:
		raise
	for x in midTimes:
		outLine = 'User ' + str(x) + ' V1  red\n'
		outputFile.write(outLine)
	outputFile.close()
	
def main():
	validInput=False
	
	while(not validInput):
		inputMode=input("\nPlease type 's' for single file conversion, 'b' for batch or 'q' for quit\nNOTE: Batch mode requires a folder in this directory called CONVERT which contains those files to be converted, and another folder 'CONVERTED' where the output will be stored\n")
		if inputMode=='s':
			while not validInput:
				inputName=input("\nPlease enter filename you wish to convert, including extentsion\n")
				outputName=input("\nPlease enter filename you wish to write output to, including extentsion (probably .txt)\nIf the file does not exist, it will be created\n")
				try:
					midTimes = findBlack(inputName)
					printOutput(outputName,midTimes)
					validInput=True
				except IOError:
					print("\ninvalid filename(s)")
			close=input("Press any key to exit")
		elif inputMode=="b":
			if os.path.exists(os.getcwd()+"\CONVERT"):
				newpath = os.getcwd()+'\CONVERTED'
				if not os.path.exists(newpath): 
					os.makedirs(newpath)
				print("Names of processed files")
			
				for fileName in os.listdir(os.getcwd()+"\CONVERT"):
					if fileName[-4:]==".txt":
						print(fileName)
						midTimes=findBlack(os.getcwd()+'\CONVERT\\'+fileName)
						printOutput(os.getcwd()+'\CONVERTED\\'+fileName,midTimes)
			else:
				print("\nNo directory 'CONVERT' found. Please close the program, create such a directory and try again")

			validInput=True
			close=input("Press any key to exit")
		elif inputMode=='q':
			validInput=True
			
		else:
			print("\ninvalid mode")
	 



	
	



if __name__=="__main__":
	main()



