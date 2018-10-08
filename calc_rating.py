from sql_connection import sql

def find_winner(self):
		if t1_score > t2_score:
			return self.team1
		elif t1_score < t2_score:
			return self.team2
		else:
			return None

def find_loser(self):
	if t1_score < t2_score:
		return self.team1
	elif t1_score > t2_score:
		return self.team2
	else:
		return None

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
		winner = None
		loser = None


	winner_rating = dota_db.get_team_rating(winner)
	loser_rating = dota_db.get_team_rating(loser)

	# print(f'team1 rating is {winner_rating}')
	# print(f'team2 rating is {loser_rating}')

	try:
		team1_rating = int(winner_rating)
		team2_rating = int(loser_rating)
	except ValueError:
		print(f"{winner_rating} or {loser_rating} team not found")
		continue


	if winner_rating > loser_rating:
		pass
	elif winner_rating <= loser_rating:
		if (loser_rating - winner_rating) > 25:
			rating_difference = loser_rating - winner_rating
			adjustment = int(rating_difference/2)
			winner_rating += adjustment
			loser_rating -= adjustment
		else:
			winner_rating += 25
			loser_rating -= 25

	dota_db.cursor.execute(f"update team set rating = {winner_rating} where name = '{winner}'")
	dota_db.cursor.execute(f"update team set rating = {loser_rating} where name = '{loser}'")
	dota_db.cursor.commit()

	print(f"Winner adjusted rating is {winner_rating}")
	print(f"Loser adjusted rating is {loser_rating}")


