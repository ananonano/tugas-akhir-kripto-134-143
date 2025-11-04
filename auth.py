import hashlib

def hash_password_sha1(password):
    """Meng-hash password menggunakan SHA-1."""
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    return sha1.hexdigest()

def verify_password_sha1(plain_password, stored_hash):
    """Memverifikasi password plain dengan hash SHA-1 yang disimpan."""
    return hash_password_sha1(plain_password) == stored_hash