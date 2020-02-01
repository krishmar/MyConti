#####################################################
# 	Script for: Creating ATF file from given XL		#			 
#				file and related ATF files			#	
# 	Output: Create package for upload				#
# 	Input files: logFileVuc.txt, Book1.xlsx			#
#####################################################

import os
import sys
import openpyxl
import subprocess
from shutil import copyfile

import stat
import traceback

import shlex

cmd = "cmd"


fileToCopy = ' '

logFileVuc = open('D://logFileVuc.txt', 'w+')

filepath = (os.getcwd())[3:]

def readFiles():
    path = '.'
    global fileToCopy
    # print("Inside readfiles module")
    for filename in os.listdir(path):
        # print("We are testing file:" + filename)
        fileToCopy = filename
        if filename.endswith(".atf"):
            print("We are testing file:" + filename)
            pharseFile = open(filename, 'r')
            lines = pharseFile.readlines()
            for line in lines:
                if "REGION" in line:
                    # print("exiting readfiles module")
                    findVariant(line)


def findVariant(line):
    for (i,char) in enumerate(line):
        if char == '"':
            AtfRegion = line[int(i+1):-2]
            checkXL(AtfRegion)
            break
            print(AtfRegion)
            


def checkXL(AtfRegion):
    global fileToCopy
    
    wb = openpyxl.load_workbook('Book1.xlsx')
    sheet = wb.get_sheet_by_name('DocMatBOM')
    
    if AtfRegion[-4:] == '_DEV':
        verifyRegion = AtfRegion
    else:
        verifyRegion = AtfRegion + '_PROD'
    
    for i in range(1,72):
        val='J'+str(i)
        prefVal = 'D'+str(i)
        sufVal = 'K'+str(i)
        c = sheet[str(val)]
        region = c.value
     

        if (region):
            if (region[:3]) == 'atf':
                xlRegion = region[4:]
                if (xlRegion == verifyRegion):
                    d = sheet[str(prefVal)]
                    fil = d.value
                    k = sheet[str(sufVal)]
                    end = k.value
                    file7z = fil + '_FIL_900_' + end
                    print("Finished verifying" + fileToCopy)
                    create7z(file7z)
                    break

        

def errorSequence():
    boolean = False
    while boolean == False:
        inPut = raw_input("Script did not run in completion. Enter UID to exit:")
        boolean = True                      
                    
                
def create7z(file7z):
    
    global fileToCopy
    global logFileVuc
    global filepath 
    
    
    p = subprocess.Popen(shlex.split(cmd), shell = True, stdin = subprocess.PIPE, stderr = subprocess.STDOUT,
                         stdout = logFileVuc)
                         
    os.getcwd()
    p.communicate(

        'd:\n' +
        'cd ' + filepath + '\n' +
        '7z ' + 'a ' + file7z + '.7z '+  fileToCopy + '\n'
        )
    print("Finished creating" + fileToCopy)
    
"""
Format to Zip a file
7z a <outputFileName> <inputFileName>

Format to zip a folder
7z a <outputFolderName> ./<inputfolderName>/*
   
"""   
    
    

try:
    
    #print("start")
    readFiles()
    
        
except:
    e = traceback.format_exc()
    print(e)
    errorSequence()

finally:
    print("Operation completed. Bye!")     