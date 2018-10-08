from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from dota_objects import dota_match
from sql_connection import sql
from datetime import datetime
from selenium.webdriver.chrome.options import Options 


def teamname_validation(team1, team2):
	"""Makes sure that the the teams are not TBD"""
	if team1 == "TBD" or team2 == "TBD":
		return False
	else:
		return True


options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

browser = webdriver.Chrome("ChromeDriver.exe", chrome_options=options)

dota_db = sql()

while True:
	
	for n in range(1, 6):
		browser.get(f'https://cybersportscore.com/en/dota-2?s={n}')
		finished_matches = browser.find_element_by_xpath("//div[@class='event_list event_list_ended']").find_elements_by_class_name('event')

		print(len(finished_matches))

		for match in finished_matches:
			print("next match")
			date_div = match.find_element_by_class_name('date')
			time = date_div.find_elements_by_tag_name("div")[0].text
			date = date_div.find_elements_by_tag_name("div")[1].text
			date_time = datetime.strptime(f'{date} {datetime.now().year} {time}', '%d %b %Y %H:%M')

			tournament_div = match.find_element_by_class_name('tournament')
			tournament_name = tournament_div.find_elements_by_tag_name('img')[0].get_attribute('alt')

			BO_div = match.find_element_by_class_name('bo')
			BO_format = BO_div.find_elements_by_tag_name('a')[0].text

			teams_div = match.find_element_by_class_name('teams')
			team1 = teams_div.find_elements_by_tag_name('em')[0].text
			team2 = teams_div.find_elements_by_tag_name('em')[1].text

			if not teamname_validation(team1, team2):
				continue

			if match.find_elements_by_class_name('eventbets'):
				odds = match.find_element_by_class_name('eventbets').find_elements_by_class_name('kt')
				team1_odds = odds[0].find_elements_by_tag_name('b')[0].text
				team2_odds = odds[1].find_elements_by_tag_name('b')[0].text
			else:
				team1_odds = '0'
				team2_odds = '0'

			team1_score = match.find_element_by_class_name('team-home').find_elements_by_tag_name('span')[0].text
			team2_score = match.find_element_by_class_name('team-away').find_elements_by_tag_name('span')[0].text



			print(f'{str(date_time)} {tournament_name} {BO_format} {team1} {team1_odds} {team2} {team2_odds} Scores:{team1_score} {team2_score}')
			match_data = dota_match(tournament_name, BO_format, date_time, team1, team2, team1_odds, team2_odds, team1_score, team2_score)

			dota_db.write_match(match_data)

	print(f"Run completed on: {datetime.now()}")
	sleep(600)

