import sys
import os
sys.path.append(f'{os.path.abspath(os.path.join(os.getcwd(), os.pardir))}\\transaction')
from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from wallet_utility import calculate_hash 
from wallet_utility import create_transaction_data, convert_tx_to_byte
from Crypto.Hash import SHA256
import json
import base58
from tx_input import TransactionInput
from tx_output import TransactionOutput
import binascii
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
    def __init__(self, PrivateKeyFileLocation, PublicKeyFileLocation, Input: [TransactionInput], Output: [TransactionOutput]) -> None:
        self.PrivateKey = ECC.import_key((open(PrivateKeyFileLocation).read()))
        self.PublicKey = ECC.import_key((open(PublicKeyFileLocation).read()))
        self.Input = Input
        self.Output = Output
    def signing_tx(self):
        tx_dict = {
            "inputs": [tx_input.to_json(with_pub_and_signature=False) for tx_input in self.Input],
            "outputs": [tx_output.to_json() for tx_output in self.Output]
        }
        tx_bytes = json.dumps(tx_dict, indent=2).encode('utf-8')
        hashed_bytes = SHA256.new(tx_bytes)
        return (DSS.new(self.PrivateKey, 'fips-186-3')).sign(hashed_bytes)
    def sign(self):
        signature_hex = binascii.hexlify(self.signing_tx()).decode('utf-8')
        pubkey_hex = binascii.hexlify(self.PublicKey).decode('utf-8')
        for tx_inputs in self.Input:
            tx_inputs.signature = signature_hex
            tx_inputs.pubkey = pubkey_hex
    def broadcast(self): 
        return {
            "inputs": [i.to_json() for i in self.Input],
            "outputs": [i.to_json() for i in self.Output]
        }

