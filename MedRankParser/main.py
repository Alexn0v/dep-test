import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import urllib.request

from PIL import  Image, ImageOps

import dropbox
from dropbox.exceptions import AuthError
import pathlib




#VARIABLES
CHROME_DRIVER = '/Users/alexnov/chromedriver'
DROPBOX_ACCESS_TOKEN = 'sl.BG8CD_sO6B1R3R3PB0ytweTmsBAOyXeVfDCzqH4lJ2FFRD2yfcmdMWui92OOzWII1JZlAMt2CjcSV_WRHMK0EY9AD-mhJMbtFfnmN244u4iSZSdZjiBJVsEFQoPA7CKJukeAf1N5COI-'

# START CHROME DRIVER
Driver = webdriver.Chrome (executable_path=CHROME_DRIVER)


# START WORK WITH EXCEL
MedRank_columns = [0,1,2,3]
MedRank_Leads = pd.read_excel('MedRank_Leads.xlsx', usecols=MedRank_columns)

print ('Something need doing? | parse_all_data ()')

def parse_all_data ():
	for i in range(len(MedRank_Leads)):
		link = MedRank_Leads.loc[i].at['Photo']
		first_name = MedRank_Leads.loc[i].at['First Name']
		last_name = MedRank_Leads.loc[i].at['Last Name']
		image_directory,image_name = get_image(link,first_name,last_name)
		image_directory,image_name = resize_image(image_directory,image_name)
		m,dropbox_file_path = dropbox_upload_file(image_directory,image_name,dropbox_file_path='/MEDRANK_TEST/{}'.format(image_name))
		image_link = dropbox_get_link(dropbox_file_path)
		MedRank_Leads.loc[i,'Link'] = image_link

	MedRank_Leads.to_excel ('test.xlsx')
	print('Jobs Done !')

def dropbox_connect():
	try:
		dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
	except AuthError as e:
		print('Error connecting to Dropbox with access token: ' + str(e))
	return dbx

def get_image(link,first_name,last_name):
	Driver.get(link)
	img = Driver.find_element(by=By.XPATH, value='//*[@id="profilePhoto"]/img')
	src = img.get_attribute ('src')
	urllib.request.urlretrieve (src, "/Users/alexnov/Medrank/Original/profile-photo_doctor_primarycare_{}_{}_1024x1024_2021.png".format(first_name,last_name))
	return ("/Users/alexnov/Medrank/Original/profile-photo_doctor_primarycare_{}_{}_1024x1024_2021.png".format(first_name,last_name),
			"profile-photo_doctor_primarycare_{}_{}_1024x1024_2021.png".format(first_name,last_name))

def resize_image(image_directory,image_name):
	img = Image.open(image_directory)
	img = ImageOps.fit(img, (1024,1024))
	img.save("/Users/alexnov/Medrank/Resized/"+image_name)
	return ("/Users/alexnov/Medrank/Resized/",image_name)

def dropbox_upload_file(local_path, local_file, dropbox_file_path):
	try:
		dbx = dropbox_connect()
		local_file_path = pathlib.Path(local_path) / local_file
		with local_file_path.open("rb") as f:
			meta = dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))
			return meta,dropbox_file_path
	except Exception as e:
		print('Error uploading file to Dropbox: ' + str(e))

def dropbox_get_link(dropbox_file_path):
	try:
		dbx = dropbox_connect()
		shared_link_metadata = dbx.sharing_create_shared_link_with_settings(dropbox_file_path)
		shared_link = shared_link_metadata.url
		return shared_link.replace('?dl=0', '?dl=0')
	except dropbox.exceptions.ApiError as exception:
		if exception.error.is_shared_link_already_exists():
			shared_link_metadata = dbx.sharing_get_shared_links(dropbox_file_path)
			shared_link = shared_link_metadata.links[0].url
			return shared_link.replace('?dl=0', '?dl=0')







#len(MedRank_Leads)
#MedRank_Leads.loc[0].at['Link']
#MedRank_Leads.at[0,'Link'] = 1
#MedRank_Leads.to_excel('test.xlsx')