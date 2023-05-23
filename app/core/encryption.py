from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import binascii
# Set up the encryption key and nonce

key = b'mysecretaeskey12' 
nonce = get_random_bytes(16)
# Define the encryption/decryption functions

# The first line converts the plaintext into a sequence of bytes using the UTF-8 encoding. 
# This is necessary because cryptographic algorithms operate on binary data.

# Next, we create an AES cipher. 
# We specify the cipher mode as GCM (Galois/Counter Mode), which provides both confidentiality and authentication.

# Moving on, we encrypt the plaintext using the AES cipher and generate a tag for authentication. 
# The ciphertext variable now holds the encrypted data, and the tag variable contains the authentication tag.

# To store and transmit the encrypted data, we concatenate the ciphertext, tag, and a unique nonce value associated with the cipher. 
# The nonce is a random value used to ensure the uniqueness of the encryption process.

# Finally, we convert the concatenated data into a hexadecimal string using the binascii.hexlify function and 
# decode it into a UTF-8 encoded string. This ensures that the encrypted data can be represented and stored as text.

# The function then returns the encrypted data as a string.


def encrypt(plaintext):
    # Convert the plaintext to bytes using UTF-8 encoding
    plaintext = plaintext.encode("utf-8")
    
    # Create a new AES cipher with the specified key, mode, and nonce
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Encrypt the plaintext and generate a tag for authentication
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    # Concatenate the ciphertext, tag, and nonce, and convert it to a hexadecimal string
    encrypted_data = binascii.hexlify(ciphertext + tag + cipher.nonce).decode("utf-8")
    
    # Return the encrypted data as a string
    return encrypted_data

def decrypt(ciphertext):
    ciphertext = ciphertext.encode("utf-8")
    ciphertext = binascii.unhexlify(ciphertext)
    nonce = ciphertext[-16:]
    tag = ciphertext[-32:-16]
    ciphertext = ciphertext[:-32]
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)
    return plaintext.decode('utf-8')