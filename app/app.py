from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/test')
def test():
  return render_template('test.html')

@app.route('/donor')
def donor():
	title = "MedSend"
	users = [{"firstName" : "Kenny", 
	        "lastName" : "Brawner",
	        "numDonations" : 8,
	        "userID" : 1}]
	user = users[0]

	items = [{"userID"   : 1,
	          "itemType" : "crutches",
	          "status"   : 1,
	          "fileName" : "../static/images/crutches-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "wheelchair",
	          "status"   : 2, 
	          "fileName" : "../static/images/wheelchair-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "crutches",
	          "status"   : 3,
	          "fileName" : "../static/images/crutches-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "wheelchair",
	          "status"   : 1, 
	          "fileName" : "../static/images/wheelchair-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "crutches",
	          "status"   : 2,
	          "fileName" : "../static/images/crutches-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "wheelchair",
	          "status"   : 3,
	          "fileName" : "../static/images/wheelchair-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "crutches",
	          "status"   : 1,
	          "fileName" : "../static/images/crutches-01.jpg"},
	         {"userID"   : 1,
	          "itemType" : "wheelchair",
	          "status"   : 2, 
	          "fileName" : "../static/images/wheelchair-01.jpg"}]
	           
	return render_template('donor.html', user=user, 
		                                 title=title, 
		                                 items=items)

@app.route('/donee')
def donee():
	return render_template('donee.html')

if __name__=='__main__':
  app.run(debug=True)
