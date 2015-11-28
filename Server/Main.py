__author__ = 'Marelis'

import urllib.request
import requests

Charity  = [("Suited to Success Inc.","290626"),"",)]

def Get_Donation():
    donation = requests.get('')
    data = site.read()
    file = open("file.html","wb") #open file in binary mode
    file.write(data)
    file.close()
    return data

index = []


