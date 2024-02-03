from Crypto.Hash import SHA256, RIPEMD160
import json
import os

def calculate_hash(data, hash_function: str = "sha256"):
    if type(data) == str:
        data = bytes(data, "utf-8")
    if hash_function == "sha256":
        hash = SHA256.new()
        hash.update(data)
        return hash.hexdigest()
    if hash_function == "ripemd160":
        hash = RIPEMD160.new()
        hash.update(data)
        return hash.hexdigest()
def create_transaction_data(sender_address, receiver_address, amount):
    return {
        "sender_address": sender_address,
        "receiver_address": receiver_address,
        "amount": amount
    }
def convert_tx_to_byte(transaction_data):
    return json.dumps(transaction_data, indent=2).encode('utf-8')
    