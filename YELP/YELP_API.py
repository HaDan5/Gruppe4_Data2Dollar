import requests

#Link to Tutorial: https://www.justintodata.com/python-api-call-to-request-data/

#INSERT YOUR API KEY BETWEEN THE QUOTATION MARKS
api_key = ''

headers = {'Authorization': 'Bearer {}'.format(api_key)}
search_api_url = 'https://api.yelp.com/v3/businesses/search'
params = {'term': 'coffee', 
          'location': 'Toronto, Ontario',
          'limit': 50}


response = requests.get(search_api_url, headers=headers, params=params, timeout=5)


print(response.url)
print(response.status_code)

data_dict = response.content

with open('data.json', 'wb') as f:
    f.write(data_dict)