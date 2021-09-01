from cryptography.hazmat.primitives.asymmetric import ec
from TransactionInput import TransactionInput
from Transaction import Transaction


class Wallet:
    '''
    Simple wallet to store address 
    '''

    def __init__(self):
        self.generateKeyPair()
        self.UTXOs = {}
        
    def generateKeyPair(self):
        try:
            self.privateKey = ec.generate_private_key(curve= ec.SECP256K1)
            self.publicKey = self.privateKey.public_key()
        except Exception as e:
            raise RuntimeError(e)
    
    def getBalance(self, chain):
        total = 0
        for o in chain.UTXOs.values():
            UTXO = o
            if UTXO.isMine(self.publicKey):
                self.UTXOs[UTXO.id] = UTXO
                total = total + UTXO.value
        return total

    def sendFunds(self,_recipient,value,chain):
        if(self.getBalance(chain)<value):
            print("not enough funds to send transaction. Transaction Discarded!")
            return None
        #create list of inputs (the unspent transactions to show sufficient funds)
        inputs = []
        
        total = 0
        for o in self.UTXOs.values():
            UTXO = o
            total = total + UTXO.value
            inputs.append(TransactionInput(UTXO.id))
            if total > value:
                break
        
        newTransaction = Transaction(self.publicKey, _recipient, value, inputs)
        newTransaction.generateSignature(self.privateKey)

        for input in inputs:
            del self.UTXOs[input.transactionOutputId]

        return newTransaction