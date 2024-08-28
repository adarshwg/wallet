
class TransactionID:
    def __init__(self):
        with open('transaction_id_store.txt','r+') as file:
            transaction_id = int(file.read())
            file.seek(0)
            file.write(f'{transaction_id+1}')
        self.transaction_id = transaction_id

    def get_transaction_id(self):
        return self.transaction_id





