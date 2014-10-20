#!/usr/bin/python

from pprint import pprint
from coinhouse_btc_api_wrapper import CoinhouseBtcApiWrapper

api = CoinhouseBtcApiWrapper()

print('\nget addresses/needed/')
json = api.how_many_addresses_are_needed()
pprint(json)

print('\npost addresses/')
address = '1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX'
json = api.give_new_addresses(address)
pprint(json)

print('\npatch addresses/:the_hash')
balance = 1.3
json = api.register_payment(address, balance)
pprint(json)

print('\npath addresses/:the_hash')
json = api.try_clearance(address, balance)
pprint(json)


