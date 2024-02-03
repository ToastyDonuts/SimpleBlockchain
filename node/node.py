from Crypto.Signature import DSS
from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Blockchain import Block
import copy
import json
import binascii
from node_utility import calculate_hash

class NodeTransaction:
    def __init__(self, block: Block) -> None:
        self.block = block
        self.transaction_data = {}
        self.signature = ""
        self.inputs = ""
        self.outputs = ""
    def validate_signature(self):
        tx_data = copy.deepcopy(self.transaction_data)
        for count, tx_input in enumerate(tx_data["inputs"]):
            tx_input_dict = json.loads(tx_input)
            public_key = tx_input_dict.pop("pubkey")
            signature = tx_input_dict.pop("signature")
            tx_data["inputs"][count] = json.dumps(tx_input_dict)
            signature_decoded = binascii.unhexlify(signature.encode("utf-8"))
            public_key_byte = binascii.unhexlify(public_key).encode("utf-8")
            public_key_imported = ECC.import_key(public_key_byte)
            tx_data["inputs"][count] = json.dumps(tx_input_dict)
            tx_bytes = json.dumps(tx_data, indent=2).encode('utf-8')
            tx_hash = SHA256.new(tx_bytes)
            (DSS.new(public_key_imported, 'fips-186-3')).verify(tx_hash)
    def get_tx_utxo(self, utxo_hash):
        current_block = self.block
        while current_block:
            if current_block.transaction_hash == utxo_hash:
                return current_block.transaction_data
            current_block = current_block.previous_block
    def validate_have_fund(self):
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            public_key = input_dict["public_key"]
            sender_public_hash = calculate_hash(calculate_hash(public_key), hash_function='ripemd160')
            transaction_data = self.get_tx_utxo(input_dict["transaction_hash"])
            output_public_hash = json.loads(transaction_data["outputs"][input_dict["output_index"]])["public_key_hash"]
            assert output_public_hash == sender_public_hash
    def input_amount(self):
        total_input = 0
        for tx_input in self.inputs:
            input_dict = json.loads(tx_input)
            transaction_data = self.get_tx_utxo(input_dict["transaction_hash"])
            utxo_amount = json.loads(transaction_data["outputs"][input_dict["output_index"]])["amount"]
            total_input = total_input + utxo_amount
        return total_input

    def output_amount(self):
        total_output = 0
        for tx_output in self.outputs:
            output_dict = json.loads(tx_output)
            amount = output_dict["amount"]
            total_out = total_output + amount
        return total_output
    def validate_fund(self):
        assert self.input_amount == self.output_amount

    def validate(self):
        self.validate_signature()
        self.validate_have_fund()
        self.validate_fund