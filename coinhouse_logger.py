import logging

class CoinhouseTransactionLogger:
    def __init__(self, out_file='coinhouse_transaction.log'):
        # create logger
        self.logger = logging.getLogger('logger name')
        self.logger.setLevel(logging.DEBUG) # log all escalated at and above DEBUG

        # add a file handler
        fh = logging.FileHandler(out_file)
        fh.setLevel(logging.DEBUG) # ensure all messages are logged to file

        # create a formatter and set the formatter for the handler.
        frmt = logging.Formatter('%(asctime)s,%(levelname)s,%(account)s,%(txid)s,%(message)s')
        fh.setFormatter(frmt)

        # add the Handler to the logger
        self.logger.addHandler(fh)

    def log_transaction(self, account, txid, message):
        attr = { 'account': account, 'txid': txid }
        self.logger.info(message, extra=attr)

