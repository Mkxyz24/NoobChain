import hashlib
class StringUtil:

    def applySha256(str_in):
        try:
            return hashlib.sha256(str_in.encode()).hexdigest()
        except Exception as e:
            print(e)