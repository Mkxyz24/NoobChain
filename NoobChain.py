'''
A blockchain with simple proof of work mining system
Functionality to send signed transactions using simple wallet
'''




from hashlib import new
from StringUtil import StringUtil
import json
from cryptography.hazmat.primitives import hashes
from TransactionOutput import TransactionOutput
from Transaction import Transaction
from Wallet import Wallet
from Block import Block
        

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
    def __init__(self):
        self.blockchain = []
        self.difficulty = 3
        self.UTXOs = {}
        self.minimumTransaction = 0.1
    

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
                    print("#Inputs(" + str(currentTransaction.getInputsValue())+ ") are not equal to outputs(" + str(currentTransaction.getOutputsValue())+ ") on Transaction(" + str(t) + ") and block: " + str(i))
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

                if currentTransaction.outputs[0].recepient != currentTransaction.recepient:
                    print("#Transaction(" + str(t) + ") output recipient is not who it should be")
                    return False
                if currentTransaction.outputs[1].recepient != currentTransaction.sender:
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
        genesis.addTransaction(self.genesisTransaction, self)
        self.addBlock(genesis)

        #testing
        block1 = Block(genesis.hash)
        print("WalletA's balance is: ",walletA.getBalance(self))
        print("WalletA is attempting to send funds(40) to WalletB")   
        block1.addTransaction(walletA.sendFunds(walletB.publicKey,40,self),self)
        self.addBlock(block1)
        print("WalletA's balance is: ",walletA.getBalance(self))
        print("walletB's balance is: ", walletB.getBalance(self))

        block2 = Block(block1.hash)
        print("WalletA is attempting to send more funds(1000) than it has.")   
        block2.addTransaction(walletA.sendFunds(walletB.publicKey,1000,self),self)
        self.addBlock(block2)
        print("WalletA's balance is: ",walletA.getBalance(self))
        print("walletB's balance is: ", walletB.getBalance(self))

        block3 = Block(block2.hash)
        print("WalletB is attempting to send funds(20) to WalletA")
        block3.addTransaction(walletB.sendFunds(walletA.publicKey,20,self),self)
        #self.addBlock(block3)
        print("WalletA's balance is: ",walletA.getBalance(self))
        print("walletB's balance is: ", walletB.getBalance(self))

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
