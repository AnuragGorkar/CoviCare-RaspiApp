from flask import Flask
import random

salt = "hb0bIc"
password = "mGMZOu8P"




app = Flask(__name__)

vitals_list = [
{"temp": 31, "hb" : 75, "o2" : 98.42},
{"temp": 32, "hb" : 78, "o2" : 97.25},
{"temp": 27, "hb" : 79, "o2" : 96.53},
{"temp": 29, "hb" : 88, "o2" : 93.72},
{"temp": 30, "hb" : 85, "o2" : 96.26},
{"temp": 30, "hb" : 83, "o2" : 98.98},
{"temp": 34, "hb" : 81, "o2" : 99.00},
{"temp": 31, "hb" : 77, "o2" : 97.42},
{"temp": 29, "hb" : 90, "o2" : 99.24},
{"temp": 29, "hb" : 93, "o2" : 99.17},
{"temp": 30, "hb" : 99, "o2" : 98.89},
]

@app.route("/")
def vitalsInfoPage():
	return str(vitals_list[random.randint(0, 10)])

if __name__ == "__main__":
	app.run(host='0.0.0.0', port= 8080)

