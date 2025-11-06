import string
from Crypto.Cipher import DES, Blowfish, CAST
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

# 4. Steganografi (PVD)
QUANTIZATION_TABLE = [
    (0, 7, 3),
    (8, 15, 3),
    (16, 31, 4),
    (32, 63, 5),
    (64, 127, 6),
    (128, 255, 7)
]

def find_range(diff):
    """Mencari range yang sesuai untuk nilai perbedaan."""
    diff = abs(diff)
    for (lower, upper, bits) in QUANTIZATION_TABLE:
        if lower <= diff <= upper:
            return (lower, upper, bits)
    return None # Seharusnya tidak terjadi jika tabel lengkap

def data_to_binary(data):
    """Konversi string ke binary."""
    if isinstance(data, str):
        return ''.join(format(ord(i), '08b') for i in data)
    elif isinstance(data, bytes) or isinstance(data, bytearray):
        return ''.join(format(i, '08b') for i in data)
    raise TypeError("Tipe data tidak didukung.")

def binary_to_string(binary_data):
    """Konversi binary kembali ke string."""
    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    decoded_message = ""
    for byte in all_bytes:
        if len(byte) == 8:
            try:
                decoded_message += chr(int(byte, 2))
            except ValueError:
                pass # Mengabaikan byte yang tidak lengkap/valid di akhir
    return decoded_message

def pvd_hide_message(image, secret_message):
    """Menyembunyikan pesan menggunakan PVD."""
    img = image.copy()
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    pixels = list(img.getdata())
    width, height = img.size
    
    # 1. Siapkan data binary
    binary_message = data_to_binary(secret_message)
    binary_message_len = len(binary_message)
    
    # Sembunyikan panjang pesan (32 bits) di awal
    binary_len_header = format(binary_message_len, '032b')
    binary_data_to_hide = binary_len_header + binary_message
    
    data_index = 0
    new_pixels = []
    
    # Iterasi per piksel (bukan per blok 2x1)
    # Kita akan proses channel R, G, B secara terpisah
    # (P, Q) adalah pasangan piksel
    
    flat_pixels = [p for pixel in pixels for p in pixel] # [R1, G1, B1, R2, G2, B2, ...]

    if len(binary_data_to_hide) > (len(flat_pixels) // 2) * 7: # Asumsi max bits
        raise ValueError("Pesan terlalu besar untuk gambar ini.")

    i = 0
    while i < len(flat_pixels) - 1 and data_index < len(binary_data_to_hide):
        p1 = flat_pixels[i]
        p2 = flat_pixels[i+1]
        
        diff = p1 - p2
        lower, upper, n_bits = find_range(diff)
        
        if data_index + n_bits <= len(binary_data_to_hide):
            bits_to_embed_str = binary_data_to_hide[data_index : data_index + n_bits]
            bits_to_embed_int = int(bits_to_embed_str, 2)
            
            # Hitung perbedaan baru
            new_diff = lower + bits_to_embed_int if diff >= 0 else -(lower + bits_to_embed_int)
            
            # Hitung nilai piksel baru
            m = new_diff - diff
            p1_new = p1 + math.ceil(m / 2)
            p2_new = p2 - math.floor(m / 2)
            
            # Penanganan Overflow/Underflow
            if p1_new > 255: 
                p1_new, p2_new = 255, 255 - new_diff
            elif p1_new < 0:
                p1_new, p2_new = 0, 0 - new_diff
            
            if p2_new > 255:
                p2_new, p1_new = 255, 255 + new_diff
            elif p2_new < 0:
                p2_new, p1_new = 0, 0 + new_diff

            # Pastikan clipping terakhir
            p1_new = max(0, min(255, p1_new))
            p2_new = max(0, min(255, p2_new))

            flat_pixels[i] = p1_new
            flat_pixels[i+1] = p2_new
            
            data_index += n_bits
        
        # Pindah ke pasangan berikutnya (lewati 2 piksel)
        i += 2

    if data_index < len(binary_data_to_hide):
         raise ValueError("Tidak cukup ruang untuk menyembunyikan seluruh pesan (error iterasi).")

    # Rekonstruksi tuple piksel
    final_pixel_tuples = []
    for j in range(0, len(flat_pixels), 3):
        if j+2 < len(flat_pixels):
            final_pixel_tuples.append(tuple(flat_pixels[j:j+3]))

    img_stego = Image.new('RGB', (width, height))
    img_stego.putdata(final_pixel_tuples)
    return img_stego


def pvd_reveal_message(image):
    """Mengungkap pesan dari gambar PVD."""
    img = image.copy()
    if img.mode != 'RGB':
        img = img.convert('RGB')
        
    pixels = list(img.getdata())
    flat_pixels = [p for pixel in pixels for p in pixel] # [R1, G1, B1, R2, G2, B2, ...]

    binary_extracted_data = ""
    
    # 1. Ekstrak Header Panjang Pesan (32 bits pertama)
    i = 0
    binary_len_header = ""
    while i < len(flat_pixels) - 1 and len(binary_len_header) < 32:
        p1 = flat_pixels[i]
        p2 = flat_pixels[i+1]
        
        diff = p1 - p2
        lower, upper, n_bits = find_range(diff)
        
        # Ambil n_bits dari |diff|
        bits_to_extract_int = abs(diff) - lower
        bits_to_extract_str = format(bits_to_extract_int, f'0{n_bits}b')
        
        binary_len_header += bits_to_extract_str
        i += 2

    if len(binary_len_header) < 32:
        return None # Gambar terlalu kecil atau bukan stego PVD

    binary_len_header = binary_len_header[:32]
    try:
        message_length = int(binary_len_header, 2)
    except ValueError:
        return None # Header korup

    # 2. Ekstrak Sisa Pesan
    # 'i' sekarang menunjuk ke piksel setelah header
    binary_message_data = ""
    while i < len(flat_pixels) - 1 and len(binary_message_data) < message_length:
        p1 = flat_pixels[i]
        p2 = flat_pixels[i+1]
        
        diff = p1 - p2
        lower, upper, n_bits = find_range(diff)
        
        bits_to_extract_int = abs(diff) - lower
        bits_to_extract_str = format(bits_to_extract_int, f'0{n_bits}b')
        
        binary_message_data += bits_to_extract_str
        i += 2
        
    if len(binary_message_data) < message_length:
        return None # Pesan tidak lengkap
        
    binary_message_data = binary_message_data[:message_length]
    
    return binary_to_string(binary_message_data)