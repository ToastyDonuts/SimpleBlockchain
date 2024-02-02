from datetime import datetime
from node_utility import Cryptographic_SHA256_Hash
import json

class Block:
    def __init__(self, transaction_data:str, timestamp:str, previous_block=None) -> None:
        self.transaction_data = transaction_data
        self.timestamp = timestamp
        self.previous_block = previous_block
    @property
    def previous_block_cryptographic_hash(self):
        if self.previous_block:
            return self.previous_block.cryptographic_hash
        return '0'
    @property
    def cryptographic_hash(self) -> str:
        block_data={
            "transaction_data": self.transaction_data,
            "timestamp": str(self.timestamp),
            "previous_block_cryptographic_hash": self.previous_block_cryptographic_hash
        }
        hash_output = Cryptographic_SHA256_Hash(json.dumps(block_data, indent=2).encode('utf-8'))
        self.hash_output = hash_output
        return hash_output
    



