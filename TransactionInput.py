
class TransactionInput:
    UTXO = None #Contains the Unspent transaction output
    def __init__(self,transactionOutputId):
        self.transactionOutputId = transactionOutputId
