from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from dota_objects import dota_match



matches = {}

browser = webdriver.Chrome("ChromeDriver.exe")

browser.get('http://esportlivescore.com/g_dota.html')

#match_div = browser.find_element_by_id('upcoming')

all_matches = browser.find_elements_by_tag_name('div')

#print(len(all_matches))
for match in all_matches:
	if "event_id_" in match.get_attribute('id'):
		game_id = match.get_attribute('id')
		print(game_id)
		matches[game_id] = dota_match(game_id)
		teams = match.find_elements_by_class_name('event-team-info')
		for team in teams:
			if len(team.find_elements_by_tag_name('a')):
				team_name = team.find_elements_by_tag_name('a')[0].text
				print(team_name)
				matches[game_id].store_team(team_name)
			else:
				print("TBD team")


