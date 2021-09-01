from StringUtil import StringUtil

class TransactionOutput:
    def __init__(self, recepient, value, parentTransactionId):
        self.recepient = recepient
        self.value = value
        self.parentTransactionId = parentTransactionId
        self.id = StringUtil().applySha256(
            StringUtil().getStringFromKey(recepient) +
            str(value) +
            parentTransactionId
        )


    def isMine(self,publicKey):
        '''
        check if coin belongs to you
        '''
        return (publicKey == self.recepient)
