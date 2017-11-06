from flask import Flask,jsonify,request,redirect
from flask import render_template
from datetime import datetime
import time
import sys
import os
import csv
import sqlite3
import json
import math

app = Flask(__name__)

# ref_userid = 5

db_path = os.path.join(app.root_path, "db/database.db")

icons = {
  'crutches': 'static/img/svg/crutches-icon-01.svg',
  'wheelchair': 'static/img/svg/wheelchair-icon-01.svg',
  'stretcher': 'static/img/svg/stretcher-icon-01.svg',
  'walker': 'static/img/svg/walker-icon-01.svg',
  'fracture boot': 'static/img/svg/fractureboot-icon-01.svg',
  'cane': 'static/img/svg/cane-icon-01.svg'
}

images = {
  'crutches': 'static/img/crutches-02.jpeg',
  'cane': 'static/img/cane-01.jpeg',
  'wheelchair': 'static/img/wheelchair-01.jpeg',
  'stretcher': 'static/img/stretcher-01.jpeg',
  'walker': 'static/img/walker-01.jpeg',
  'fracture boot': 'static/img/fractureboot-01.jpeg',
}

@app.route('/')
def index():
  create_db()
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  orders = c.execute("SELECT * from donations where date_distributed > 2017-01-01 LIMIT 5")
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
  orders = c.execute("SELECT id,type from users where username=? AND password=?",(username,password))
  data = c.fetchall()
  if data == []:
    return redirect('/')
  print(data)
  account_type = data[0][1]
  userid = str(data[0][0])
  if data[0][1] == "donor":
    return redirect('/donor/'+userid)
  elif data[0][1] == "donee":
    return redirect('/donee/'+userid)
  else:
    return redirect('/organization/'+userid)

@app.route('/contact')
def contact():
  return render_template('contact.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/new_account', methods=['GET'])
def new_account():
  return render_template('new_account.html')

@app.route('/new_account', methods=['POST'])
def new_acc_login():
  print(request.form)
  # ref_userid += 1
  new_user = []
  username = request.form['username']
  password = request.form['password']
  password2 = request.form['password2']
  user_type = request.form['type']
  if password != password2 or username == '':
    return redirect('/new_account')
  new_user.append(str(5*23456%6+124%3))
  new_user.append(username)
  new_user.append(password)
  new_user.append(user_type)
  print(new_user)
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  c.execute("INSERT INTO users VALUES (?,?,?,?)", new_user)
  conn.commit()
  return redirect('/donee/'+new_user[0])

@app.route('/donor/<userid>')
def donor(userid):
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  orders = c.execute("SELECT * from donations where userid == "+userid+"")
  data = c.fetchall()
  donations = donations_dict_arr(data)
  title = "MedSend"
  orders = c.execute("SELECT * from users where id == "+userid+"")
  data = c.fetchall()
  username = ""
  for d in data:
    username = d[1]
  return render_template('donor.html', username=username,
		                                 title=title,
		                                 donations=donations,
                                     userid=userid)

@app.route('/donate/<userid>', methods=['GET'])
def donate_item(userid):
  return render_template("donate.html", userid=userid)

@app.route('/request/<userid>', methods=['GET'])
def request_item(userid):
    return render_template('request.html',userid=userid)

@app.route('/organization/<userid>')
def organization(userid):
    title = "MedSend"
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    orders = c.execute("SELECT * from donations where userid == "+userid+"")
    data = c.fetchall()
    donations = donations_dict_arr(data)
    orders = c.execute("SELECT * from users where id == "+userid+"")
    data = c.fetchall()
    username = ""
    for d in data:
      username = d[1]
    return render_template('organization.html', username=username, title=title, donations = donations, userid=userid)

@app.route('/donee/<userid>', methods=['GET'])
def donee(userid):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    orders = c.execute("SELECT * from requests where userid == "+userid+"")
    data = c.fetchall()
    requests = requests_dict_arr(data)
    orders = c.execute("SELECT * from users where id == "+userid+"")
    data = c.fetchall()
    username = ""
    for d in data:
      username = d[1]
    return render_template('donee.html', username=username, userid=userid, requests = requests)

@app.route('/donee/<userid>', methods=['POST'])
def donee_requests_update(userid):
    item = request.form['item_type']
    new_request = []
    new_request.append(userid)
    new_request.append(request.form['item_type'])
    new_request.append(icons[item])
    new_request.append(images[item])
    now = datetime.now()
    today = str(now.strftime('%Y/%m/%d'))
    today = today.replace('/','-')
    new_request.append(today)
    new_request.append("")
    new_request.append(request.form['amount'])
    print(new_request)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?)", new_request)
    conn.commit()
    return redirect('/donee/'+userid)

@app.route('/donor/<userid>', methods=['POST'])
def donor_donations_update(userid):
  item = request.form['item_type']
  new_donation = []
  new_donation.append(userid)
  new_donation.append(request.form['item_type'])
  new_donation.append(images[item])
  now = datetime.now()
  today = str(now.strftime('%Y/%m/%d'))
  today = today.replace('/','-')
  new_donation.append(today)
  new_donation.append("")
  new_donation.append(request.form['amount'])
  print(new_donation)
  conn = sqlite3.connect(db_path)
  c = conn.cursor()
  c.execute("INSERT INTO donations VALUES (?,?,?,?,?,?)", new_donation)
  conn.commit()
  return redirect('/donor/'+userid)


if __name__=='__main__':
  app.run(debug=True)

def requests_dict_arr(data):
  donations= []
  for d in data:
    item = dict()
    item['userid'] = d[0]
    item['item_type'] = d[1]
    item['icon'] = d[2]
    item['image'] = d[3]
    item['date_requested'] = d[4]
    item['date_received'] = d[5]
    donations.append(item)
    print(donations)
  return donations

def donations_dict_arr(data):
  donations= []
  for d in data:
    item = dict()
    item['userid'] = d[0]
    item['item_type'] = d[1]
    item['image'] = d[2]
    item['date_donated'] = d[3]
    item['date_distributed'] = d[4]
    item['amount'] = d[5]
    donations.append(item)
    print(donations)
  return donations


def create_db():
  conn = sqlite3.connect(db_path)
  conn.text_factory = lambda x: unicode(x, "utf-8", "ignore")
  c = conn.cursor()
  # if remaking database.db comment the below 3 lines
  c.execute("DROP TABLE users")
  c.execute("DROP TABLE donations")
  c.execute("DROP TABLE requests")

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

  c.execute('''CREATE TABLE donations
               (userid int,
                item_type text,
                image text,
                date_donated text,
                date_distributed text,
                amount int)''')
  file_name = app.root_path+'/csv/donations.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print('ROW SKIPPED',row)
    else:
      c.execute("INSERT INTO donations VALUES (?,?,?,?,?,?)", row)

  c.execute('''CREATE TABLE requests
               (userid int,
                item_type text,
                icon text,
                image text,
                date_requested text,
                date_received text,
                amount int)''')
  file_name = app.root_path+'/csv/requests.csv'
  f = open(file_name,'rt')
  reader = csv.reader(f)
  column_names = True
  for row in reader:
    if column_names:
      column_names = False
      print('ROW SKIPPED',row)
    else:
      c.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?)", row)
  conn.commit()
  f.close()
