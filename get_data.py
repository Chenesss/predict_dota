from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *

browser = webdriver.Chrome("/Library/Selenium/ChromeDriver")

browser.get('http://esportlivescore.com/g_dota.html')

#match_div = browser.find_element_by_id('upcoming')

all_matches = browser.find_elements_by_tag_name('div')

#print(len(all_matches))
for match in all_matches:
	if "event_id_" in match.get_attribute('id'):
		print(match.get_attribute('id'))
		teams = match.find_elements_by_class_name('event-team-info')
		for team in teams:
			if len(team.find_elements_by_tag_name('a')):
				print(team.find_elements_by_tag_name('a')[0].text)
			else:
				print("TBD team")


