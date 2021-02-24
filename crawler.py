import json
import requests
import twint
import sys
import datetime
from data import constants
from core import Graph, Trends, SendMail
import subprocess

#crawl and gather twitter data
def twitter_intel(user_name, text = ""):
    date_ = datetime.date.today()
    user = twint.Config()
    user.Username = user_name
    user.Limit = 10
    #user.Popular_tweets = True
    user.Since = str(date_)
    if text != "":
        user.Search = [text]
    user.Store_json = True
    user.Output = "response.json"
    try:
        twint.run.Search(user)
    except KeyboardInterrupt:
        print("...")
        print(constants.corp)
        sys.exit()
    print("checking object")
    return "json stored"

#Build mock twitter dataset
def find_trends():
    print("[*] looking for trends")
    obj = open('response.json', "r")
    for i in obj.readlines():
        print("[!] Building DATASET")
        cn = i.split("\n")
        js1 = cn[0] # prepare to load json
        js2 = json.loads(js1)
        trend.analyze_data(js2['tweet'], js2['username'], js2['name'])
#
def md5(string):
    md5encrypt = "http://api.hashify.net/hash/md4/hex?value=" + str(string)
    encrypt = requests.get(md5encrypt)
    json_ = encrypt.json()
    final_string = json_['Digest']
    return final_string
#Mock UI
def user_interface():
    myF = input("[*] custom search? (y/n) ")
    if myF == "y":
        username = input("Enter a twitter username: ")
        searchstring = input("Enter a search string: ")
        if username == "":
            print("You never entered a username!!")
            sys.exit()
        if searchstring == "":
            twitter_intel(username)
        else:
            twitter_intel(username, searchstring)
    elif myF == "n":
        top = open("top.txt", "r")
        for i in top.readlines():
            clean_ = i.split("\n")
            name = clean_[0]
            try:
                daily = open("daily.txt", "r")
                for j in daily.readlines():
                    corp_ = j.split("\n")
                    corp = corp_[0]
                    constants.corp[corp] = 0
                    twitter_intel(name, corp)
            except KeyboardInterrupt:
                print("oops")

def clean_():
    with open("response.json", "w") as a, open("daily.txt", "w") as b:
        a,b.write("")

clean_()
print("[*] Gathering third party intel...")
trend = Trends.TrendResearch()
#trend.nlp_()
trend.researchBot()
print("[*] Top trenders =>")
daily = open("daily.txt", "r")
for i in daily.readlines():
    print(i)
daily.close()
print("[*] Starting user interface...")
user_interface()
find_trends()
graph = Graph.Graph(constants.corp)
graph.graph1()
