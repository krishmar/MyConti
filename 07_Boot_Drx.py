#####################################################
#   Script for: Measure timing for DRX Power ON     #       
#   Output: written to XL file                      #
#   Input files: messages_Drx_1,                #
#       messages_Drx_2 & messages_Drx_3             #
#####################################################

import os
import re
import stat
import traceback
import sys
import xlsxwriter

booly = False
version = []

start_t = " "
USB_t = " "
netReg_t = " "
IPCrdy_t = " "
dataCon_t = " "
MQTT_t = " "

first_occur_f1 = 0
first_occur_f2 = 0

currentFile = " "


def pharseIt():
    """
    This method modifies the version number details in app_version.h.
    """
    # global first_occur_f2
    # first_occur_f2 = 0
    # workbook = xlsxwriter.Workbook('Dtx.xlsx')
    # worksheet = workbook.add_worksheet()
    
    #global currentFile
    
    print "Indide pharesIt Loop: "+ currentFile
    
    pharseFile = open(currentFile, 'r')
    print "File Open for reading"
    lines = pharseFile.readlines()
    for line in lines:
    
        if "gic_show_resume_irq" in line:
            start_line(line)

        elif "USB channel diag connected" in line:
            USB_Done(line)

        elif "Modem registered" in line:
            net_registered(line)

        elif "IPC link established" in line:
            IPC_ready(line)

        elif "Current State - [CNM_DATACALL_CONNECTED]" in line:
            Data_connection_done(line)

        elif "SSL handshake done write:" in line:
            MQTT_done(line)

            
    pharseFile.close()

def start_line(line):   
    global start_t
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == 'aivc2'): 
            start_t = dt[i-1]
        
    return
                        
                

def USB_Done(line):

    global USB_t
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == 'aivc2'): 
            USB_t = dt[i-1]
                
    return
        
        
def net_registered(line):

    global netReg_t
    global first_occur_f2
    
    if first_occur_f2 == 0:
        dt = line.split(" ")
        for (i, subword) in enumerate(dt):
            if (subword == 'aivc2'): 
                netReg_t = dt[i-1]
        first_occur_f2 = 1
            
    return

def IPC_ready(line):

    global IPCrdy_t
        
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == 'aivc2'): 
            IPCrdy_t = dt[i-1]
            
    return

def Data_connection_done(line):

    global dataCon_t
    
    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == 'aivc'): 
            dataCon_t = dt[i-1]
                
    return

def MQTT_done(line):

    global MQTT_t

    dt = line.split(" ")
    for (i, subword) in enumerate(dt):
        if (subword == 'aivc2'): 
            MQTT_t = dt[i-1]
            
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

    global currentFile
    global first_occur_f2
    

                    
    workbook = xlsxwriter.Workbook('Dtx.xlsx')

    worksheet = workbook.add_worksheet()
    
    cell_format02 = workbook.add_format()
    cell_format02.set_num_format('##0')
    
    cell_format01 = workbook.add_format()
    cell_format01.set_align('vcenter')
    
    worksheet.set_column('A:A', 15)
    
    worksheet.write('B1', 'Time')
                
    worksheet.write('A2', 'USB Enumration:')
    worksheet.write('A3', 'DAL')
    worksheet.write('A4', 'Net Registered:')
    worksheet.write('A5', 'IPC Ready:')
    worksheet.write('A6', 'Data Connection:')   
    worksheet.write('A7', 'MQTT Done:')
    
    worksheet.write('A9', 'Start_t:')
        
    worksheet.write('A13', 'USB_t:')
    worksheet.write('A14', 'USB_t:')
    worksheet.write('A15', 'netReg_t:')
    worksheet.write('A16', 'IPCrdy_t:') 
    worksheet.write('A17', 'dataCon_t:')
    worksheet.write('A18', 'MQTT_t:')
    
    worksheet.write('L1', 'Data1') 
    worksheet.write('M1', 'Data2')
    worksheet.write('N1', 'Data3')
    worksheet.write('O1', 'Result') 
    
    for i in range(1,4,1):
    
        if (i == 1):
            currentFile = 'messages_Drx_1'
            first_occur_f2 = 0
            pharseIt()
            
            worksheet.write('B9', start_t)
            
            worksheet.write('B13', USB_t)
            worksheet.write('B14', IPCrdy_t)
            worksheet.write('B15', netReg_t)
            worksheet.write('B16', IPCrdy_t)
            worksheet.write('B17', dataCon_t)
            worksheet.write('B18', MQTT_t)
            
            worksheet.write('B2', '=TEXT(B13-B9,"h:mm:ss")')
            worksheet.write('B3', '=TEXT(B14-B9,"h:mm:ss")')
            worksheet.write('B4', '=TEXT(B15-B9,"h:mm:ss")')    
            worksheet.write('B5', '=TEXT(B16-B9,"h:mm:ss")')
            worksheet.write('B6', '=TEXT(B17-B9,"h:mm:ss")')    
            worksheet.write('B7', '=TEXT(B18-B9,"h:mm:ss")')
            
            worksheet.write('C2', '= RIGHT(B2,2)')
            worksheet.write('C3', '= RIGHT(B3,2)')
            worksheet.write('C4', '= RIGHT(B4,2)')
            worksheet.write('C5', '= RIGHT(B5,2)')   
            worksheet.write('C6', '= RIGHT(B6,2)')
            worksheet.write('C7', '= RIGHT(B7,2)')
                       
            worksheet.write('D2', '=INT(C2)')
            worksheet.write('D3', '=INT(C3)')
            worksheet.write('D4', '=INT(C4)')
            worksheet.write('D5', '=INT(C5)')   
            worksheet.write('D6', '=INT(C6)')
            worksheet.write('D7', '=INT(C7)')
            
            print "Completed file one"

        if (i == 2):
            currentFile = 'messages_Drx_2'
            first_occur_f2 = 0
            pharseIt() 
            
            worksheet.write('E9', start_t)
            
            worksheet.write('E13', USB_t)
            worksheet.write('E14', IPCrdy_t)
            worksheet.write('E15', netReg_t)
            worksheet.write('E16', IPCrdy_t)
            worksheet.write('E17', dataCon_t)
            worksheet.write('E18', MQTT_t)
            
            worksheet.write('E2', '=TEXT(E13-E9,"h:mm:ss")')
            worksheet.write('E3', '=TEXT(E14-E9,"h:mm:ss")')
            worksheet.write('E4', '=TEXT(E15-E9,"h:mm:ss")')    
            worksheet.write('E5', '=TEXT(E16-E9,"h:mm:ss")')
            worksheet.write('E6', '=TEXT(E17-E9,"h:mm:ss")')    
            worksheet.write('E7', '=TEXT(E18-E9,"h:mm:ss")')
            
            worksheet.write('F2', '= RIGHT(E2,2)')
            worksheet.write('F3', '= RIGHT(E3,2)')
            worksheet.write('F4', '= RIGHT(E4,2)')
            worksheet.write('F5', '= RIGHT(E5,2)')   
            worksheet.write('F6', '= RIGHT(E6,2)')
            worksheet.write('F7', '= RIGHT(E7,2)')      
        
            worksheet.write('G2', '=INT(F2)')
            worksheet.write('G3', '=INT(F3)')
            worksheet.write('G4', '=INT(F4)')
            worksheet.write('G5', '=INT(F5)')   
            worksheet.write('G6', '=INT(F6)')
            worksheet.write('G7', '=INT(F7)')
            
            print "Completed file Two"
            
        if (i == 3):
            currentFile = 'messages_Drx_3'
            first_occur_f2 = 0
            pharseIt()
            
            print "Started file three"
            
            worksheet.write('H9', start_t)
        
            worksheet.write('H13', USB_t)
            worksheet.write('H14', IPCrdy_t)
            worksheet.write('H15', netReg_t)
            worksheet.write('H16', IPCrdy_t)
            worksheet.write('H17', dataCon_t)
            worksheet.write('H18', MQTT_t)
            
            worksheet.write('H2', '=TEXT(H13-H9,"h:mm:ss")')
            worksheet.write('H3', '=TEXT(H14-H9,"h:mm:ss")')
            worksheet.write('H4', '=TEXT(H15-H9,"h:mm:ss")')    
            worksheet.write('H5', '=TEXT(H16-H9,"h:mm:ss")')
            worksheet.write('H6', '=TEXT(H17-H9,"h:mm:ss")')    
            worksheet.write('H7', '=TEXT(H18-H9,"h:mm:ss")')
            
            worksheet.write('I2', '= RIGHT(H2,2)')
            worksheet.write('I3', '= RIGHT(H3,2)')
            worksheet.write('I4', '= RIGHT(H4,2)')
            worksheet.write('I5', '= RIGHT(H5,2)')   
            worksheet.write('I6', '= RIGHT(H6,2)')
            worksheet.write('I7', '= RIGHT(H7,2)')   

    
            worksheet.write('J2', '=INT(I2)')
            worksheet.write('J3', '=INT(I3)')
            worksheet.write('J4', '=INT(I4)')
            worksheet.write('J5', '=INT(I5)')   
            worksheet.write('J6', '=INT(I6)')
            worksheet.write('J7', '=INT(I7)')
            
            print "Completed file Three"
            
        i = +1
        
    print "Completed all files"
        
    worksheet.write('L2', '=D2')
    worksheet.write('L3', '=D3')
    worksheet.write('L4', '=D4')
    worksheet.write('L5', '=D5')   
    worksheet.write('L6', '=D6')
    worksheet.write('L7', '=D7')
    
    worksheet.write('M2', '=G2')
    worksheet.write('M3', '=G3')
    worksheet.write('M4', '=G4')
    worksheet.write('M5', '=G5')   
    worksheet.write('M6', '=G6')
    worksheet.write('M7', '=G7')
    
    worksheet.write('N2', '=J2')
    worksheet.write('N3', '=J3')
    worksheet.write('N4', '=J4')
    worksheet.write('N5', '=J5')   
    worksheet.write('N6', '=J6')
    worksheet.write('N7', '=J7')
    
    
    
    worksheet.write('O2', '=AVERAGE(L2:N2)',cell_format02 )
    worksheet.write('O3', '=AVERAGE(L3:N3)',cell_format02 )
    worksheet.write('O4', '=AVERAGE(L4:N4)',cell_format02 )
    worksheet.write('O5', '=AVERAGE(L5:N5)',cell_format02 )   
    worksheet.write('O6', '=AVERAGE(L6:N6)',cell_format02 )
    worksheet.write('O7', '=AVERAGE(L7:N7)',cell_format02 )
 
    workbook.close()
    
    

try:

    # pharseIt()
    
    copy2XL()
        
    print  "USB_t:   " + "\t" + USB_t 
    print  "netReg_t:" + "\t" + netReg_t
    print  "IPCrdy_t:" + "\t" + IPCrdy_t
    print  "dataCon_t:"+ "\t" + dataCon_t
    print  "MQTT_t:  " + "\t" + MQTT_t

    
    
except:
    e = traceback.format_exc()
    print e
    errorSequence()

finally:
    print "Operation completed. Bye!"
    

__CreatedBy__ = 'Krishnan Senthil Kumar: UIDk9245'
__CreatedOn__ = '09/06/17'
