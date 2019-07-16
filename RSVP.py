from bs4 import BeautifulSoup
import requests
import time
import re

class Scraper:
    def __init__(self,party):
        domain = r'(?<=whenisgood\.net).*'
        m = re.search(domain,party)
        if m.group(0):
            self._party = m.group(0)
        else:
            self._party = party
        self._groups ={}
        self._days
    
    @property
    def party(self):
        return self._party
    @party.setter
    def party(self,value):
        self._party=value

    @property
    def groups(self):
        return self._groups
    @groups.setter
    def groups(self,value):
        value[0]=key
        value[1]=value
        if key not in self._groups.keys():
            self._groups.update({key: [value]})
        elif value not in self._groups[key]:
            self._groups.update({key: self._groups[key].extend(value)})
            else:
                x.update({key: list(set(x[key] + y[key]))})  

    def go_scrape(self):
        url="whenisgood.net"+self._party
        req = requests.get(url)
        soup=BeautifulSoup(req.content,'html.parser')
        days=soup.find_all("td",{'class': 'proposed'})
        day_links = []
        for day in days:
            link = re.search(r'(?<=pop\(\').+?(?=\')',day['onClick'])
            day_links.extend(link)
        for day_link in day_links:
            result = requests.get("whenisgood.net"+day_link)
            soup = BeautifulSoup(result.content,'html.parser')
            table = soup.find('table')
            rows = table.find_all('tr')
            for row in rows:
                data = row.find_all('td')
                date = 0
                group = 0
                for datum in data:
                    value = 'N/A'
                    key = []
                    if date == 1:
                        value = datum.text
                        date = 0
                    elif datum.text[:-1]=='Date':
                        date = 1
                    if group == 1:
                        names = datum.text.split(',')
                        key = [name.strip() for name in names]
                        group = 0
                    elif datum.text[:-1]=='Can make it':
                        group = 1
                    if value not 'N/A' and key:
                        self._groups = (key, value)
                        break
            print('Day processed')