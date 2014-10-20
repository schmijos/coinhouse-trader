#!/usr/bin/python
import time, sys
import logging
from pprint import pprint
from bitcoinrpc.authproxy import AuthServiceProxy
from coinhouse_btc_api_wrapper import CoinhouseBtcApiWrapper

logging.basicConfig(level=logging.DEBUG)
logging.addLevelName( logging.WARNING, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
logging.addLevelName( logging.ERROR, "\033[1;41m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

# bitcoind config
username = "bitcoinrpc"
password = "HwWVVJ1sy9uALf8fqFCvxiNzavXMmRQhSr2sTM5t1xCa"
uri = "http://{0}:{1}@127.0.0.1:8332".format(username, password)
btc_account_incoming  = "incoming"
btc_account_verifying = "verifying"
btc_account_done      = "done"

# connect to bitcoind
try:
    btcd = AuthServiceProxy(uri) # bitcoind
    logging.debug("GETINFO:")
    logging.debug(btcd.getinfo())
    logging.debug("GETPEERINFO:")
    logging.debug(btcd.getpeerinfo())
    logging.info("successfully connected to btc-jsonrpc")
except:
    logging.exception('could not connect to btc-jsonrpc')
    sys.exit()


# connect to coinhouse btc api
try:
    ch_api = CoinhouseBtcApiWrapper() # coinhouse api
    logging.info("successfully connected to coinhouse api")
except:
    logging.exception("could not connect to coinhouse api")
    sys.exit()


# provide btc addresses to rails and try to clear transactions periodically
round = 0;
while True:
    try:
        round += 1

        # check, how many new addresses coinhouse needs
        address_gen_count = ch_api.how_many_addresses_are_needed()
        # generate and get new addresses from bitcoind
        new_addresses = list(btcd.getnewaddress(btc_account_incoming) for n in range(address_gen_count))
        # register addresses in rails for showing them to end users
        for address in new_addresses:
            ch_api.give_new_addresses(address)

        # check incoming addresses for balance (not yet verified). 
        # if there is enough btc on the account
        # we transfer it to verifying. otherwise it is forced to await more btcs
        incoming_addresses = btcd.getaddressesbyaccount(btc_account_incoming)
        for address in incoming_addresses:
            balance = btcd.getreceivedbyaddress(address, 0)
            if balance > 0:
                is_paid_enough = ch_api.register_payment(address, balance)
                if is_paid_enough:
                    btcd.setaccount(address, btc_account_verifying)

        # check btc verifications and clear the transaction if there 
        # are at least 2 verifications
        verifying_addresses = btcd.getaddressesbyaccount(btc_account_verifying)
        for address in verifying_addresses:
            balance = btcd.getreceivedbyaddress(address, 2)
            is_clear = ch_api.try_clearance(address, balance)
            if is_clear:
                btcd.setaccount(address, btc_account_done)

        logging.info("round %d" % round)
        time.sleep(10)

    except KeyboardInterrupt:
        logging.info("Closed. Bye!")
        sys.exit()
