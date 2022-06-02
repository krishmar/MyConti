#####################################################
#   Script for: Get list of the commints in the     #            
#               given baseline version input        #   
#   Output: change-summary_SOC/VUC_SW_ver.txt       #
#   Input: Sofware baseline version                 #
#####################################################


import os
import sys
import shutil

i=0
printList=[]

currentWD = os.getcwd()

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
    
socPath = "\\" + aivcSOC + swVer +  "\\" + "docs"
vucPath = "\\" + aivcVUC + swVer + "-C38" + "\\" + "docs"
    
socDOCpath = basePath + aivcPath + verPath + socPath
vucDOCpath = basePath + aivcPath + verPath + vucPath
qryDOCpath = basePath + aivcPath + verPath + "\\" +"aivc_test_reports"  

socFile = socDOCpath + "\\" + "change-summary.txt"
vucFile = vucDOCpath + "\\" + "change-summary.txt"

SocVerFile = "change-summary" + "_SOC_" + swVer + ".txt"
VucVerFile = "change-summary" + "_VUC_" + swVer + ".txt"
CSfile = "change-summary.txt"

shutil.copy(socFile, currentWD)
os.rename(CSfile,SocVerFile)
shutil.copy(vucFile, currentWD)
os.rename(CSfile,VucVerFile)

def errorSequence():
    """
    This method is created as an error handling method.
    It prevents the screen from shutting down immediately after the script is run.

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
