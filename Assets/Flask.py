__author__ = '1m2i3_000'
from flask import Flask, render_template, request, jsonify, session, g, redirect, url_for, abort ,Response
import json
import requests
import xmltodict
import os
import sqlite3

DATABASE = 'scores.db'

app = Flask(__name__)
app.config.from_object("__main__")


Charity  = {"290626":"Suited to Success Inc."
           ,"654538":"KiTs for the World"
           ,"2050":"The Demo Charity (JustGiving Demo)"
           ,"186234":"Al-khair"}

api_key = 'aa49186d'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/test')
def get_current_user():
    return "test"

@app.route('/api/getCharities')
def getCharities():
    return Response(json.dumps(Charity), mimetype='application/json')

@app.route('/api/post/<charity_id>')
def getId (charity_id):
    testy = get_Charity_Details(charity_id)
    return Response(testy, mimetype='application/json')

def get_Charity_Details(_charity_id):
    url = 'https://v3-sandbox.justgiving.com/donation/direct/charity/%s' % (_charity_id)
    details = requests.get('https://api.justgiving.com/%s/v1/charity/search?q=&charityid=%s' % (api_key,_charity_id))
    obj = xmltodict.parse(details.content)
    description = obj['charitySearch']['charitySearchResults']['charitySearchResult']['description']
    name = obj['charitySearch']['charitySearchResults']['charitySearchResult']['charityDisplayName']
    return json.dumps({'url':url,'name':name,'description':description})



if __name__ == "__main__":
    app.run(debug=True)