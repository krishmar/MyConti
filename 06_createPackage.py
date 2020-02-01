#####################################################
# 	Script for: Creating binary pacakge to upload 	#			 
#				with given list in text file		#	
# 	Output: Create package for upload				#
# 	Input : Text file with list of bianries			#
#####################################################

import os
import subprocess
import shlex
import string
from shutil import copyfile

#''''''''''''''''''''''''''''''''
# Create directory DEVEL and PROD
# ''''''''''''''''''''''''''''''''

path = os.getcwd()
os.chdir(path)

if not os.path.isdir('DEVEL'):
    os.mkdir('DEVEL')
if not os.path.isdir('PROD'):    
    os.mkdir('PROD')
    
develPath = path + "\\"+"DEVEL"
prodPath = path + "\\"+"PROD"

workingPath = ' '

targetPath = develPath # default path is devel path

logFileVuc = open("logFileVuc.txt","w+")    

cmd = 'cmd'

pharseFile = open('file_list.txt', 'r')
print("Reading file file_list.txt")
    
lines = pharseFile.readlines()


def create7z(file7z,filePath):

    global targetPath
    #target = targetPath
    
    zipFile = file7z + '.7z '
    
    p = subprocess.Popen(shlex.split(cmd), shell = True, stdin = subprocess.PIPE, stderr = subprocess.STDOUT,
                         stdout = logFileVuc)
                         
    #os.getcwd()
    p.communicate(

        #'d:\n' +
        'cd ' + filePath + '\n' +
        '7z ' + 'a ' + file7z + '.7z '+  file7z + '\n'
        
        # move *.7z targetPath
            
        )
       
    if (p.wait() == 0):
        moveFiles(zipFile)
            
                       
def moveFiles(zipFile):

    global targetpath
    
    fromPath = workingPath + zipFile
        
    shutil.move(fromPath, targetpath)
   
for folderName, subfolders, filenames in os.walk(path):
##   #print('The current folder is ' + folderName)
    #filePath = os.getcwd()
    for subfolder in subfolders:
        #data1 = str(subfolder)
        
        data1 = str.strip(subfolder)
        #print("The sub folder is: " + data1)
        for line in lines:
            #data2 = str(line)
            data2 = str.strip(line)
            
            if(data2 == data1):
                print(data2[:4])
                if((data2[:4]) == "prod"):
                    tagetPath = prodPath
                if((data2[:7]) == "bannerup"):
                    if((data2[8:4]) == "prod"):
                        tagetPath = prodPath
                workingPath = folderName
                #print("This line is from file_list: " + data2)
                #Detection of whether is production file
                print("############################################")
                print("Yes found dir : " + line)
                print("############################################")
                print(folderName)
                filePath = os.getcwd()
                print(filePath)
                create7z(subfolder,folderName)

                
  
print("Finished creating Zip file")
