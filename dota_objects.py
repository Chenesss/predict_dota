from datetime import datetime



class dota_match:
	def __init__(self, tournament, game_format, date_time, team1, team2, t1_odds, t2_odds, t1_score, t2_score):
		self.team1 = team1
		self.team2 = team2
		self.t1_odds = t1_odds
		self.t2_odds = t2_odds
		self.tournament = tournament
		self.date_time = date_time
		self.game_format = game_format
		self.t1_score = t1_score
		self.t2_score = t2_score

	def details(datetime=None, game_format=None, results=None):
		if datetime:
			self.datetime = datetime
		if game_format:
			self.game_format = game_format
		if results:
			self.results = results

	@property
	def winner(self):
		if t1_score > t2_score:
			return self.team1
		elif t1_score < t2_score:
			return self.team2
		else:
			return None
	
	@property
	def loser(self):
		if t1_score < t2_score:
			return self.team1
		elif t1_score > t2_score:
			return self.team2
		else:
			return None
	

	def store_team(self, team):
		if self.team1 == None:
			self.team1 = team
		elif self.team2 == None:
			self.team2 = team
		else:
			raise Exception(f'Trying to add 3rd team {team} into match id {self.id}')
	


# class team:
# 	def __init__(self, name, )

