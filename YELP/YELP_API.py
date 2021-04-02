import requests
import json

#Link to Tutorial: https://www.justintodata.com/python-api-call-to-request-data/

#INSERT YOUR API KEY BETWEEN THE QUOTATION MARKS
api_key = ''

headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'


data = []

for offset in range(0, 1000, 50):
        params = {
            'limit': 50, 
            'location': 'Aldgate, London',
            'categories': 'food, restaurants, shopping, beautysvc',
            'offset': offset
        }

        response = requests.get(search_api_url, headers=headers, params=params)
        if response.status_code == 200:
            data += response.json()['businesses']
        elif response.status_code == 400:
            print('400 Bad Request')
            break

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)