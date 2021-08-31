'''
A blockchain with simple proof of work mining system
Functionality to send signed transactions using simple wallet
'''


from datetime import datetime
from typing import Sequence
from StringUtil import StringUtil
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

class Block:
    '''
    Block class to hold information about transactions in blocks.
    Each block has its own hash (A digital fingerprint) which is calculated using previous hash
    Blocks are mined by finding a hash lower than target value (Proof of work system)
    '''
    def __init__(self, data, previousHash):
        '''
        Initializing block with data and hashes
        '''
        self.data = data
        self.previousHash = previousHash
        self.timeStamp = datetime.now()
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):
        '''
        Hash calculator using sha256 algorithm
        '''
        calculatedHash = StringUtil.applySha256(self.previousHash
                                                + self.timeStamp.strftime("%m/%d/%Y %H:%M:%S")
                                                + str(self.nonce)
                                                + self.data)
        return calculatedHash

    def mineBlock(self, difficulty):
        '''
        Proof of work algorithm to find hash that is lower than the target hash
        '''
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce = self.nonce + 1
            self.hash = self.calculateHash()
        print("Block Mined!!! : " + self.hash)

class Wallet:
    '''
    Simple wallet to store address 
    '''
    def __init__(self):
        self.generateKeyPair()
    
    def generateKeyPair(self):
        try:
            self.privateKey = ec.generate_private_key(curve= ec.SECP256K1)
            self.publicKey = self.privateKey.public_key()
        except Exception as e:
            raise RuntimeError(e)

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

    def __init__(self, from_addr, to_addr, value, inputs)  :
        self.sender = from_addr
        self.recepient = to_addr
        self.value = value
        self.inputs = inputs

    def calculateHash(self):
        Transaction._sequence = Transaction._sequence+1
        return StringUtil.applySha256(
                                StringUtil.getStringFromKey(self.sender) +
                                StringUtil.getStringFromKey(self.recepient) +
                                str(self.value) + Transaction._equence
                                )

    def generateSignature(self, privateKey):
        data = StringUtil.getStringFromKey(self.sender) + StringUtil.getStringFromKey(self.recepient) +str(self.value)
        self.signature = StringUtil.applyECDSASig(privateKey,bytes(data,'ascii'))

    def verifySignature(self):
        data = StringUtil.getStringFromKey(self.sender) + StringUtil.getStringFromKey(self.recepient) +str(self.value)
        return StringUtil.verifyECDSASig(self.sender, bytes(data,'ascii'), self.signature)



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
    difficulty = 5


    def isChainValid(self):
        #loop through blockchain to check hashes consistency
        hashTarget = "0"*self.difficulty
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
        return True
    


    def main(self):
        '''
        verbose function
        '''

        walletA = Wallet()
        walletB = Wallet()
        
        #test public and private keys
        print("Private and public keys: ")
        print(StringUtil.getStringFromKey(walletA.privateKey))
        print(StringUtil.getStringFromKey(walletA.publicKey))

        #Test transaction from walletA to walletB
        transaction = Transaction(walletA.publicKey,walletB.publicKey,5,None)
        transaction.generateSignature(walletA.privateKey)

        #verify signature 
        print("is signature verified")
        print(transaction.verifySignature())

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
