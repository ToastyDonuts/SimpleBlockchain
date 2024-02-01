from typing import Any
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from utility import calculate_hash 
from utility import create_transaction_data, convert_tx_to_byte
from Crypto.Hash import SHA256
import base58

class wallet_owner:
    def __init__(self, public_key=None, private_key=None, wallet_address=None) -> None:
        self.public_key = public_key
        self.private_key = private_key
        self.wallet_address = wallet_address

    def initialize_wallet(self):
        private_key_notencoded = ECC.generate(curve='P-256')
        public_key_notencoded = private_key_notencoded.public_key()
        self.private_key = private_key_notencoded.export_key(format='PEM')
        self.public_key = public_key_notencoded.export_key(format='DER')
        hashed_public_sha256 = calculate_hash(self.public_key, "sha256")
        hashed_public_ripemd = calculate_hash(hashed_public_sha256, "ripemd160")
        self.wallet_address = base58.b58encode(hashed_public_ripemd)
        

class transaction:
    def __init__(self, wallet_owner=None, receiver_address=None, amount=None) -> None:
        self.wallet_owner = wallet_owner
        self.receiver_address = receiver_address
        self.amount = amount
    def create_transaction(self):
        sender_address = self.wallet_owner.wallet_address
        create_transaction_data(self.receiver_address, sender_address, self.amount)
        return convert_tx_to_byte(create_transaction_data)
    def signing(self):
        transaction=self.create_transaction()
        hashed_tx=calculate_hash(transaction, "sha256")
        signing_key = DSS.new(self.wallet_owner.private_key)
        signed_transaction = DSS.DssSigScheme(signing_key).sign(hashed_tx)
        return signed_transaction

wallet = wallet_owner()
wallet.initialize_wallet()
print(wallet.private_key)
print(wallet.public_key)
print(wallet.wallet_address)
# transaction_class = transaction(wallet_owner, '4bwqYydoKmk5LYrS4Vc1tRP9yJ5rk5UZfJryAfuzNZ9L5reH3cTsAQXvsaRxbccNu4', )