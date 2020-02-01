#####################################################
# 	Script for: Get information of all commits 		#			 
#				in a confluence page 				#	
# 	Output: XL file with details of commit			#
# 	Input files: Confluence page ID    				#
#####################################################


import os
import urllib3
from bs4 import BeautifulSoup
from datetime import datetime
from cmlib.confluence.query import Query as Confluence_Query
import xlsxwriter


row=1

workbook = xlsxwriter.Workbook('Commit details.xlsx')
worksheet = workbook.add_worksheet()

def get_pageID(title_Wk):
    
    i=0
    title_SW = ""
    title_end = ["CAN, CUD, NON-FOTA, R.Serv, R.Diag",
                "Connectivity & Geofence",
                "Diagnostics",
                "Ecall & Xcall & Audio",
                "Platform Patches",
                "RAS, DCM & Security",
                "SW reprogramming",
                "System",
                "UCD & DAL",
                "VuC & CAN"]

    query = Confluence_Query()
    
    for title in title_end:
        title_full = str(title_Wk + "" + title_SW +  " " + title_end[i])
        print("title_full: " + title_full)
        pages = query.search(title = title_full)
        for page in pages.results:
            page_id = page.id
            # print("page_id : " + page_id)
            get_commit(page_id,title_full)
        i=i+1

def get_commit(page_id,title_full):

    global row
    confData = ["" ]
    count = 0 

    http = urllib3.PoolManager()
    url = "http://buic-confluence:8090/pages/viewpage.action?pageId=" + page_id
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data,"html.parser")

    data1 = soup.select('tr a')
    title = "Commits in Page: " + '" ' + title_full + ' "'
    print(title)
    print('"""""""""""""""""""""""""""""""""""""""""""""""""""""""""')
    print('\n')
    for data2 in data1:
        data3 = data2.getText()
        
        if(count == 0):
           row += 1     
           worksheet.write(row,0, title)
           row += 1
           count = count+1
        #print("confData: " + confData)
        if (data3[:6] == "https:"):
            print(data3)
            worksheet.write(row,1, data3)
            row += 1


titleWeek = ["Wk 18.2",
"Wk 18.4",
"Wk 18.5",
"Wk 19.1",
"Wk 19.2",
"Wk 19.4"]

for week in titleWeek:
    title_Wk = week
    row += 2
    mainTitle = "Following are results for " + week
    worksheet.write(row,0, mainTitle)
    row += 1
    get_pageID(title_Wk)
    

workbook.close()

