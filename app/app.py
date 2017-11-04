from flask import Flask
from flask import render_template
import csv
import sqlite3
import json
import math

app = Flask(__name__)

@app.route('/')
def index():
  create_db()
  donations = [
  { "img": "static/img/crutch.jpeg",
    "item": "Crutches",
    "location": "Houston"
  },
  { "img": "static/img/crutch.jpeg",
    "item": "Crutches",
    "location": "Dallas"
  },
  { "img": "static/img/crutch.jpeg",
    "item": "Crutches",
    "location": "Chicago"
  },
  { "img": "static/img/crutch.jpeg",
    "item": "Crutches",
    "location": "New York"
  },
  { "img": "static/img/crutch.jpeg",
    "item": "Crutches",
    "location": "Denver"
  }
  ]
  return render_template('index.html', donations=donations)

@app.route('/donor')
def donor():
	title = "MedSend"
	users = [{"firstName" : "Kenny",
	        "lastName" : "Brawner",
	        "numDonations" : 8,
	        "userID" : 1}]
	user = users[0]

	items = [{"userID"   : 1,
	          "itemType" : "Crutches",
	          "status"   : 1,
	          "fileName" : "../static/img/crutch.jpeg"},
	         {"userID"   : 1,
	          "itemType" : "Wheelchair",
	          "status"   : 2,
	          "fileName" : "../static/img/wheelchair-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "Crutches",
	          "status"   : 3,
	          "fileName" : "../static/img/crutch.jpeg"},
	         {"userID"   : 1,
	          "itemType" : "Wheelchair",
	          "status"   : 1,
	          "fileName" : "../static/img/wheelchair-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "Crutches",
	          "status"   : 2,
	          "fileName" : "../static/img/crutch.jpeg"},
	         {"userID"   : 1,
	          "itemType" : "Wheelchair",
	          "status"   : 3,
	          "fileName" : "../static/img/wheelchair-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "Crutches",
	          "status"   : 1,
	          "fileName" : "../static/img/crutch.jpeg"},
	         {"userID"   : 1,
	          "itemType" : "Wheelchair",
	          "status"   : 2,
            "fileName" : "../static/img/wheelchair-01.jpg"}]

	return render_template('donor.html', user=user,
		                                 title=title,
		                                 items=items)

@app.route('/donee')
def donee():
	return render_template('donee.html')

if __name__=='__main__':
  app.run(debug=True)

def create_db():
  conn = sqlite3.connect('./db/database.db')
  conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
  c = conn.cursor()
  c.execute("DROP TABLE users")
  c.execute('''CREATE TABLE users
               (id int,
                username text,
                password text,
                type text)''')
  file_name = '../users.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print(row)
    else:
      c.execute("INSERT INTO users VALUES (?,?,?,?)", row)

  c.execute("DROP TABLE donations")
  c.execute('''CREATE TABLE donations
               (userid int,
                item_type text,
                image text,
                date_donated text,
                date_distributed text)''')
  file_name = '../donations.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print(row)
    else:
      c.execute("INSERT INTO users VALUES (?,?,?,?,?)", row)

  c.execute("DROP TABLE requests")
  c.execute('''CREATE TABLE requests
               (userid int,
                item_type text,
                icon text
                image text,
                date_requested text,
                date_recieved text)''')
  file_name = '../requests.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print(row)
    else:
      c.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", row)
  conn.commit()
  f.close()
