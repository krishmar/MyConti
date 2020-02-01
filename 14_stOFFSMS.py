#####################################################
# 	Script for: Measure timing for stOFFSMS state	#		
# 	Output: written to XL file						#
# 	Input files: VUC stOFFSMS.txt					#
#####################################################

import os
import re
import stat
import traceback
import sys
import xlsxwriter

booly = False
version = []

start_t = [1,1,1,1,1]
expMsg_t = [1,1,1,1,1]

nonRTC_t = " "
RTC_t = " "

first_occur_f1 = 0
first_occur_f2 = 0

s_pos = 0
e_pos = 0


# during boot time the system always reset to Jan 1 00:00:00 
# Only after loading all the initial module. Actual time is updated from
# the RTC. So all KPI measurements need to offeset this reset time.


def pharseIt():
    """
    This method modifies the version number details in app_version.h.
    """
    
    pharseFile = open('VUC stOFFSMS.txt', 'r')
    print "File Open for reading"
    lines = pharseFile.readlines()
    for line in lines:
    
        if "Cur State: StDrx, Prev State: StOffSMS" in line:
            start_point(line)

        elif "***Shutdown complete***" in line:
            targetMessage(line)
                    
    pharseFile.close()
    
                        
def start_point(line):

    global start_t
    global s_pos
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        print subword
        if (subword == '->'): 
            ds = dt[i-1]
            start_t[s_pos] = ds[0:8]
            s_pos =+1
            print "Value of start is %s"%start_t
        
    return
                    



def targetMessage(line):

    global expMsg_t
    global e_pos
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        #print subword 
        if (subword == '->'): 
            ds = dt[i-1]
            expMsg_t[e_pos] = ds[0:8]
            e_pos =+1
            #print "Value of start is %s" %expMsg_t
                
    return
        

        
def errorSequence():
    """
    This method is created as an error handling method.
    It prevents the screen from shutting down immediately after the script is run.
    It prompts for an input that has to start with UID followed by any letter from [A-Z] followed by any 4 digits from [0-9].
    """

    boolean = False
    while boolean == False:
        inPut = raw_input("Script did not run in completion. Enter UID to exit:")
        # matchObj = re.match('UID[A-Z]\d{4}', inPut, re.M | re.I)
        # if matchObj:
        boolean = True      
    

def copy2XL():
                    
    workbook = xlsxwriter.Workbook('stOFFSMS_multi_Timing.xlsx')
    worksheet = workbook.add_worksheet()
    
    worksheet.set_column('A:A', 15)
    
    worksheet.write('B1', 'Time1')
    worksheet.write('E1', 'Time2')
    worksheet.write('H1', 'Time3')
    
    worksheet.write('A2', 'Start_t:')

    worksheet.write('A7', 'Expect Msg_t:')
    worksheet.write('A9', 'Expt Timing_t:')
    
    worksheet.write('L1', 'Data1')
    worksheet.write('M1', 'Data2')
    worksheet.write('N1', 'Data3')
    worksheet.write('O1', 'Result')
    
    worksheet.write('B2', start_t[0])
    worksheet.write('E2', start_t[1])
    worksheet.write('H2', start_t[2])
    
    worksheet.write('B7', expMsg_t[0])
    worksheet.write('E7', expMsg_t[1])
    worksheet.write('H7', expMsg_t[2])
    
    worksheet.write('B9', '=TEXT((B7-B2),"h:mm:ss")')
    worksheet.write('E9', '=TEXT((E7-E2),"h:mm:ss")')
    worksheet.write('H9', '=TEXT((H7-H2),"h:mm:ss")')
    
    worksheet.write('C2', '=RIGHT(B9,2)')
    worksheet.write('F2', '=RIGHT(E9,2)')
    worksheet.write('I2', '=RIGHT(H9,2)')
    
    worksheet.write('D2', '=INT(C2)')
    worksheet.write('G2', '=INT(F2)')
    worksheet.write('J2', '=INT(I2)')
    
    worksheet.write('L2', '=D2')
    worksheet.write('M2', '=G2')
    worksheet.write('N2', '=J2')
    worksheet.write('O2', '=AVERAGE(D2:J2)')    
    
    
    workbook.close()
        


try:

    pharseIt()
    
    copy2XL()
    
    
    print  "start_t1: %s  " %start_t[0]
    print  "expMsg_t1: %s " %expMsg_t[0]
    
    print  "start_t2: %s  " %start_t[1]
    print  "expMsg_t2: %s " %expMsg_t[1]
    
    print  "start_t3: %s  " %start_t[2]
    print  "expMsg_t3: %s " %expMsg_t[2]

        
except:
    e = traceback.format_exc()
    print e
    errorSequence()

finally:
    print "Operation completed. Bye!"
    


__CreatedBy__ = 'Krishnan Senthil Kumar: UIDk9245'
__CreatedOn__ = '09/06/17'
