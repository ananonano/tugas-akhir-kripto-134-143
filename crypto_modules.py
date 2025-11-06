import string
from Crypto.Cipher import DES, Blowfish, CAST, ARC4
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from PIL import Image
import math

# 1. DES (Untuk Database History)
def des_encrypt(data, key):
    cipher = DES.new(key, DES.MODE_ECB)
    padded_data = pad(data, DES.block_size)
    return cipher.encrypt(padded_data)

def des_decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_data = cipher.decrypt(ciphertext)
    return unpad(decrypted_data, DES.block_size)

# 2. Super Enkripsi (Vigenere + Blowfish)
# 2a. Vigenere Cipher
def vigenere_encrypt(plain_text, key):
    encrypted_text = ""
    key_index = 0
    key = key.upper()
    
    for char in plain_text:
        if 'a' <= char <= 'z':
            shift = ord(key[key_index % len(key)]) - ord('A')
            encrypted_char = chr(((ord(char) - ord('a') + shift) % 26) + ord('a'))
            key_index += 1
        elif 'A' <= char <= 'Z':
            shift = ord(key[key_index % len(key)]) - ord('A')
            encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
            key_index += 1
        else:
            encrypted_char = char
        encrypted_text += encrypted_char
    return encrypted_text

def vigenere_decrypt(cipher_text, key):
    decrypted_text = ""
    key_index = 0
    key = key.upper()
    
    for char in cipher_text:
        if 'a' <= char <= 'z':
            shift = ord(key[key_index % len(key)]) - ord('A')
            decrypted_char = chr(((ord(char) - ord('a') - shift + 26) % 26) + ord('a'))
            key_index += 1
        elif 'A' <= char <= 'Z':
            shift = ord(key[key_index % len(key)]) - ord('A')
            decrypted_char = chr(((ord(char) - ord('A') - shift + 26) % 26) + ord('A'))
            key_index += 1
        else:
            decrypted_char = char
        decrypted_text += decrypted_char
    return decrypted_text

# 2b. Blowfish
def blowfish_encrypt(data, key):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    padded_data = pad(data, Blowfish.block_size)
    return cipher.encrypt(padded_data)

def blowfish_decrypt(ciphertext, key):
    cipher = Blowfish.new(key, Blowfish.MODE_ECB)
    decrypted_data = cipher.decrypt(ciphertext)
    return unpad(decrypted_data, Blowfish.block_size)

# 2c. Super Enkripsi
def super_encrypt(plain_text, vigenere_key, blowfish_key):
    # Tahap 1: Vigenere
    vigenere_encrypted = vigenere_encrypt(plain_text, vigenere_key)
    # Tahap 2: Blowfish
    super_encrypted = blowfish_encrypt(vigenere_encrypted.encode('utf-8'), blowfish_key)
    return super_encrypted

def super_decrypt(super_ciphertext, vigenere_key, blowfish_key):
    # Tahap 1: Blowfish Dekripsi
    try:
        blowfish_decrypted = blowfish_decrypt(super_ciphertext, blowfish_key)
        # Tahap 2: Vigenere Dekripsi
        vigenere_decrypted = vigenere_decrypt(blowfish_decrypted.decode('utf-8'), vigenere_key)
        return vigenere_decrypted
    except Exception as e:
        return f"Error dekripsi: {e}. Pastikan kunci benar dan data tidak rusak."

# 3. Enkripsi File (CAST-128)
def cast_encrypt_file(file_bytes, key):
    cipher = CAST.new(key, CAST.MODE_ECB) 
    padded_data = pad(file_bytes, CAST.block_size)
    return cipher.encrypt(padded_data)

def cast_decrypt_file(file_bytes, key):
    cipher = CAST.new(key, CAST.MODE_ECB)
    try:
        decrypted_data = cipher.decrypt(file_bytes)
        return unpad(decrypted_data, CAST.block_size)
    except ValueError:
        return None

# Helper untuk mengubah data (string, bytes) ke binary string
def data_to_binary(data):
    """Konversi string atau bytes ke binary string."""
    if isinstance(data, str):
        return ''.join(format(ord(i), '08b') for i in data)
    elif isinstance(data, bytes) or isinstance(data, bytearray):
        return ''.join(format(i, '08b') for i in data)
    raise TypeError("Tipe data tidak didukung.")

# Helper untuk mengubah binary string kembali ke bytes
def binary_to_bytes(binary_data):
    """Konversi binary string kembali ke bytes."""
    all_bytes = []
    for i in range(0, len(binary_data), 8):
        byte_str = binary_data[i:i+8]
        if len(byte_str) == 8:
            try:
                all_bytes.append(int(byte_str, 2))
            except ValueError:
                pass # Abaikan byte tidak lengkap
    return bytearray(all_bytes)

def lsb_rc4_hide(image, secret_message, key):
    """Menyisipkan pesan rahasia ke gambar menggunakan LSB, dienkripsi dengan RC4."""
    img = image.copy()
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # 1. Enkripsi pesan dengan RC4
    try:
        key_bytes = key.encode('utf-8')
        cipher = ARC4.new(key_bytes)
        message_bytes = secret_message.encode('utf-8')
        encrypted_data = cipher.encrypt(message_bytes)
    except Exception as e:
        raise ValueError(f"Error RC4 Encryption: {e}")

    # 2. Tambahkan delimiter unik (8 null bytes)
    # Ini untuk menandai akhir dari pesan rahasia
    data_to_hide = encrypted_data + b'\x00\x00\x00\x00\x00\x00\x00\x00'
    
    # 3. Ubah data terenkripsi ke binary string
    binary_data = data_to_binary(data_to_hide)
    
    data_index = 0
    img_data = list(img.getdata())
    new_pixels = []
    
    if len(binary_data) > len(img_data) * 3:
        raise ValueError("Pesan terlalu besar untuk gambar ini.")

    for pixel in img_data:
        if data_index >= len(binary_data):
            new_pixels.append(pixel)
            continue
        
        # (R, G, B)
        new_pix = []
        for i in range(3): # Loop R, G, B
            if data_index < len(binary_data):
                # Ambil nilai pixel (misal 254 -> 11111110)
                # Ubah LSB (bit terakhir)
                # (pixel[i] & ~1) -> Meng-nol-kan bit terakhir
                # | int(binary_data[data_index]) -> Men-set bit terakhir ke bit data
                new_val = (pixel[i] & ~1) | int(binary_data[data_index])
                new_pix.append(new_val)
                data_index += 1
            else:
                new_pix.append(pixel[i])
                
        new_pixels.append(tuple(new_pix))

    if data_index < len(binary_data):
         raise ValueError("Tidak cukup ruang untuk menyembunyikan seluruh pesan (error iterasi).")
         
    img_stego = Image.new('RGB', img.size)
    img_stego.putdata(new_pixels)
    return img_stego

def lsb_rc4_reveal(image, key):
    """Mengekstrak pesan rahasia dari gambar LSB, didekripsi dengan RC4."""
    img = image.copy()
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    img_data = list(img.getdata())
    binary_data = ""
    
    # Delimiter (8 null bytes) dalam binary
    delimiter_binary = '00000000' * 8 

    for pixel in img_data:
        for i in range(3): # R, G, B
            # Ekstrak LSB (bit terakhir) dan tambahkan ke string binary
            binary_data += str(pixel[i] & 1)
            
            # Cek apakah delimiter sudah ditemukan
            if binary_data.endswith(delimiter_binary):
                # Hapus delimiter dari data
                binary_data = binary_data[:-len(delimiter_binary)]
                
                # Ubah binary ke bytes
                encrypted_bytes = binary_to_bytes(binary_data)
                
                # 4. Dekripsi dengan RC4
                try:
                    key_bytes = key.encode('utf-8')
                    cipher = ARC4.new(key_bytes)
                    decrypted_data = cipher.decrypt(encrypted_bytes)
                    return decrypted_data.decode('utf-8')
                except Exception as e:
                    # Gagal dekripsi (kunci salah)
                    return None

    # Jika loop selesai tanpa menemukan delimiter
    return None