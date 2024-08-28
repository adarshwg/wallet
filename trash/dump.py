# import requests
#
# url = "https://currency-exchange.p.rapidapi.com/listquotes"
#
# headers = {
# 	"x-rapidapi-key": "07b3b4645emsh09fd09ab354951ap150633jsn0f22efb145ff",
# 	"x-rapidapi-host": "currency-exchange.p.rapidapi.com"
# }
#
# response = requests.get(url, headers=headers)
#
# print(response.json())

import functools
import requests


class OpenExchangeClient:
    BASE_URL = "https://openexchangerates.org/api"

    def __init__(self, app_id):
        self.app_id = app_id

    @property
    @functools.lru_cache(maxsize=2)
    #least recently used - maxsize - data that's used frequently
    # defines how many elements will stay in the cache
    def latest(self):
        return requests.get(f'{self.BASE_URL}/latest.json?app_id={self.app_id}').json()

    def convert(self, amount, curr_currency, new_currency):
        rates = self.latest['rates']
        to_rate = rates[new_currency]
        if curr_currency == 'USD':
            return amount * to_rate
        else :
            usd_amount= amount/rates[curr_currency]
            return usd_amount* to_rate

op = OpenExchangeClient()