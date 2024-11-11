from Crypto.Cipher import AES
import random
import string

plaintext = b'Test String!'

key_string = ''.join(random.choices(string.ascii_uppercase, k=6))
key_string = key_string + key_string + key_string + key_string
key_bytes = bytes(key_string, 'utf-8')
key = key_bytes

dummy = "AAAAAA" + "AAAAAA" + "AAAAAA" + "AAAAAA"
dummy = bytes(dummy, 'utf-8')

cipher_enc = AES.new(key, AES.MODE_EAX)
nonce = cipher_enc.nonce
ciphertext, tag = cipher_enc.encrypt_and_digest(plaintext)

cipher_dec = AES.new(dummy, AES.MODE_EAX, nonce=nonce)

decrypted = cipher_dec.decrypt(ciphertext)

f=open("ciphertext","wb")
f.write(ciphertext)
f=open("nonce","wb")
f.write(nonce)
f=open("key","wb")
f.write(key)

def filter(plaintext):
    return all(32 <= ord(c) <= 255 for c in plaintext)

f=open("plaintext", "w")
print(decrypted.decode(errors='ignore'))
if filter(decrypted.decode(errors='ignore')):
    f.write(decrypted.decode(errors='ignore'))