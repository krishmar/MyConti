#####################################################
# 	Script for: Plot data contents in log file		#			 
#				to an XL file						#	
# 	Output: Plot in XL file							#
# 	Input files: sysTrack.txt						#
#####################################################

import os
import re
import stat
import traceback
import sys
import xlsxwriter

from xlsxwriter.utility import xl_range_abs

try:
    os.remove("convert_cpu.xlsx")
    
except:
    print "something went wrong"

workbook = xlsxwriter.Workbook('Plot USS.xlsx', {'strings_to_numbers': True})
#workbook = xlsxwriter.Workbook('Plot USS.xlsx')
worksheet = workbook.add_worksheet()

#percent_format = workbook.add_format({'num_format': '0.00%'})


row=0
coloumn=0
series=0
row_track = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

time=0

pharseFile = open('sysTrack.txt', 'r')
print "File Open for reading"
lines = pharseFile.readlines()

lookFor = ['(systemd)', '(aivc-enabler)', '(aivc-commsrv)', '(aivc-lt)', '(aivc-vcsgw)',  
'(aivc-suppsrv)', '(aivc-fotaivi)', '(aivc-tcustmgr)', '(aivc-can_swl_ap)', '(aivc-gnh)',       
'(cgrulesengd)', '(conti-nadif)', '(vcs)', '(audioctrld)', '(netmgrd)',
'(location-mgrd)', '(lifecycle-mgrd)', '(qmi_cust_app_sv)', '(conti-mcm-svc)', '(time-mgrd)',    
'(swl-mgrd)', '(dbus-daemon)', '(flash-scrubd)', '(dc_ota_rb)', '(conti-apmd)',
'(rb_uad)', '(rb_engine)', '(swl_can_downloa)', '(conti-mpmc)', '(aivc_fota_updat)',
'(efs_uad)', '(qti)', '(mms)', '(redis-server)', '(HiFi)',
'(conti-psapcall)', '(qmuxd)', '(pasd)', '(adbd)', '(per_update_agen)',
'(systemd-journal)', '(diagrebootapp)', '(systemd-udevd)', '(connmand)',
'(auditd)', '(dnsmasq)', '(atfwd_daemon)', '(systemd-logind)','(sh)',
'(dc_interface)', '(memory_10mins.s)', '(agetty)', '(syslogd)', '(klogd)',
'(pers_db_create.)', '(dc_start)', '(tail)', '(reboot-daemon)']


for i in lookFor:
    worksheet.write(0, coloumn, i)
    coloumn += 1



for line in lines:
    for i in lookFor:
        if i in line:
            dt = line.split(" ")
            coloumn = lookFor.index(i)
            for (i, subword) in enumerate(dt):
                if (subword == ':'+'\t'+'PSS'):
                    dt1 = dt[i+6]
                    # print dt1
                    dt2 = int(dt1[:-8])
                    dt3 = float(dt2/163676.0)*100
                    dt4 = format(dt3, '.2f')
                    worksheet.write(row_track[coloumn], coloumn, dt4)
            row_track[coloumn] +=1   


# Create a new chart object.
chart = workbook.add_chart({'type': 'line'})

# Add a series to the chart.
    
for c in range(0,45):
    cell_range = xl_range_abs(0, c, 45, c)
    
    chart.add_series({'values': '=Sheet1!'+cell_range+'',
            'name': ['Sheet1', 0, c],
                })
				
chart.set_title ({'name': 'Results of Memory Usage'})
chart.set_x_axis({'name': 'Time Period'})
chart.set_y_axis({'name': 'Memory Usage (%)'})				

worksheet.insert_chart('C1', chart)
       
pharseFile.close()

workbook.close()

