#!/usr/bin/python

from datetime import datetime
import requests

class CoinhouseBtcApiWrapper:
    def __init__(self, hostname = 'http://coinhouseweb:3000/btc/'):
        self.base_uri = hostname
        r= requests.get(self.base_uri + 'info', allow_redirects=False)
        r.raise_for_status()
        self.log_liveness()

    def log_liveness(self):
        self.last_alive = datetime.now().time()

    def get_last_alive(self):
        return self.last_alive

    # GET addresses/needed
    def how_many_addresses_are_needed(self):
        loc = self.base_uri + 'addresses/needed'
        r = requests.get(loc, allow_redirects=False)
        r.raise_for_status()
        self.log_liveness()
        return r.json()

    # POST addresses
    def give_new_addresses(self, address):
        loc = self.base_uri + 'addresses'
        payload = { 'the_hash': address }
        r = requests.post(loc, data=payload, allow_redirects=False)
        r.raise_for_status()
        self.log_liveness()
        return r.json()

    # PATCH addresses/:id
    def register_payment(self, address, balance):
        loc = self.base_uri + 'addresses/' + address
        payload = { 'balance': balance }
        r = requests.patch(loc, data=payload, allow_redirects=False)
        r.raise_for_status()
        self.log_liveness()
        return r.json()

    # PATCH addresses/:id/try_clearance
    def try_clearance(self, address, balance):
        loc = self.base_uri + 'addresses/' + address  + '/try_clearance'
        payload = { 'balance': balance }
        r = requests.patch(loc, data=payload, allow_redirects=False)
        r.raise_for_status()
        self.log_liveness()
        return r.json()
