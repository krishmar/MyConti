#####################################################
# 	Script for: Measuring memory of SOC and VUC.	#		
# 	Output: written to XL file						#
# 	Input files: topGrep.txt, sizes_RH850.txt		#
# 	topGrep.txt: for SOC memory						#
# 	sizes_RH850.txt: for VUC memory					#
#####################################################

import os
import re
import stat
import traceback
import sys
import xlsxwriter
import shutil

booly = False
version = []

dt1 = " "
dt2 = " "
dt3 = " "
dt4 = " "
dt5 = " "
dt6 = " "
dt7 = " "
dt8 = " "
dtR1 = " "
dtR2 = " "
dtR3 = " "
dtC1 = " "

def pharseIt():
        
    pharseFile = open('topGrep.txt', 'r')
    print "Reading file topGrep.txt"
    
    lines = pharseFile.readlines()

    for line_no, line in enumerate(lines):
    
        if "system" in line:             
            SYSline = lines[line_no-1]
            if "LEBs" in SYSline:
                socROMsystem(SYSline)
                print "System done"
                
        if "dsp2" in line:           
            dsp2line = lines[line_no-1]
            if "LEBs" in dsp2line:
                socROMdsp2(dsp2line)
                print "dsp2 done"
            
        if "uarea" in line:          
            uarealine = lines[line_no-1]
            if "LEBs" in uarealine:
                socROMuarea(uarealine)
                print "Uarea done"  
            
        elif "MemTotal:" in line:
            socRAMtotal(line)
            print "MemTotal done"
            
        elif "MemAvailable:" in line:
            socRAMavailable(line)
            print "MemAvailable done"
            
        elif "AIVC Version" in line:
            grepSWversion(line)
            print "AIVC Version done"
            
        elif "Stack Used:" in line:
            vucStack(line)
            print "MemAvailable done"
            
        elif "CPU Usage:" in line:
            cpuUsage(line)
            print "CPU Usage done"
                    
    pharseFile.close()
    
    

def getVucMemFile():

    global dt1
    
    VucMemFile = open('sizes_RH850.txt','r')
    lines = VucMemFile.readlines()
    for line in lines:
        if "Total RAM" in line:
            vucRAMsize(line)
            print "Found RAM data"
        
        if "Total Flash" in line:
            vucROMsize(line)
            print "Found Flash data"
            
            
def socROMsystem(SYSline):

    global dtR1
    
    dt = SYSline.split(" ")
    for (i, subword) in enumerate(dt):
        #print "socROMsystem: " + subword
        if (subword == 'bytes,'): 
            dtR1 = dt[i+1]
                        
    return
    
def socROMdsp2(dsp2line):

    global dtR2
    
    dt = dsp2line.split(" ")
    for (i, subword) in enumerate(dt):
        #print "socROMsystem: " + subword
        if (subword == 'bytes,'): 
            dtR2 = dt[i+1]
                        
    return
    
def socROMuarea(uarealine):

    global dtR3
    
    dt = uarealine.split(" ")
    for (i, subword) in enumerate(dt):
        #print "socROMsystem: " + subword
        if (subword == 'bytes,'):
            dtR3 = dt[i+1]
                        
    return  
    
def cpuUsage(line): 

    global dtC1
    
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        #print "socROMsystem: " + subword
        if (subword == 'Usage:'): 
            dtC1 = dt[i+1]
                        
    return  

                
                        
def grepSWversion(line):

    global dt1
    
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        #print "socROMsystem: " + subword
        if (subword == 'AIVC'): 
            dt_sub = dt[i+2]
            dt1=dt_sub[12:20]
                        
    return
                    

def vucRAMsize(line):

    global dt2
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == ':'): 
            dt2 = dt[i+1]
            
    return


def vucROMsize(line):

    global dt3
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == ':'): 
            dt3 = dt[i+1]
            
    return

def socROMsize(line):
    global dt4
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == 'ubi0:system'): 
            rawdt4 = dt[i+14]
            dt4 = rawdt4[:4]

def socRAMtotal(line):
    global dt5
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == '->'): 
            dt5 = dt[i+7]

def socRAMavailable(line):
    global dt6
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == '->'): 
            dt6 = dt[i+7]
    
def vucStack(line): 
    global dt7
    global dt8
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == 'Used:'): 
            dt7 = dt[i+1]
    for (i, subword) in enumerate(dt):
        if (subword == 'Free:'): 
            dt8 = dt[i+1]
            
def moveFilesToServer():

    workingPath = os.getcwd()
    
    os.chdir(workingPath)
    
    Sfile1 = workingPath + '/topGrep.txt'
    Sfilemod1 = workingPath + '/topGrep_'+ dt1 +'.txt'
    
    os.rename(Sfile1, Sfilemod1)
    
    ## \\IGDB001\didc0126\09_SW_Others\9999_Integration_Team\KPI_Measurement\03_Script files\01_getMemoryMeasure
    
    grepFileLocation = Sfilemod1
    memXlsxFileLocation = workingPath + '/Memory Measure_'+ dt1 +'.xlsx'
    targetDirLocation = '//IGDB001'+'/'+ 'didc0126'+'/'+'09_SW_Others'+'/'+'9999_Integration_Team'+'/'+'KPI_Measurement'+'/'+'Memory_Measurement_Files'
    
    moveToLocation = workingPath + '/' + 'Memory_Measurement_Files'
        
    shutil.copy(grepFileLocation, targetDirLocation)
    shutil.copy(memXlsxFileLocation, targetDirLocation)
    
    shutil.move(grepFileLocation, moveToLocation)
    shutil.move(memXlsxFileLocation, moveToLocation)
    

    
        
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
    

def copy2XL():

    workbook = xlsxwriter.Workbook('Memory Measure_'+dt1+'.xlsx')
    worksheet = workbook.add_worksheet(dt1)
    
    worksheet.set_column('G:G', 15)
    
    worksheet.write('A1', 'Measurement details of SW '+dt1)
    worksheet.write('G3', 'SOC ROM')
    
    worksheet.write('G4', 'System:') # socROMdsp2
    worksheet.write('G5', 'Dsp2:')
    worksheet.write('G6', 'Uarea:')
    
    worksheet.write('G8', 'SOC RAM')
    worksheet.write('G8', 'Total:') # socRAMtotal
    worksheet.write('G10', 'Avialable:') #socRAMavailable
    
    worksheet.write('G12', 'VUC Mem')   
    worksheet.write('G13', 'Total RAM')#vucRAM  
    worksheet.write('G14', 'Total Flash')#vucFlash
    
    worksheet.write('G16', 'VUC Stack')
    worksheet.write('G17', 'Used')#stackUsed
    worksheet.write('G18', 'Free')#stackFree
    
        
    worksheet.write('H4', dtR1) # socROM
    worksheet.write('H5', dtR2) # socRAMtotal
    worksheet.write('H6', dtR3) #socRAMavailable
    
    worksheet.write('H8', '163684') # socRAMtotal
    worksheet.write('H10', dt6) #socRAMavailable
    
    worksheet.write('H13', dt2)#vucRAM  
    worksheet.write('H14', dt3)#vucFlash
    
    worksheet.write('H17', dt7)#stackUsed
    worksheet.write('H18', dt8)#stackFree
    
    worksheet.write('B5','ROM') # socROM
    worksheet.write('B6','RAM') # socRAMtotal
    worksheet.write('B7','Stack') #socRAMavailable
    
    worksheet.write('C4', 'Soc')#vucRAM 
    worksheet.write('D4', 'VuC')#vucFlash
    
    worksheet.write('B11', 'CPU U:')#vucRAM 
    worksheet.write('C11', dtC1+'%')#vucRAM
        
    percent_format = workbook.add_format({'num_format': '0.00%'}) 
            
    worksheet.write('C5','=(H4+H5)/H6', percent_format)
    worksheet.write('C6','=1-(H10/H8)', percent_format)
    worksheet.write('C7','=C6', percent_format)
    
    worksheet.write('D5','=(H14/1024)/(1.5*1024-128-128)', percent_format)
    worksheet.write('D6','=(H13/1024)/(128-8-0.75)', percent_format)
    worksheet.write('D7','=H17/(H17+H18)', percent_format)  
           
    workbook.close()
        

try:
    
    workingPath = os.getcwd()

    pharseIt()
    
    getVucMemFile()
    
    os.chdir(workingPath)
        
    copy2XL()
    
    moveFilesToServer()

       
except:
    e = traceback.format_exc()
    #print e
    errorSequence()

finally:
    print "Operation completed. Bye!"
    


__CreatedBy__ = 'Krishnan Senthil Kumar: UIDk9245'
__CreatedOn__ = '09/06/17'
