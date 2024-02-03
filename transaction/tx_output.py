import json

class TransactionOutput:
    def __init__(self, pubkey_hash, amount):
        self.amount = amount
        self.pubkey_hash = pubkey_hash

    def to_json(self):
        return json.dumps({
            "amount": self.amount,
            "public_key_hash": self.pubkey_hash
        })