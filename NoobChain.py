'''
A blockchain with simple proof of work mining system
Functionality to send signed transactions using simple wallet
'''



from datetime import datetime
from hashlib import new
from typing import Sequence
from StringUtil import StringUtil
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from TransactionInput import TransactionInput
from TransactionOutput import TransactionOutput

class Block:
    '''
    Block class to hold information about transactions in blocks.
    Each block has its own hash (A digital fingerprint) which is calculated using previous hash
    Blocks are mined by finding a hash lower than target value (Proof of work system)
    '''
    def __init__(self, previousHash):
        '''
        Initializing block with data and hashes
        '''
        self.previousHash = previousHash
        self.timeStamp = datetime.now()
        self.nonce = 0
        self.merkleRoot = ""
        self.transactions = []
        self.hash = self.calculateHash()


    def calculateHash(self):
        '''
        Hash calculator using sha256 algorithm
        '''
        calculatedHash = StringUtil().applySha256(self.previousHash
                                                + self.timeStamp.strftime("%m/%d/%Y %H:%M:%S")
                                                + str(self.nonce)
                                                + self.merkleRoot)
        return calculatedHash

    def mineBlock(self, difficulty):
        '''
        Proof of work algorithm to find hash that is lower than the target hash
        '''
        self.merkleRoot = StringUtil().getMerkleRoot(transactions = self.transactions)
        target = StringUtil().getDifficultyString(difficulty)
        while self.hash[:difficulty] != target:
            self.nonce = self.nonce + 1
            self.hash = self.calculateHash()
        print("Block Mined!!! : " + self.hash)

    def addTransaction(self, transaction):
        if(transaction==None):
            return False
        if self.previousHash != "0":
            if transaction.processTransaction() != True:
                print("Transaction failed to process. Discarded")
                return False
        self.transactions.append(transaction)
        print("Transaction Successfully added to Block")
        return True

class Wallet:
    '''
    Simple wallet to store address 
    '''
    UTXOs = {}
    def __init__(self):
        self.generateKeyPair()
    
    def generateKeyPair(self):
        try:
            self.privateKey = ec.generate_private_key(curve= ec.SECP256K1)
            self.publicKey = self.privateKey.public_key()
        except Exception as e:
            raise RuntimeError(e)
    
    def getBalance(self):
        total = 0
        for id,o in NoobChain.UTXOs.items():
            UTXO = o
            if UTXO.isMine(self.publicKey):
                self.UTXOs[UTXO.id] = UTXO
                total = total + UTXO.value
        return total

    def sendFunds(self,_recipient,value):
        if(self.getBalance()<value):
            print("not enough funds to send transaction. Transaction Discarded!")
            return None

        #create list of inputs
        inputs = []
        
        total = 0
        for id,o in self.UTXOs.items():
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

class Transaction:
    '''
    make transactions
    each transaction holds:
    1) public keys of sender and receiver
    2) amount to be transferred
    3) inputs (reference to previous transactions to verify if sender has sufficient funds)
    4) outputs (shows the amount after transactions, to be used as inputs in futher transactions)
    '''
    inputs = []
    outputs = []
    _sequence = 0          #rough count of generated transactions
    transactionId = None

    def __init__(self, from_addr, to_addr, value, inputs)  :
        self.sender = from_addr
        self.recepient = to_addr
        self.value = value
        self.inputs = inputs

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

    def processTransaction(self):
        if(self.verifySignature() == False):
            print("#Transaction Signature failed to verify")
            return False
        #gather Transaction inputs (make sure they are unspent)
        for i in self.inputs:
            i.UTXO = NoobChain.UTXOs[i.transactionOutputId]
        
        #check if transaction is valid
        if (self.getInputsValue() < NoobChain.minimumTransaction):
            print("Transaction inputs too small" + self.getInputsValue())
            return False

        #generate Transaction Outputs
        leftOver = self.getInputsValue() - self.value
        self.transactionId = self.calculateHash()
        self.outputs.append(TransactionOutput(self.recepient,self.value,self.transactionId))
        self.outputs.append(TransactionOutput(self.sender,leftOver,self.transactionId))

        #add outputs to unspent list
        for o in self.outputs:
            NoobChain.UTXOs[o.id] = o

        #remove transaction inputs from UTXO lists as spent
        for i in self.inputs:
            if i.UTXO == None:
                continue
            del NoobChain.UTXOs[i.UTXO.id]

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



        

def json_serial(obj):
    '''
    JSON serializer for objects not serializable by default json code
    '''

    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

class NoobChain:
    '''
    The main class of the blockchain
    Just some useful functions nothing special
    
    '''
    blockchain = []
    difficulty = 3
    UTXOs = {}
    minimumTransaction = 0.1
    

    def isChainValid(self):
        #loop through blockchain to check hashes consistency
        hashTarget = "0"*self.difficulty
        tempUTXOs = {}
        tempUTXOs[self.genesisTransaction.outputs[0].id] = self.genesisTransaction.outputs[0]

        for i in range(1,len(self.blockchain)):
            currentBlock = self.blockchain[i]
            previousBlock = self.blockchain[i-1]
            #compare registered hash and calculated hash
            if(currentBlock.hash != currentBlock.calculateHash()):
                print("Current Hashes not equal")
                return False
            #compare previous hash and registered previous hash
            if(previousBlock.hash != currentBlock.previousHash):
                print("Previous Hashes not equal")
                return False
            #check if hash is solved
            if(currentBlock.hash[:self.difficulty] != hashTarget):
                print("This block hasn't been mined")
                return False
            #blockchain transactions
            for t in range(len(currentBlock.transactions)):
                currentTransaction = currentBlock.transactions[t]

                if currentTransaction.verifySignature() == False:
                    print("#Signature on Transaction(" + str(t) + ") is Invalid")
                    return False
                if currentTransaction.getInputsValue() != currentTransaction.getOutputsValue():
                    print("#Inputs are not equal to outputs on Transaction(" + str(t) + ")")
                    return False
                
                for input in currentTransaction.inputs:
                    tempOutput = tempUTXOs[input.transactionOutputId]
                    if tempOutput == None:
                        print("#Referenced input on Transaction(" + str(t) + ") is Missing")
                        return False
                    if input.UTXO.value != tempOutput.value:
                        print("#Referenced input Transaction(" + str(t) + ") value is Invalid")
                        return False
                    del tempUTXOs[input.transactionOutputId]
                
                for output in currentTransaction.outputs:
                    tempUTXOs[output.id] = output
                
                if currentTransaction.outputs[0].recipient != currentTransaction.recipient:
                    print("#Transaction(" + str(t) + ") output recipient is not who it should be")
                    return False
                if currentTransaction.outputs[1].recipient != currentTransaction.sender:
                    print("#Transaction(" + str(t) + ") output 'change' is not sender.")
                    return False
        print("Blockchain is valid")
        return True
    
    def addBlock(self, newBlock):
        newBlock.mineBlock(self.difficulty)
        self.blockchain.append(newBlock)

    def main(self):
        '''
        verbose function
        '''

        walletA = Wallet()
        walletB = Wallet()
        coinbase = Wallet()

        #create genesis transaction, which sends 100 NoobCoin to walletA
        self.genesisTransaction = Transaction(coinbase.publicKey, walletA.publicKey, 100, None)
        self.genesisTransaction.generateSignature(coinbase.privateKey)
        self.genesisTransaction.transactionId = "0"
        self.genesisTransaction.outputs.append(TransactionOutput(self.genesisTransaction.recepient,
                                                            self.genesisTransaction.value,
                                                            self.genesisTransaction.transactionId))
        self.UTXOs[self.genesisTransaction.outputs[0].id] = self.genesisTransaction.outputs[0]

        print("creating and mining Genesis Block... ")
        genesis = Block("0")
        genesis.addTransaction(self.genesisTransaction)
        self.addBlock(genesis)

        #testing
        block1 = Block(genesis.hash)
        print("WalletA's balance is: ",walletA.getBalance())
        print("WalletA is attempting to send funds(40) to WalletB")
        block1.addTransaction(walletA.sendFunds(walletB.publicKey,40))
        self.addBlock(block1)
        print("WalletA's balance is: ",walletA.getBalance())
        print("walletB's balance is: ", walletB.getBalance())

        block2 = Block(block1.hash)
        #print("WalletA's balance is: ",walletA.getBalance())
        print("WalletA is attempting to send more funds(1000) than it has.")
        block2.addTransaction(walletA.sendFunds(walletB.publicKey,1000))
        self.addBlock(block2)
        print("WalletA's balance is: ",walletA.getBalance())
        print("walletB's balance is: ", walletB.getBalance())

        block3 = Block(block2.hash)
        #print("WalletA's balance is: ",walletA.getBalance())
        print("WalletB is attempting to send funds(20) to WalletA")
        block3.addTransaction(walletB.sendFunds(walletA.publicKey,20))
        #self.addBlock(block3)
        print("WalletA's balance is: ",walletA.getBalance())
        print("walletB's balance is: ", walletB.getBalance())

        self.isChainValid()



        # #test public and private keys
        # print("Private and public keys: ")
        # print(StringUtil().getStringFromKey(walletA.privateKey))
        # print(StringUtil().getStringFromKey(walletA.publicKey))

        # #Test transaction from walletA to walletB
        # transaction = Transaction(walletA.publicKey,walletB.publicKey,5,None)
        # transaction.generateSignature(walletA.privateKey)

        # #verify signature 
        # print("is signature verified")
        # print(transaction.verifySignature())

        # self.blockchain.append(Block("Hi im the first block", "0"))
        # print("Trying to Mine block 1... ")
        # self.blockchain[0].mineBlock(self.difficulty)

        # self.blockchain.append(Block("Yo im the second block", self.blockchain[-1].hash))
        # print("Trying to Mine block 2... ")
        # self.blockchain[1].mineBlock(self.difficulty)

        # self.blockchain.append(Block("Hey im the third block", self.blockchain[-1].hash))
        # print("Trying to Mine block 3... ")
        # self.blockchain[2].mineBlock(self.difficulty)

        # print("Blockchain is Valid: " + str(self.isChainValid()))

        # print("THE BLOCKCHAIN: ")
        # json_chain = json.dumps([block.__dict__ for block in self.blockchain], default=json_serial, indent=1)
        # print(json_chain)


if __name__ == '__main__':
    NoobChain().main()
