from datetime import datetime
from StringUtil import StringUtil


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

    def addTransaction(self, transaction, chain):
        if(transaction==None):
            return False
        if self.previousHash != "0":
            if transaction.processTransaction(chain) != True:
                print("Transaction failed to process. Discarded")
                return False
        self.transactions.append(transaction)
        print("Transaction Successfully added to Block")
        return True