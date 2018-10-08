import pyodbc
from dota_objects import dota_match

#server = "DESKTOP-A5IJFLQ"
server = "localhost"
database = "PREDICT_DOTA"


class sql:
	def __init__(self):
		try:
			print("Starting Connection...")
			self.connection = pyodbc.connect(DRIVER='{SQL Server}', server=server,database=database, port='1433',trusted_connection='yes', timeout=10)
			self.cursor = self.connection.cursor()
		except pyodbc.Error as err:
			print(f"Something went wrong and unable to establish SQL connection")
			if err.args[0] == '28000':
				error_msg("Login Failed for user")
			else:
				raise
		
	def write_match(self, match_data):
		team1_id = self.get_team_id(match_data.team1)
		team2_id = self.get_team_id(match_data.team2)

		match_ID = self.match_exist(match_data)
		if match_ID:
			print("Match already in system")
			query = f"update match set datetime=CAST('{match_data.date_time}' as datetime), team1_result={match_data.t1_score}, team2_result={match_data.t2_score}, team1_odds={match_data.t1_odds}, team2_odds={match_data.t2_odds} where id = {match_ID}"
		else:
			print("Match not yet in system")
			query = f"insert into match (tournament_name, BO, datetime, team1_name, team2_name, team1_odds, team2_odds, team1_result, team2_result) values ('{match_data.tournament}', '{match_data.game_format}', CAST('{match_data.date_time}' as datetime), '{match_data.team1}', '{match_data.team2}', {match_data.t1_odds}, {match_data.t2_odds}, {match_data.t1_score}, {match_data.t2_score})"

		self.cursor.execute(query)
		self.cursor.commit()

	def match_exist(self, match_data):
		query = f"select * from match where tournament_name='{match_data.tournament}' and team1_name = '{match_data.team1}' and team2_name = '{match_data.team2}' and CAST('{match_data.date_time}' as datetime) >= datetime "
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		if(len(results)):
			return results[0].ID
		else:
			return False

	def get_team_id(self, team_name):
		self.team_validation(team_name)

		self.cursor.execute(f"select * from team where name = '{team_name}'")
		results = self.cursor.fetchall()
		if len(results) == 1:
			print(f"Single team found")
		else:
			if len(results) > 1:
				raise Exception(f"There is more than one record in Team table with name {team_name}") 
			elif len(results) == 0:
				raise Exception(f"There is no record in Team table with name {team_name}")  

		return results[0].id
		


	def team_validation(self, team_name):
		query = f"select * from team where name = '{team_name}'"
		self.cursor.execute(query)
		if len(self.cursor.fetchall()) == 0:
			query = f"insert into team (name, rating) values ('{team_name}', 2500)"
			self.cursor.execute(query)
			self.cursor.commit()

	def match_history(self, team):
		query = f"select * from match where team1_name = '{team}' or team2_name = '{team}"
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def get_all_teams(self):
		query = f"select * from team"
		self.cursor.execute(query)
		return self.cursor.fetchall()

	def get_team_rating(self, team):
		query = f"select * from team where name = '{team}'"
		self.cursor.execute(query)
		results = self.cursor.fetchall()
		if len(results):
			return results[0].rating
		else:
			return "None"

	def get_all_matches(self, processed=None):
		if processed == True:
			query =f"select * from match where processedat is not NULL order by datetime"
		elif processed == False:
			query =f"select * from match where processedat is NULL order by datetime"
		else:
			query =f"select * from match order by datetime"

		self.cursor.execute(query)
		return self.cursor.fetchall()






	def __del__(self):
		print("Closing Connection")
		self.connection.close()