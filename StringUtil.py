import hashlib
from cryptography.hazmat.primitives.serialization import Encoding,PrivateFormat,PublicFormat,NoEncryption
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey,EllipticCurvePublicKey,ECDSA
from cryptography.hazmat.primitives import hashes


class StringUtil:

    def applySha256(self,str_in):
        try:
            return hashlib.sha256(str_in.encode()).hexdigest()
        except Exception as e:
            print(e)

    def getStringFromKey(self,key):
        if isinstance(key, EllipticCurvePrivateKey):
            base64_bytes =  key.private_bytes(encoding=Encoding.PEM,
                                                format=PrivateFormat.TraditionalOpenSSL,
                                                encryption_algorithm=NoEncryption()
                                                                )
        elif isinstance(key, EllipticCurvePublicKey):
            base64_bytes =  key.public_bytes(encoding=Encoding.PEM,
                                                format=PublicFormat.SubjectPublicKeyInfo)
        return base64_bytes.decode("ascii")

    def applyECDSASig(self,privateKey, input):
        try:
            signature = privateKey.sign(
                input,
                ECDSA(hashes.SHA256())
            )
        except Exception as e:
            raise RuntimeError(e)
        return signature
    
    def verifyECDSASig(self,publicKey, data, signature):
        try:
            publicKey.verify(signature,data,ECDSA(hashes.SHA256()))
        except:
            return False
            #raise RuntimeError(e)
        else:
            return True

    def getDifficultyString(self,difficulty):
        return "0"*difficulty

    def getMerkleRoot(self, transactions):
        count = len(transactions)

        previousTreeLayer = []
        for transaction in transactions:
            previousTreeLayer.append(transaction.transactionId)

        treeLayer = previousTreeLayer

        while(count > 1):
            treeLayer = []
            for i in range(1, len(previousTreeLayer), 2):
                treeLayer.append(self.applySha256(previousTreeLayer[i-1] + previousTreeLayer[i]))
            count = len(treeLayer)
            previousTreeLayer = treeLayer
        
        if len(treeLayer) == 1:
            merkleRoot = treeLayer[0]
        else:
            merkleRoot = ""
        
        return merkleRoot


