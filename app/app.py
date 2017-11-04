from flask import Flask,jsonify,request,redirect
from flask import render_template
import sys
import os
import csv
import sqlite3
import json
import math

app = Flask(__name__)

db_path = os.path.join(app.root_path, "db/database.db")

class User:
  def __init__(self, name):
    self.name = name
    self.requested = ["car", "crutches", "rock"]
    self.requested2 = ["wheelchair", "heelies"]

@app.route('/')
def index():
  create_db()
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  orders = c.execute("SELECT * from donations where date_distributed > 2017-01-01")
  data = c.fetchall()
  donations = donations_dict_arr(data)
  return render_template('index.html', donations=donations)

@app.route('/login', methods=['POST'])
def login():
  print("login",request.form)
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  username = request.form['username']
  password = request.form['password']
  if username == '' or password == '':
    return redirect('/')
  orders = c.execute("SELECT type from users where username=? AND password=?",(username,password))
  data = c.fetchall()[0][0]
  print(data)
  if data == "donor":
    return redirect('/donor/1')
  else:
    return redirect('/donee/2')

@app.route('/donor/<userid>')
def donor(userid):
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

@app.route('/request')
def request():
    wheelchair = {'name' : 'wheelchair', 'status' : 2, 'image' : 'static/img/svg/crutches-icon-01.svg'}
    heelies = {'name' : 'walker', 'status' : 3, 'image' : 'static/img/svg/walker-icon-01.svg'}
    donations = {'car' : ['honda', 'tesla'],
        'crutches' : ['broken crutches', 'shiny new crutches']}
    progression = ['processing ', 'request successful', 'ready for pickup', 'received']
    title = "MedSend"
    user = User('john doe')
    return render_template('request.html', user=user, title=title, donations = donations)

@app.route('/donee/<userid>')
def donee():
    wheelchair = {'name' : 'wheelchair', 'status' : 2, 'image' : 'static/img/svg/crutches-icon-01.svg'}
    heelies = {'name' : 'walker', 'status' : 3, 'image' : 'static/img/svg/walker-icon-01.svg'}
    donations = {'car' : ['honda', 'tesla'],
            'crutches' : ['broken crutches', 'shiny new crutches']}
    progression = ['processing ', 'request successful', 'ready for pickup', 'received']
    title = "MedSend"
    user = User('john doe')
    return render_template('donee.html', user=user, title=title, progression=progression, status=2)

if __name__=='__main__':
  app.run(debug=True)

def donations_dict_arr(data):
  donations= []
  for d in data:
    item = dict()
    item['userid'] = d[0]
    item['item_type'] = d[1]
    item['image'] = d[2]
    item['date_donated'] = d[3]
    item['date_distributed'] = d[4]
    donations.append(item)
    print(donations)
  return donations


def create_db():
  conn = sqlite3.connect(db_path)
  conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
  c = conn.cursor()
  c.execute("DROP TABLE users")
  c.execute('''CREATE TABLE users
               (id int,
                username text,
                password text,
                type text)''')
  file_name = app.root_path +'/csv/users.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print('ROW SKIPPED',row)
    else:
      c.execute("INSERT INTO users VALUES (?,?,?,?)", row)

  c.execute("DROP TABLE donations")
  c.execute('''CREATE TABLE donations
               (userid int,
                item_type text,
                image text,
                date_donated text,
                date_distributed text)''')
  file_name = app.root_path+'/csv/donations.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print('ROW SKIPPED',row)
    else:
      c.execute("INSERT INTO donations VALUES (?,?,?,?,?)", row)

  c.execute("DROP TABLE requests")
  c.execute('''CREATE TABLE requests
               (userid int,
                item_type text,
                icon text,
                image text,
                date_requested text,
                date_recieved text)''')
  file_name = app.root_path+'/csv/requests.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print('ROW SKIPPED',row)
    else:
      c.execute("INSERT INTO requests VALUES (?,?,?,?,?,?)", row)
  conn.commit()
  f.close()
