import re

import requests
from bs4 import BeautifulSoup


url = "https://www.ign.es/web/ign/portal/sis-catalogo-terremotos/-/catalogo-terremotos/searchTerremoto?latMin=26.6412193530742&latMax=30.244734978074202&longMin=-19.694437169627594&longMax=-15.212015294627593&startDate=01/01/2010&endDate=06/11/2021&selIntensidad=N&selMagnitud=N&intMin=&intMax=&magMin=&magMax=&selProf=N&profMin=&profMax=&fases=no&cond="

html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')

if __name__ == '__main__':
    attrs = {
        'href': re.compile(r'\.mid$')
    }

    tracks = soup.find_all('a', attrs=attrs, string=re.compile(r'^((?!\().)*$'))

    count = 0
    for track in tracks:
        print(track)
        count += 1
    print(len(tracks))
