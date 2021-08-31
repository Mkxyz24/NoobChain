import hashlib
import base64
#import ecdsa
from cryptography.hazmat.primitives.serialization import Encoding,PrivateFormat,PublicFormat,NoEncryption
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey,EllipticCurvePublicKey,ECDSA
from cryptography.hazmat.primitives import hashes

class StringUtil:

    def applySha256(str_in):
        try:
            return hashlib.sha256(str_in.encode()).hexdigest()
        except Exception as e:
            print(e)

    def getStringFromKey(key):
        if isinstance(key, EllipticCurvePrivateKey):
            base64_bytes =  key.private_bytes(encoding=Encoding.PEM,
                                                format=PrivateFormat.TraditionalOpenSSL,
                                                encryption_algorithm=NoEncryption()
                                                                )
        elif isinstance(key, EllipticCurvePublicKey):
            base64_bytes =  key.public_bytes(encoding=Encoding.PEM,
                                                format=PublicFormat.SubjectPublicKeyInfo)
        return base64_bytes.decode("ascii")

    def applyECDSASig(privateKey, input):
        try:
            signature = privateKey.sign(
                input,
                ECDSA(hashes.SHA256())
            )
        except Exception as e:
            raise RuntimeError(e)
        return signature
    
    def verifyECDSASig(publicKey, data, signature):
        try:
            publicKey.verify(signature,data,ECDSA(hashes.SHA256()))
        except Exception as e:
            raise RuntimeError(e)
        else:
            return True

    # def applyECDSASig(privateKey, input):
    #     try:
    #         signingKey = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    #         #verifyingKey = signingKey.get_verifying_key()
    #         signature = signingKey.sign(bytes(input, 'ascii'))
    #     except Exception as e:
    #         raise RuntimeError(e)
    #     return signature

    # def verifyECDSASig(publicKey, data, signature):
    #     try:
    #         verifyingKey = ecdsa.VerifyingKey.from_string(bytes.fromhex(publicKey), curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    #         return verifyingKey(bytes.fromhex(signature), data)
    #     except Exception as e:
    #         raise RuntimeError(e)

