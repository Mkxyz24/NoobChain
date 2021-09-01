from StringUtil import StringUtil
from TransactionOutput import TransactionOutput


class Transaction:
    '''
    make transactions
    each transaction holds:
    1) public keys of sender and receiver
    2) amount to be transferred
    3) inputs (reference to previous transactions to verify if sender has sufficient funds)
    4) outputs (shows the amount after transactions, to be used as inputs in futher transactions)
    '''

    _sequence = 0          #rough count of generated transactions

    def __init__(self, from_addr, to_addr, value, inputs):
        self.sender = from_addr
        self.recepient = to_addr
        self.value = value
        self.inputs = inputs
        self.outputs = []
        self.transactionId = None


    def calculateHash(self):
        Transaction._sequence = Transaction._sequence+1
        return StringUtil().applySha256(
                                StringUtil().getStringFromKey(self.sender) +
                                StringUtil().getStringFromKey(self.recepient) +
                                str(self.value) + str(Transaction._sequence)
                                )

    def generateSignature(self, privateKey):
        data = StringUtil().getStringFromKey(self.sender) + StringUtil().getStringFromKey(self.recepient) +str(self.value)
        self.signature = StringUtil().applyECDSASig(privateKey,bytes(data,'ascii'))

    def verifySignature(self):
        data = StringUtil().getStringFromKey(self.sender) + StringUtil().getStringFromKey(self.recepient) +str(self.value)
        return StringUtil().verifyECDSASig(self.sender, bytes(data,'ascii'), self.signature)

    def processTransaction(self,chain):
        if(self.verifySignature() == False):
            print("#Transaction Signature failed to verify")
            return False
        #gather Transaction inputs (make sure they are unspent)
        for i in self.inputs:
            i.UTXO = chain.UTXOs[i.transactionOutputId]
        
        #check if transaction is valid
        if (self.getInputsValue() < chain.minimumTransaction):
            print("Transaction inputs too small" + self.getInputsValue())
            return False

        #generate Transaction Outputs
        leftOver = self.getInputsValue() - self.value
        self.transactionId = self.calculateHash()
        self.outputs.append(TransactionOutput(self.recepient,self.value,self.transactionId))
        self.outputs.append(TransactionOutput(self.sender,leftOver,self.transactionId))

        #add outputs to unspent list
        for o in self.outputs:
            chain.UTXOs[o.id] = o

        #remove transaction inputs from UTXO lists as spent
        for i in self.inputs:
            if i.UTXO == None:
                continue
            del chain.UTXOs[i.UTXO.id]

        return True

    def getInputsValue(self):
        total = 0
        for i in self.inputs:
            if i.UTXO == None:
                continue
            total = total + i.UTXO.value
        return total

    def getOutputsValue(self):
        total = 0
        for o in self.outputs:
            total = total + o.value
        return total

