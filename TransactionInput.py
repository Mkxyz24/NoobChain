class TransactionInput:
    
    def __init__(self,transactionOutputId):
        self.transactionOutputId = transactionOutputId
        self.UTXO = None #Contains the Unspent transaction output