from flask import Flask
from flask import render_template
from flask import request
import csv

# ethan code
class User:
  def __init__(self, name):
    self.name = name
    self.requested = ["car", "crutches", "rock"]
    self.requested2 = [wheelchair, heelies]
#####################

app = Flask(__name__)

@app.route('/')
def index():
  title = "MedSend"
  return render_template('index.html', title=title)

@app.route('/donee')
def donee():
    wheelchair = {'name' : 'wheelchair', 'status' : 2, 'image' : 'static/img/svg/crutches-icon-01.svg'}
    heelies = {'name' : 'walker', 'status' : 3, 'image' : 'static/img/svg/walker-icon-01.svg'}
    donations = {'car' : ['honda', 'tesla'],
        'crutches' : ['broken crutches', 'shiny new crutches']}
    progression = ['processing ', 'request successful', 'ready for pickup', 'received']
    title = "MedSend"
    user = User('john doe')
    return render_template('donee.html', user=user, title=title, donations = donations)

@app.route('/donee_profile')
def displayProfile():
    wheelchair = {'name' : 'wheelchair', 'status' : 2, 'image' : 'static/img/svg/crutches-icon-01.svg'}
    heelies = {'name' : 'walker', 'status' : 3, 'image' : 'static/img/svg/walker-icon-01.svg'}
    donations = {'car' : ['honda', 'tesla'],
            'crutches' : ['broken crutches', 'shiny new crutches']}
    progression = ['processing ', 'request successful', 'ready for pickup', 'received']
      title = "MedSend"
    user = User('john doe')
    return render_template('donee_profile.html', user=user, title=title, progression=progression, status=2)

@app.route('/update_requests', methods=[ 'POST'])
def update():
  requested = request.form.get("needed items")


if __name__=='__main__':
  app.run(debug=True)
