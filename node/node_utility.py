from Crypto.Hash import SHA256

def Cryptographic_SHA256_Hash(data):
    if type(data) == str:
        data = bytes(data, "utf-8")
    hash = SHA256.new(data=data)
    return hash.hexdigest()