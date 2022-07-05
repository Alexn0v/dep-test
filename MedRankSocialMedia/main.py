import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import re

import urllib.request



#VARIABLES
CHROME_DRIVER = '/Users/alexnov/chromedriver'

# START CHROME DRIVER
Driver = webdriver.Chrome (executable_path=CHROME_DRIVER)

# REGEX
Instagram = r'(.)+(instagram.com/)+(.)*'
Facebook = r'(.)+(facebook.com/)+(.)*'
Twitter = r'(.)+(Twitter.com/)+(.)*'
Linkedin = r'(.)+(Linkedin.com/)+(.)*'

#Facebook	Instagram	Linkedin	Twitter

# START WORK WITH EXCEL
MedRank_columns = [3,4,5,6,8,9,10,11]
MedRank_Leads = pd.read_excel('MedRank_Leads.xlsx', usecols=MedRank_columns)

print ('Something need doing? | parse_all_data ()')

def parse_all_data ():
	for i in range(0,len(MedRank_Leads)):
		link = MedRank_Leads.loc[i].at['Website']
		try:
			get_social_media(link,i)
		except Exception as e:
			print(e)
			MedRank_Leads.loc[i, 'Facebook'] = 'No Website'
			MedRank_Leads.loc [i, 'Instagram'] = 'No Website'
			MedRank_Leads.loc [i, 'Linkedin'] = 'No Website'
			MedRank_Leads.loc [i, 'Twitter'] = 'No Website'
			MedRank_Leads.to_excel ('final.xlsx')
		MedRank_Leads.fillna('–',inplace=True)
		MedRank_Leads.to_excel ('final.xlsx')
		print('Done #{}'.format(i))
	print('Jobs Done !')

def get_social_media (link,i):
	Driver.get(link)
	social_media_links = Driver.find_elements(by=By.XPATH, value='//a[@href]')
	for _ in social_media_links:
		href = _.get_attribute('href')
#		print (href)
		parse_social_media (href,i)
#		add_social_media_to_table (i,hred_link, social_media)


def parse_social_media (href,i):
	if re.match(Instagram, href) is not None:
		MedRank_Leads.loc [i,'Instagram'] = href
		print (href,'Instagram')
#		return (href,'Instagram')
	elif re.match(Facebook, href) is not None:
		MedRank_Leads.loc [i, 'Facebook'] = href
		print (href,'Facebook')
#		return (href, 'Facebook')
	elif re.match(Twitter, href) is not None:
		MedRank_Leads.loc [i, 'Twitter'] = href
		print (href,'Twitter')
#		return (href, 'Twitter')
	elif re.match (Linkedin, href) is not None:
		MedRank_Leads.loc [i, 'Linkedin'] = href
		print (href, 'Linkedin')
#		return (href, 'Linkedin')

def fill_blank_spaces (i):
	Facebook_b = MedRank_Leads.loc [i, 'Facebook']
	Instagram_b = MedRank_Leads.loc [i, 'Instagram']
	Linkedin_b = MedRank_Leads.loc [i, 'Linkedin']
	Twitter_ = MedRank_Leads.loc [i, 'Twitter']
	pass


#	MedRank_Leads.to_excel ('final.xlsx')



def add_social_media_to_table(i,hred_link,social_media):
	MedRank_Leads.loc [i, social_media] = hred_link
	MedRank_Leads.to_excel ('final.xlsx')






'''
def test ():
	link = 'http://clearcenterofhealth.com/'
	Driver.get(link)
	website_links = Driver.find_elements(by=By.XPATH, value='//a[@href]')
	for _ in website_links:
		print (_.get_attribute ("href"))
'''

#elems = driver.find_elements_by_tag_name('a')
#    for elem in elems:
#        href = elem.get_attribute('href')
#        if href is not None:
#            print(href)
