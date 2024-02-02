from typing import Any
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from wallet_utility import calculate_hash 
from wallet_utility import create_transaction_data, convert_tx_to_byte
from Crypto.Hash import SHA256
import os
import base58

currentpath=os.path.dirname(__file__)

class wallet_owner:
    def __init__(self, public_key=None, private_key=None, wallet_address=None) -> None:
        self.public_key = public_key
        self.private_key = private_key
        self.wallet_address = wallet_address
    def initialize_wallet(self):
        currentpath=os.path.dirname(__file__)
        num=1
        private_key_notencoded = ECC.generate(curve='P-256')
        public_key_notencoded = private_key_notencoded.public_key()
        while os.path.isfile(f'{currentpath}/keys/privatekey{num}.pem'):
            num=num+1
        with open (f'{currentpath}/keys/privatekey{num}.pem', 'w+') as privatekeyfile: ## until i find a better way
            data = private_key_notencoded.export_key(format='PEM')
            privatekeyfile.write(data)
        with open (f'{currentpath}/keys/publickey{num}.pem', 'w+') as publickeyfile: ## until i find a better way
            data = public_key_notencoded.export_key(format='PEM')
            publickeyfile.write(data)
        openpubkey = open(f'{currentpath}/keys/publickey{num}.pem', 'r')
        self.public_key = openpubkey.read()
        hashed_public_sha256 = calculate_hash(self.public_key, "sha256")
        hashed_public_ripemd160 = calculate_hash(hashed_public_sha256, "ripemd160")
        wallet_address_encoded = base58.b58encode(hashed_public_ripemd160)
        self.wallet_address = wallet_address_encoded.decode("utf-8")
        with open (f'{currentpath}/keys/address{num}.pem', 'w+') as addressfile:
            data = self.wallet_address
            addressfile.write(data)
        

class transaction:
    def __init__(self, sender_private_key=None, sender_wallet_address=None, receiver_wallet_address=None, amount=None) -> None:
        self.sender_private_key = sender_private_key
        self.sender_wallet_address = sender_wallet_address
        self.receiver_wallet_address = receiver_wallet_address
        self.amount = amount
    def create_transaction(self):
        transaction_data = create_transaction_data(self.sender_wallet_address, self.receiver_wallet_address, self.amount)
        return convert_tx_to_byte(transaction_data)
    def signing(self, tx_byte):
        signing_key = DSS.new(ECC.import_key(self.sender_private_key), 'fips-186-3')
        hashed_tx=SHA256.new(tx_byte)
        signed_transaction = signing_key.sign(hashed_tx)
        return signed_transaction