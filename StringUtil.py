import hashlib
import base64

class StringUtil:

    def applySha256(str_in):
        try:
            return hashlib.sha256(str_in.encode()).hexdigest()
        except Exception as e:
            print(e)

    def getStringFromKey(key):
        base64_bytes =  base64.b64encode(key.encode("ascii"))
        return base64_bytes.decode("ascii")