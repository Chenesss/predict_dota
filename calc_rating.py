from sql_connection import sql
from datetime import datetime


dota_db = sql()

all_matches = dota_db.get_all_matches(processed=False)

for match in all_matches:

	if match.team1_result > match.team2_result:
		winner = match.team1_name
		loser = match.team2_name
	elif match.team1_result < match.team2_result:
		loser = match.team1_name
		winner = match.team2_name
	else:
		print("Draw")
		dota_db.processed_match(match.ID)
		continue

	winner_rating = dota_db.get_team_rating(winner)
	loser_rating = dota_db.get_team_rating(loser)

	try:
		winner_rating = int(winner_rating)
		loser_rating = int(loser_rating)
	except ValueError:
		print(f"{match.team1_name} or {match.team2_name} team not found")
		continue


	if winner_rating > loser_rating:
		pass
	elif winner_rating <= loser_rating:
		if (loser_rating - winner_rating) > 25:
			rating_difference = loser_rating - winner_rating
			adjustment = int(rating_difference/3)
			winner_rating += adjustment
			loser_rating -= adjustment
		else:
			winner_rating += 25
			loser_rating -= 25

	dota_db.update_team_rating(winner, winner_rating)
	dota_db.update_team_rating(loser, loser_rating)

	print(f"Winner: {winner} adjusted rating is {winner_rating}")
	print(f"Loser: {loser} adjusted rating is {loser_rating}")

	dota_db.processed_match(match.ID)

