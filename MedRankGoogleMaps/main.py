import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

import urllib.request



#VARIABLES
CHROME_DRIVER = '/Users/alexnov/chromedriver'
LINK = 'https://www.google.com/maps/'

# START CHROME DRIVER
Driver = webdriver.Chrome (executable_path=CHROME_DRIVER)

# START WORK WITH EXCEL
MedRank_columns = [3,4,21,22,23,24,25,26,27,28,29,30,31,32]
MedRank_Leads = pd.read_excel('MedRank_Leads.xlsx', usecols=MedRank_columns)

#Primary Location (Address Line 1)	Primary Location (Address Line 2)	Primary Location (City)	Primary Location (State)	Primary Location (Zip Code)
# Primary Location (Google Maps Link)
#Secondary Location (Address Line 1)	Secondary Location (Address Line 2)	Secondary Location (City)	Secondary Location (State)	Secondary Location (Zip Code)
# Secondary Location (Google Maps Link)


# !!!San Francisco CA94102

def parse_all_data():
	MedRank_Leads.fillna ('', inplace=True)
	for i in range(877,len(MedRank_Leads)):
#	for i in range (610, 629):
#		Primary_locatinon = MedRank_Leads.loc[i].at['Primary Location (Address Line 1)']+' '+MedRank_Leads.loc [i].at ['Primary Location (Address Line 2)']+MedRank_Leads.loc [i].at ['Primary Location (City)']+' '+MedRank_Leads.loc [i].at ['Primary Location (State)']+' '+str(MedRank_Leads.loc [i].at ['Primary Location (Zip Code)']).split('.')[0]
#		Secondary_location = MedRank_Leads.loc[i].at['Secondary Location (Address Line 1)']+' '+MedRank_Leads.loc [i].at ['Secondary Location (Address Line 2)']+MedRank_Leads.loc [i].at ['Secondary Location (City)']+' '+MedRank_Leads.loc [i].at ['Secondary Location (State)']+' '+str(MedRank_Leads.loc [i].at ['Secondary Location (Zip Code)']).split('.')[0]
		Primary_locatinon = MedRank_Leads.loc[i].at['Primary Location (Address Line 1)']+' '+MedRank_Leads.loc [i].at ['Primary Location (City)']+' '+MedRank_Leads.loc [i].at ['Primary Location (State)']+' '+str(MedRank_Leads.loc [i].at ['Primary Location (Zip Code)']).split('.')[0]
		Secondary_location = MedRank_Leads.loc[i].at['Secondary Location (Address Line 1)']+' '+MedRank_Leads.loc [i].at ['Secondary Location (City)']+' '+MedRank_Leads.loc [i].at ['Secondary Location (State)']+' '+str(MedRank_Leads.loc [i].at ['Secondary Location (Zip Code)']).split('.')[0]

#
#print(i,"1st:",Primary_locatinon,'2nd:',Secondary_location)

		if Primary_locatinon.replace(' ','') == '':
			MedRank_Leads.loc [i, 'Primary Location (Google Maps Link)'] = '-'
		else:
			try:
				print('Doing:',i,'Location:',Primary_locatinon)
				Primary_link = get_link(Primary_locatinon)
				MedRank_Leads.loc [i, 'Primary Location (Google Maps Link)'] = Primary_link
			except Exception as e:
				print (e)
				MedRank_Leads.loc [i, 'Primary Location (Google Maps Link)'] = 'Err'

		if Secondary_location.replace(' ','') == '':
			MedRank_Leads.loc [i, 'Secondary Location (Google Maps Link)'] = '-'
		else:
			try:
				print('Doing:',i,'Location:',Secondary_location)
				Secondary_link = get_link(Secondary_location)
				MedRank_Leads.loc [i, 'Secondary Location (Google Maps Link)'] = Secondary_link
			except Exception as e:
				print (e)
				MedRank_Leads.loc [i, 'Secondary Location (Google Maps Link)'] = 'Err'

		MedRank_Leads.to_excel ('final.xlsx')


def check_():
	MedRank_Leads.fillna ('', inplace=True)
	for i in range (0, 20):
#	for i in range(0,len(MedRank_Leads)):
		Primary_locatinon_1 = MedRank_Leads.loc[i].at['Primary Location (Address Line 1)']
		Primary_locatinon_2 = MedRank_Leads.loc [i].at ['Primary Location (Address Line 2)']
		Primary_locatinon_3 = MedRank_Leads.loc [i].at ['Primary Location (City)']
		Primary_locatinon_4 = MedRank_Leads.loc [i].at ['Primary Location (State)']
		Primary_locatinon_5 = str(MedRank_Leads.loc [i].at ['Primary Location (Zip Code)'])

		Secondary_location_1 = MedRank_Leads.loc[i].at['Secondary Location (Address Line 1)']
		Secondary_location_2 = MedRank_Leads.loc [i].at ['Secondary Location (Address Line 2)']
		Secondary_location_3 = MedRank_Leads.loc [i].at ['Secondary Location (City)']
		Secondary_location_4 = MedRank_Leads.loc [i].at ['Secondary Location (State)']
		Secondary_location_5 = str(MedRank_Leads.loc [i].at ['Secondary Location (Zip Code)'])


		if (Primary_locatinon_1,Primary_locatinon_2,Primary_locatinon_3,Primary_locatinon_4,Primary_locatinon_5) == '':
			MedRank_Leads.loc [i, 'Primary Location (Google Maps Link)'] = '-'
		else:
			try:
				Primary_location_all = Primary_locatinon_1 +' '+ Primary_locatinon_2 +' '+ Primary_locatinon_3 +' '+ Primary_locatinon_4 +' '+ Primary_locatinon_5
				print(i,Primary_location_all)
				Primary_link = get_link(Primary_location_all)
				MedRank_Leads.loc [i, 'Primary Location (Google Maps Link)'] = Primary_link
			except Exception as e:
				print (e)
				MedRank_Leads.loc [i, 'Primary Location (Google Maps Link)'] = 'Err'


		if (Secondary_location_1,Secondary_location_2,Secondary_location_3,Secondary_location_4,Secondary_location_5) == ' ':
			MedRank_Leads.loc [i, 'Secondary Location (Google Maps Link)'] = '-'
		else:
			try:
				Secondary_location_all = Secondary_location_1 +' '+ Secondary_location_2 +' '+ Secondary_location_3 +' '+ Secondary_location_4 +' '+ Secondary_location_5
				print (i, Secondary_location_all)
				Secondary_link = get_link (Secondary_location_all)
				MedRank_Leads.loc [i, 'Secondary Location (Google Maps Link)'] = Secondary_link
			except Exception as e:
				print (e)
				MedRank_Leads.loc [i, 'Secondary Location (Google Maps Link)'] = 'Err'
		MedRank_Leads.to_excel ('final.xlsx')


#		print(i,'1ST:',Primary_location_all,'2ND:',Secondary_location_all)

def get_link(Location):
	time.sleep(2)
	Driver.get (LINK)
	time.sleep (2)
	# Поле для ввода адреса
	Map_input = Driver.find_element(by=By.ID, value='searchboxinput')
	Map_input.send_keys (Location)
	# Share  адреса
	Driver.find_element (by=By.ID, value='searchbox-searchbutton').click ()
	time.sleep (6)
	Driver.find_element (by=By.XPATH,
						 value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[5]/button').click ()
	time.sleep (4)
	Location_link = Driver.find_element (by=By.XPATH,
									value='/html/body/div[3]/div[1]/div/div[2]/div/div[3]/div/div/div[1]/div[4]/div[2]/div[1]/input')
	Location_link = Location_link.get_attribute ('value')

	return Location_link






def test ():
	link = 'https://www.google.com/maps/'
	Driver.get(link)
	input = '4112 24th Street San Francisco	CA94114'
	maps_input=Driver.find_element(by=By.ID, value='searchboxinput')
	maps_input.send_keys(input)
	Driver.find_element(by=By.ID,value='searchbox-searchbutton').click()
	time.sleep(5)
	Driver.find_element(by=By.XPATH,value='/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[4]/div[5]/button').click()
	time.sleep(5)
	Map_link = Driver.find_element(by=By.XPATH,value='/html/body/div[3]/div[1]/div/div[2]/div/div[3]/div/div/div[1]/div[4]/div[2]/div[1]/input')
	Map_link = Map_link.get_attribute('value')
	print(Map_link)




'''
Doing: 25 Location:  San Francisco CA 94103
Doing: 32 Location:  San Francisco CA 94115
'''