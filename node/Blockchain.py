from datetime import datetime
from utility import Cryptographic_SHA256_Hash
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
    
genesis = Block("First", datetime.now(), None)
block1 = Block("Second", datetime.now(), genesis)
block2 = Block("Third", datetime.now(), block1)
block3 = Block("Fourth", datetime.now(), block2)
block4 = Block("Fifth", datetime.now(), block3)
block5 = Block("Sixth", datetime.now(), block4)
block6 = Block("Seventh", datetime.now(), block5)
block7 = Block("Eighth", datetime.now(), block6)
block8 = Block("Ninth", datetime.now(), block7)
block9 = Block("Tenth", datetime.now(), block8)
block10 = Block("Eleventh", datetime.now(), block9)
block11 = Block("Twelveth", datetime.now(), block10)
print(genesis.cryptographic_hash)
print(block1.cryptographic_hash)
print(block2.cryptographic_hash)
print(block3.cryptographic_hash)
print(block4.cryptographic_hash)
print(block5.cryptographic_hash)
print(block6.cryptographic_hash)
print(block7.cryptographic_hash)
print(block8.cryptographic_hash)
print(block9.cryptographic_hash)
print(block10.cryptographic_hash)
print(block11.cryptographic_hash)



