import itertools
from Crypto.Cipher import AES
from multiprocessing import Pool, cpu_count
import string
from tqdm import tqdm

# Notes
# Key is made up of 6 uppercase characters that repeat 6 times, so there are 26^6 (308915776) possibilities
# Key is random and seeded
# AES does garble everything
# I don't want to waste time generating strings, I might want to create a rainbow table

# key_string = "6 chars uppercase"
# key_string = key_string + key_string + key_string + key_string
# key_bytes = bytes(key_string, 'utf-8')
# key = key_bytes

results = []

with open("given_nonce", "rb") as file:
    nonce = file.read()

with open("given_ciphertext", 'rb') as file:
    ciphertext = file.read()

# Filters out garbage values
def filter(plaintext):
    return all(32 <= ord(c) <= 255 for c in plaintext)

# Test decryption with each key
def try_key(key_chars):
    # Initialize key
    key = ''.join(key_chars)
    key_string = key + key + key + key
    key = bytes(key_string, 'utf-8')
    
    try:
        # Create cipher and decrypt
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        # Only return values that fit the filter
        if filter(plaintext.decode(errors='ignore')):
            return key_string, plaintext.decode(errors='ignore')
    except Exception as e:
        pass
    # Otherwise, return None
    return None

def main():
    # Create table with tuples of all possible combinations for 6 character strings with A-Z
    table = itertools.product(string.ascii_uppercase, repeat=6)
    # Initialize multiprocessing
    pool = Pool(cpu_count())
    
    # Progress bar, not important to program function
    with tqdm(total=26**6, desc="Progress", unit=" keys") as pbar:
        # Iterate across the key table using multiprocessing
        for i, result in enumerate(pool.imap_unordered(try_key, table, chunksize=5000)):
            # Results will only contain plaintext that exclusively contain ascii chars 32 - 255
            if result is not None:
                results.append(result)
            # Write outputs every 100000 iterations
            if i % 100000 == 0:
                with open("decrypted.txt", 'a') as file:
                    for key, plaintext in results:
                        file.write(f"Key: {key}, Plaintext: {plaintext}\n")
                results.clear()
        
            pbar.update(1)
    # Stop multiprocessing
    pool.close()
    pool.join()
    pbar.close()
    # Just incase any results were missed at the end
    with open("decrypted.txt", 'a') as file:
        for key, plaintext in results:
            file.write(f"Key: {key}, Plaintext: {plaintext}\n")

if __name__ == '__main__':
    main()