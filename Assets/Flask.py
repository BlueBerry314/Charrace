__author__ = '1m2i3_000'
from flask import Flask, render_template, request, jsonify
import json
import requests
app = Flask(__name__)

Charity  = {"290626":"Suited to Success Inc."
           ,"654538":"KiTs for the World"
           ,"2050":"The Demo Charity (JustGiving Demo)"
           ,"186234":"Al-khair"}

api_key = '07074f97'

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/test')
def get_current_user():
    return "test"

@app.route('/api/getCharities')
def getCharities():
    return json.dumps(Charity)

@app.route('/api/post/<charity_id>')
def getId (charity_id):
    pass

def get_Charity_Details(_charity_id):
    url = 'https://v3-sandbox.justgiving.com/donation/direct/'
    details = requests.get('https://api.justgiving.com/%s/v1/charity/search?q=&charityid=%s'(api_key,_charity_id))



if __name__ == "__main__":
    app.run(debug=True)