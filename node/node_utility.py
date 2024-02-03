from Crypto.Hash import SHA256, RIPEMD160

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
