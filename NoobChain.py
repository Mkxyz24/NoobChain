from datetime import datetime
from StringUtil import StringUtil
import json


class Block:

    def __init__(self, data, previousHash):
        
        self.data = data
        self.previousHash = previousHash
        self.timeStamp = datetime.now()
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):

        calculatedHash = StringUtil.applySha256(self.previousHash
                                                + self.timeStamp.strftime("%m/%d/%Y %H:%M:%S")
                                                + str(self.nonce)
                                                + self.data)
        return calculatedHash

    def mineBlock(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce = self.nonce + 1
            self.hash = self.calculateHash()
        print("Block Mined!!! : " + self.hash)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

class NoobChain:

    blockchain = []
    difficulty = 5

    def isChainValid(self):
        #loop through blockchain to check hashes
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

        self.blockchain.append(Block("Hi im the first block", "0"))
        print("Trying to Mine block 1... ")
        self.blockchain[0].mineBlock(self.difficulty)

        self.blockchain.append(Block("Yo im the second block", self.blockchain[-1].hash))
        print("Trying to Mine block 2... ")
        self.blockchain[1].mineBlock(self.difficulty)

        self.blockchain.append(Block("Hey im the third block", self.blockchain[-1].hash))
        print("Trying to Mine block 3... ")
        self.blockchain[2].mineBlock(self.difficulty)

        print("Blockchain is Valid: " + str(self.isChainValid()))

        print("THE BLOCKCHAIN: ")
        json_chain = json.dumps([block.__dict__ for block in self.blockchain], default=json_serial, indent=1)
        print(json_chain)


if __name__ == '__main__':
    NoobChain().main()
