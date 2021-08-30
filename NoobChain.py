from datetime import datetime
from StringUtil import StringUtil


class Block:

    def __init__(self, data, previousHash):
        
        self.data = data
        self.previousHash = previousHash
        self.timeStamp = datetime.now()
        self.hash = self.calculateHash()

    def calculateHash(self):

        calculatedHash = StringUtil.applySha256(self.previousHash
                                                + self.timeStamp.strftime("%m/%d/%Y %H:%M:%S")
                                                + self.data)
        return calculatedHash


if __name__ == "__main__":

    genesisBlock = Block("Hi im the first block", "0")
    print("Hash for block 1 : " + genesisBlock.hash)

    secondBlock = Block("Yo im the second block", genesisBlock.hash)
    print("Hash for block 2 : " + secondBlock.hash)

    thirdBlock = Block("Hey im the third block", secondBlock.hash)
    print("Hash for block 3 : " + thirdBlock.hash)