import json

class TransactionInput:
    def __init__(self, tx_hash, output_index, pubkey, signature) -> None:
        self.tx_hash = tx_hash
        self.output_index = output_index
        self.pubkey = pubkey
        self.signature = signature
    def to_json(self, with_pub_and_signature=True):
        if with_pub_and_signature:
            return json.dumps({
                "transaction_hash": self.tx_hash,
                "output_index": self.output_index,
                "public_key": self.pubkey,
                "signature": self.signature
            })
        else:
            return json.dumps({
                "transaction_hash": self.tx_hash,
                "output_index": self.output_index
            })