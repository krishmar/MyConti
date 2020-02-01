#####################################################
# 	Script for: Creating a confluence page with		#	
#					given template					#
# 	Output: Create a confluence page				#
# 	Input: Page ID 									#
#####################################################

import re
import sys
import copy
from datetime import datetime
import pandas as pd
import time

from cmlib.confluence.util import get_url_from_page_name
from cmlib.confluence.query import Query as Confluence_Query
from cmlib.util import util


temp = ""
todayis = str(datetime.today().strftime('%Y-%m-%d'))
util.header2('Generate HTML report')

# html_content = 'D:\00_Confluence_create\generic_template.html'

#
# Confluence connection
#
query = Confluence_Query()

#page_id = 120982526
# page_id = 97608699 orginal

page_id = 82368286

parent_id = " "

parent_template = '''
	<table class="wrapped"><colgroup><col /></colgroup>
	<tbody>
	<tr>
	<th>Personnel's to be informed</th></tr>
	<tr>
	<td>
	<div class="content-wrapper">
	<ol>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d0157fb3b42b624ba" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbeb813f3" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbdd4120a" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbeb613a2" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01569df787866f37" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d0157fb3b42b624b7" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbdd51236" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="2c938082607eaa150161df753218006c" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cc09b1768" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="2c9380825f4ebcd0015fc2c2a63e0023" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="2c9380825f4ebcd001606d4df00e0058" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbeb813d1" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbdd61252" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbfc315e6" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbf5b14f5" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cc02c165d" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cc0d517b1" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cc06716fd" /></ac:link></li>
	<li><ac:link><ri:user ri:userkey="8a3312ed55df132d01562c2cbff41618" /></ac:link></li></ol></div></td></tr></tbody></table>
	<h2><br />Delivery for the day&nbsp;<span style="color: rgb(0,0,255);"><strong><br /></strong></span></h2>
	<ul>
	<li>
	<h3>Delivery for the day&nbsp; -&nbsp;<span style="color: rgb(0,128,0);">DI APPROVED &amp; REVIEWED by&nbsp; :&nbsp; ANDY / Lorriane&nbsp;</span><span style="color: rgb(0,0,255);"><strong><br /></strong></span></h3>
	<ul>
	<li>
	<h3><span style="color: rgb(0,0,255);">S<strong>OP1 - aivc-sw1272-rel<span style="color: rgb(255,0,0);">&nbsp;</span>Branch - AIVC_01.12.15.05</strong>&nbsp;(&nbsp;otp-mdm-9x28-aivc-2.30.31.0&nbsp;- TVIP_VUC_V01.30.02)</span></h3>
	<h3>&nbsp;&nbsp;<span style="color: rgb(255,0,0);">(POs need to update the respective child pages with the full description of commits with PR numbers)</span></h3></li></ul></li></ul>
	'''

	
mainPage_title = "2012-11-29 Wk47.1 Delivery Inspection Meeting"
query.create_page(ancestors_id=page_id, title=mainPage_title, value=parent_template)

##time.sleep(3)
##
##query = Confluence_Query()
##
##pages = query.search(title = mainPage_title)
##for page in pages.results:
##    parent_id = page.id
##    print("parent_id :" + parent_id)


child_template = '''
	<h1 class="with-breadcrumbs">Discussion items</h1>
	<p><br /></p>
	<table class="relative-table wrapped" style="width: 99.94%;">
	<thead>
	<tr>
	<th>
	<p>Domain/ FO</p></th>
	<th>
	<p>Planned Delivery / PR / CR / FT / Commit link</p></th>
	<th>
	<p>Dependency to other modules?</p></th>
	<th colspan="1">
	<p>Testing Status</p></th>
	<th colspan="1">
	<p>PR numbers</p></th>
	<th colspan="1"><span><span>VUC/Boot/EFS - NSSU</span><br /><span>System/DSP2 - SSU</span><br /></span></th>
	<th colspan="1"><span>Reviewed By</span></th></tr>
	<tr>
	<td colspan="1"><br /></td>
	<td colspan="1"><br /></td>
	<td colspan="1"><br /></td>
	<td colspan="1"><br /></td>
	<td colspan="1"><br /></td>
	<td colspan="1"><br /></td>
	<td colspan="1"><br /></td></tr></thead></table>
	<p><br /></p>
	<p><br /></p>
	<p><br /></p>
	<p><br /></p>
	'''
	
release_sw = "SW9.3"
release_week = "Wk23.1"

child_titles = ["Diagnostics, Power, VuC & CAN",
"ECall, Connectivity & Geofence",
"Platform Patches",
"RAS, Security & UCD",
"SW reprogramming",
"System"]

##for titles in child_titles:
##	childPage_title = release_sw + " " + release_week + " " + titles
##	query.create_page(ancestors_id=parent_id, title=childPage_title, value=child_template)   
##        
##
