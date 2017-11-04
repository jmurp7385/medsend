from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
  title = "MedSend"
  return render_template('index.html', title=title)

@app.route('/donor')
def donor():
	title = "MedSend"
	user = {"firstName" : "Kenny", "lastName" : "Brawner"}
	return render_template('donor.html', user=user, title=title)

@app.route('/donee')
def donee():
	return render_template('donee.html')

if __name__=='__main__':
  app.run(debug=True)
