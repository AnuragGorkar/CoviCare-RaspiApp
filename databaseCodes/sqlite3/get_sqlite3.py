import sqlite3

#Create a table
#This is done explicitly at the time of execution
#cursor.execute("""CREATE TABLE recorded_vitals( 
#	userId text primary key,
#	tempVal real ,
#	hbVal real,
#	spO2Val real,
#	timeRec datetime default current_timestamp
#	)""")

class SQLiteDataBase():
	def __init__ (self):
		#Create a conenction to the local recorded vitals data base
		self.conn = sqlite3.connect("recorded_users_vitals.db")
		
		#Create a crusor
		self.cursor = self.conn.cursor()
		
		#Create a table to store vitals data
		sqliteQuery = """CREATE TABLE IF NOT EXISTS VITALS_DATA (TEMP REAL, SPO2 REAL, HB REAL, COUGH_ANALYSIS REAL)"""
		self.cursor.execute(sqliteQuery)
		self.conn.commit()
		
	
	def get_vitals_data(self):	
		sqliteQuery = """SELECT * FROM VITALS_DATA"""
		self.cursor.execute(sqliteQuery)
		data = self.cursor.fetchall()
		self.conn.commit()
		return data
		
	def store_vitals_data(self, data):
		self.cursor.execute("INSERT INTO VITALS_DATA VALUES (?, ?, ?, ?)", (data['temp'], data['o2'], data['hb'],  data['cough_value']))
		print("Data from database")
		data = self.cursor.fetchall()
		self.conn.commit()
        


		



