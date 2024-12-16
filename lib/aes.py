import os, sys, json
import base64, hashlib
import lib.cipher as cipher
from hashlib import pbkdf2_hmac

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# key derivation function using PBKDF2
def generate_key(password, salt):
    return pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)

def encrypt(_input, password):
    """
    aes file encryption with eax mode
    
    :param _input: filepath to be encrypted
    :param password: password to generate secure key
    :return: True if successful, False otherwise
    """
    try:
        salt = get_random_bytes(16) 
        private_key = generate_key(password, salt)
        
        cipher = AES.new(private_key, AES.MODE_EAX)
        with open(_input, "rb") as file:
            ciphertext, tag = cipher.encrypt_and_digest(file.read())
        
        # write salt, nonce, tag, and ciphertext to the output file
        with open(f"{_input}.tf", "wb") as file:
            for n in (salt, cipher.nonce, tag, ciphertext):
                file.write(n)
        os.remove(_input)
        return True

    except Exception:return False



def decrypt(_input, password):
    """
    aes file decryption with EAX mode.

    :param _input: filepath to be decrypted
    :param password: password to generate secure key
    :return: True if decryption successful, False otherwise
    """
    try:
        with open(_input, "rb") as file:
            salt, nonce, tag, ciphertext = [file.read(x) for x in (16, 16, 16, -1)]

        private_key = generate_key(password, salt)  # Recreate key using the salt and password
        cipher = AES.new(private_key, AES.MODE_EAX, nonce)
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

        with open(_input.replace(".tf", ""), "wb") as file:
            file.write(decrypted_data)

        os.remove(_input)
        return True
    except Exception: return False

def crypter(mode, directory, password):
    """
    process files with crypter for encryption or decryption.

    :param mode: "encrypt" or "decrypt"
    :param directory: path to iterate and process files inside
    :param password: password to encrypt or decrypt files
    :return: count of processed files or error message
    """
    processed = 0
    # iterate and process files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            try:
                filepath = os.path.join(root, filename)
                if mode == "encrypt" and not filename.endswith(".tf"):
                    if encrypt(filepath, password):
                        processed += 1
                    else: return "corrupt file or incorrect password"

                elif mode == "decrypt" and filename.endswith(".tf"):
                    if decrypt(filepath, password):
                        processed += 1
                    else: return "corrupt file or incorrect password"

            except Exception: return "corrupt file or incorrect password"
    
    # obfuscate file names for increased privacy
    for root, dirs, files in os.walk(directory, topdown=True):
        for i in range(len(dirs)):
            try:
                if mode == "encrypt":
                    new_name = cipher.encrypt(dirs[i], password)
                    os.rename(os.path.join(root, dirs[i]), os.path.join(root, new_name))
                    dirs[i] = new_name
                elif mode == "decrypt":
                    new_name = cipher.decrypt(dirs[i], password)
                    os.rename(os.path.join(root, dirs[i]), os.path.join(root, new_name))
                    dirs[i] = new_name
            
            except Exception: continue


    return processed