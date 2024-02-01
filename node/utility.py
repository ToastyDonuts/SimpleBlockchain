from Crypto.Hash import SHA256

def Cryptographic_SHA256_Hash(data: bytes):
    hash = SHA256.new(data=data)
    return hash.hexdigest()