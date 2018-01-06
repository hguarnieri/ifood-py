import requests
import json

ACCESS_KEY = '69f181d5-0046-4221-b7b2-deef62bd60d5'
SECRET_KEY = '9ef4fb4f-7a1d-4e0d-a9b1-9b82873297d8'

CEP = '01311300'

MIN_DISCOUNT = 0.3
MIN_PRICE = 1

SHOULD_BE_CLOSED = False

def decode(val):
    return u'{}'.format(val).encode('utf-8')

def print_restaurant(obj):
    print('Restaurant name: {}'.format(decode(obj['name'])))

def print_promo(obj):
    print('Promo name: {}\nPrice: {}\n'.format(decode(obj['description']), obj['unitPrice']))

def check_min_price_restaurant(obj):
    url = 'https://wsloja.ifood.com.br/ifood-ws-v3/restaurant/menu?restaurantId={}'.format(obj['restaurantId'])
    headers = {'User-Agent': 'Special',
    'Host': 'wsloja.ifood.com.br',
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'session_token': session_token,
    'Cookie': jsessionid}

    r = requests.get(url, headers=headers)

    data = json.loads(r.text)

    try:
        printed = False
        for promo in data['data']['menu'][0]['itens']:
            originalPrice = promo['unitOriginalPrice']
            unitPrice = promo['unitPrice']
            discount = originalPrice - unitPrice
            percentage = discount / originalPrice

            if percentage > MIN_DISCOUNT and unitPrice > MIN_PRICE:
                if not printed:
                    print_restaurant(obj)
                    printed = True
                print('Found with {0:.2f}% of discount'.format(percentage * 100))
                print_promo(promo)
    except Exception as ex:
            """"""

# get session tokens
url = 'https://wsloja.ifood.com.br/ifood-ws-v3/app/config'
headers = {'access_key': ACCESS_KEY,
            'secret_key': SECRET_KEY,
            'Host': 'wsloja.ifood.com.br',
            'User-Agent': 'special'}

r = requests.get(url, headers=headers)

session_token = r.headers['session_token']
set_cookies = r.headers['Set-Cookie']
jsessionid = set_cookies[0:set_cookies.find(';')]

# get region_id
url = 'https://wsloja.ifood.com.br/ifood-ws-v3/address/locationsByZipCode?zipCode={}'.format(CEP)
headers = {'User-Agent': 'Special',
'Host': 'wsloja.ifood.com.br',
'session_token': session_token,
'Cookie': jsessionid}

r = requests.get(url, headers=headers)
data = json.loads(r.text)

location_id = data['data']['locations'][0]['locationId']

# get restaurant list
url = 'https://wsloja.ifood.com.br/ifood-ws-v3/restaurant/list'
headers = {'User-Agent': 'Special',
'Host': 'wsloja.ifood.com.br',
'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
'session_token': session_token,
'Cookie': jsessionid}

filters = 'filterJson=' + '{"cuisineTypes":[], "delivery":true, ' \
                            '"freeDeliveryFee":"true", "locationId": ' + str(location_id) + ',' \
                            '"page":1, "pageSize":5000, "paymentType":[],' \
                            '"sort":"0", "togo":false}'

r = requests.post(url, headers=headers, data=filters)
data = json.loads(r.text)

# find the best prices
for obj in data['data']['list']:
    if obj['closed'] == SHOULD_BE_CLOSED:
        check_min_price_restaurant(obj)
