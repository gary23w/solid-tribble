import datetime
import requests
from bs4 import BeautifulSoup
from data import constants

class TrendResearch():

    def __init__(self):
        print("Searching for latest trends")

    def researchBot(self):
        print(datetime.date.today())
        url = "https://finance.yahoo.com/gainers"
        crawl = requests.session()
        response = crawl.get(url)
        soup = BeautifulSoup(response.content, "lxml")
        for i in soup.find_all('a', class_="Fw(600)"):
            daily = open("daily.txt", "a")
            daily.write(i.get_text() + "\n")
            daily.close()

    def analyze_data(self, data, user, name):
        print("User: " + user)
        print("Name: " + name)
        print("Tweet =>")
        print(data)
        print("\n")
        print(constants.corp)
        for i in constants.corp:
            if str(data).__contains__(constants.corp[i]):
                constants.corp[i] += 1


