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

Ammounts = [['290626',0]
           ,['654538',0]
           ,['2050',0]
           ,['186234',0]]
api_key = '1b135151'

def connect_db():
    db = sqlite3.connect(DATABASE)
    return db

def get_db():
    g.sqlite_db = connect_db()
    return g.sqlite_db

def update_db(_char_id,_amount):
    db = get_db()
    db.execute('insert into charities (char_id, amount) values (?, ?)',
               [_char_id, _amount])
    db.commit()
    print("i did it")
    return

@app.route("/")
def index():
    db = get_db()
    cur = db.execute('select char_id, amount from charities')
    entries = [dict(char_id =row[0],amount = row[1])for row in  cur.fetchall()]
    calucalte_sum_index(entries)
    print(Ammounts)
    return render_template('index.html', ammounts=Ammounts)

@app.route('/thanks/<char_id>/')
def post_donation(char_id):
    _donation_id= request.args.get('jgDonationId')
    donation_details =  requests.get('https://api.justgiving.com/%s/v1/donation/%s'%(api_key, _donation_id))
    obj = xmltodict.parse(donation_details.content)
    amount = obj['donation']['amount']
    update_db(char_id, amount)
    print("I CAME HERE FOR YOU SENPIE")
    return render_template('close.html')

def calucalte_sum_index(entries):
    for elem in entries:
        for item in Ammounts:
            if elem['char_id'] in item[0]:
                item[1]+= elem['amount']
    return

def calucalte_sum(_add_entry):
    for item in Ammounts:
        if _add_entry[0] in item[0]:
            item[1]+=_add_entry[1]
    return

@app.route('/test')
def get_current_user():
    return "test"

@app.route('/api/getCharities')
def getCharities():
    return Response(json.dumps(Charity), mimetype='application/json')

@app.route('/api/getPoints')
def givePoints():
    #print(Ammounts)
    point_map=json.dumps(dict([(elem[0],elem[1])for elem in Ammounts]))
    return Response(point_map,mimetype='application/json')

@app.route('/api/post/<charity_id>')
def getId (charity_id):
    testy = get_Charity_Details(charity_id)
    return Response(testy, mimetype='application/json')

def get_Charity_Details(_charity_id):
    url = 'https://v3-sandbox.justgiving.com/4w350m3/donation/direct/charity/2050/?amount=10.00&exitUrl=http%3A%2F%2F127.0.0.1%2Fthanks%2F2050%3FjgDonationId%3DJUSTGIVING-DONATION-ID&currency=GBP&reference=0000&utm_source=sdidirect&utm_medium=buttons&utm_campaign=buttontype#MessageAndAmount'.format()#.format(api_key,_charity_id,_charity_id)
    details = requests.get('https://api.justgiving.com/%s/v1/charity/search?q=&charityid=%s'%(api_key,_charity_id))
    obj = xmltodict.parse(details.content)
    description = obj['charitySearch']['charitySearchResults']['charitySearchResult']['description']
    name = obj['charitySearch']['charitySearchResults']['charitySearchResult']['charityDisplayName']
    return json.dumps({'url':url,'name':name,'description':description})



if __name__ == "__main__":
    app.run(debug=True)