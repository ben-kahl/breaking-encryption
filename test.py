from Crypto.Cipher import AES
import string

with open("given_nonce", "rb") as file:
    nonce = file.read()

with open("given_ciphertext", 'rb') as file:
    ciphertext = file.read()

plaintext = b'Luke Skywalker has returned to his home planet of Tatooine in an attempt to rescue his friend Han Solo from the clutches of the vile gangster Jabba the Hutt. Little does Luke know that the GALACTIC EMPIRE has secretly begun construction on a new armored space station even more powerful than the first dreaded Death Star. When completed, this ultimate weapon will spell certain doom for the small band of rebels struggling to restore freedom to the galaxy...'

key = "LBSSAQLBSSAQLBSSAQLBSSAQ"
key_bytes = bytes(key, 'utf-8')

cipher_enc = AES.new(key_bytes, AES.MODE_EAX, nonce=nonce)

ciphertext, tag = cipher_enc.encrypt_and_digest(plaintext)

f=open("ciphertext", "wb")
f.write(ciphertext)

cipher_dec = AES.new(key_bytes, AES.MODE_EAX, nonce=nonce)

decrypted = cipher_dec.decrypt(ciphertext)

print(decrypted.decode())

# def try_key(key_chars):
#     # key = ''.join(key_chars)
#     key = "AAAAAA"
#     key_string = key + key + key + key
#     key = bytes(key_string, 'utf-8')
    
#     try:
#         cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        
#         plaintext = cipher.decrypt(ciphertext)
        
#         return key_string, plaintext.decode(errors='ignore',encoding='utf-8')
        
#     except Exception as e:
#         print(e)
#         pass
#     return None

# def filter(plaintext):
#     return all(32 <= ord(c) <= 255 for c in plaintext)