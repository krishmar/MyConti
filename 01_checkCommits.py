#####################################################
# 	Script for: Check for matching commits before	#			 
#				and after build finish				#	
# 	Output: Result output in "commitReport.txt"		#
# 	Input files: DI_Query.txt						#
#####################################################



import os
import sys

i=0
printList=[]

verPath = str(sys.argv[1])
basePath = ("\\"+"\\" + "IGDB001" + "\\" + "didc0126" + "\\" + "13_SW_Baselines")

if (verPath[:5] == "AIVC_"):
	aivcPath = ("\\" + "03_BaselineReleases" + "\\")
	swVer = verPath[5:]
	aivcSOC = "aivc-soc-"
	aivcVUC = "aivc-vuc-"
elif (verPath[:5] == "AIVC2"):
	aivcPath = ("\\" + "07_SOP2Releases" + "\\")
	swVer = verPath[6:]
	aivcSOC = "aivc2-soc-"
	aivcVUC = "aivc2-vuc-"	
elif (verPath[:5] == "AIVC3"):
	aivcPath = ("\\" + "11_SOP3Releases" + "\\")
	swVer = verPath[6:]
	aivcSOC = "aivc3-soc-"
	aivcVUC = "aivc3-vuc-"
	
socPath = "\\" + aivcSOC + swVer +	"\\" + "docs"
vucPath = "\\" + aivcVUC + swVer + "-C38" + "\\" + "docs"
	
socDOCpath = basePath + aivcPath + verPath + socPath
vucDOCpath = basePath + aivcPath + verPath + vucPath
qryDOCpath = basePath + aivcPath + verPath + "\\" +"aivc_test_reports"	

socFile = socDOCpath + "\\" + "change-log.txt"
vucFile = vucDOCpath + "\\" + "change-log.txt"
commitFile = qryDOCpath + "\\" + "DI_Query.txt"
#reportFile = qryDOCpath + "\\" + "DI_Query.txt"

reportFile = open((qryDOCpath + "\\" + "commitReport.txt"),"w+")

pharseFile1 = open(commitFile, 'r')
DI_lines = pharseFile1.readlines()

pharseFile2 = open(socFile, 'r')
SOC_lines = pharseFile2.readlines()
 
pharseFile3 = open(vucFile, 'r')
VUC_lines = pharseFile3.readlines()

print(" ")

reportFile.write(" \n")
reportFile.write("####v########e########e########r##########a##########a####\n")
reportFile.write("    Creating commit report for build: " + verPath+"       \n")
reportFile.write("####v########e########e########r##########a##########a####\n")
reportFile.write(" \n")

for line in DI_lines:
	chk_DI_Lines = DI_lines[i]
	trackFlag = 0
	
	for line in VUC_lines:
		if chk_DI_Lines in line:
			reportFile.write("Found commit: " +  chk_DI_Lines +  "in file name: 'change-log.txt' for VUC @ line: "+ line+"\n")
			print("Found commit: " +  chk_DI_Lines +  "in file name: 'change-summary_VUC.txt' @ line: "+ line)
			trackFlag = 1
			break
			
	if (trackFlag == 0):
		for line in SOC_lines:
			if chk_DI_Lines in line:
				print("Found commit: " +  chk_DI_Lines +  "in file name: 'change-log.txt' for SOC @ line: "+ line)
				reportFile.write("Found commit: " +  chk_DI_Lines +  "in file name: 'change-summary_SOC.txt' @ line: "+ line+"\n")
				trackFlag = 1
				break
	
	if (trackFlag == 0):
		printList.append(chk_DI_Lines)
		trackFlag = 1
				
	i = i+1			
	
for list in printList: 
	print("########################### Aiyooo!!! Masala ###########################")
	reportFile.write("########################### Aiyooo!!! Masala ###########################"+"\n")
	print("cannot find commit :" + list)
	reportFile.write("cannot find commit :" + list + "\n")

pharseFile1.close()
pharseFile2.close()
pharseFile3.close()
reportFile.close()

def errorSequence():
	"""
	This method is created as an error handling method.
	It prevents the screen from shutting down immediately after the script is run.
	It prompts for an input that has to start with UID followed by any letter from [A-Z] followed by any 4 digits from [0-9].
	"""

	boolean = False
	while boolean == False:
		inPut = raw_input("Script did not run in completion. Enter UID to exit:")
		boolean = True		


try:
   
	print(" ")

		
except:
	e = traceback.format_exc()
	print e
	errorSequence()

finally:
	print(" ")
	print "Operation completed. Bye!"
	
  

__CreatedBy__ = 'Krishnan Senthil Kumar: UIDk9245'
__CreatedOn__ = '28/11/19'