import pandas as pd
import requests
import json

# Link zum Tutorial: https://www.justintodata.com/python-api-call-to-request-data/

# Datei mit Stadtviertel lesen und als Liste umwandeln
df = pd.read_excel('Berlin_Quartiers.xlsx')
areas = []
for i in df['Areas']:
    areas.append(i)

# Parameter definieren, um die YELP API zu verwenden
api_key = 'sy7Tf3DraMboZ23tUG08JwyvJBs5-jGNsyVyOLVbkrid5OzniEPnXO8VScBtRHVxZWI9WV5d3VVbqNku9rvFNqNmxg5LUrzpLduvSGrIWSYP6tpffOiV4u634tFNYHYx'

headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'


data = []

# Liste mit der Anzahl Stadtviertel, um über diese zu iterieren
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]


# Kategorien zu sammeln: 'food,restaurants,shopping,beautysvc,collegeuniv,elementaryschools,highschools,privateschools,hospitals,nightlife,arts,parks'

for x in numbers:
    loc = str(areas[x])+', Berlin'
    for offset in range(0, 1000, 50):
        params = {
            'limit': 50, 
            'location': loc,
            'categories': 'parks',
            'offset': offset
        }
    
        response = requests.get(search_api_url, headers=headers, params=params)
        if response.status_code == 200:
            data += response.json()['businesses']
        elif response.status_code == 400:
            print('400 Bad Request')
            break

# Gesammelte Daten als JSON-Datei speichern
with open('yelp_data_berlin.json', 'a+', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

