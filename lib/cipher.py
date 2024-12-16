import re, sys
from random import randint

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def vigenere_cipher(key, message, mode):
    """
    vigenère cipher function that encrypts or decrypts a message
    using a specified key and mode ('encrypt' or 'decrypt').
    
    :param key: The key used for encryption or decryption
    :param message: The message to be processed
    :param mode: 'encrypt' for encryption, 'decrypt' for decryption
    :return: The processed message
    """
    result = []
    key_index = 0
    key = key.upper()

    for char in message:
        char_index = alphabet.find(char.upper())
        if char_index != -1:
            if mode == "encrypt": char_index += alphabet.find(key[key_index])
            elif mode == "decrypt": char_index -= alphabet.find(key[key_index])
            char_index %= len(alphabet)

            if char.isupper(): result.append(alphabet[char_index])
            elif char.islower(): result.append(alphabet[char_index].lower())
            key_index += 1

            if key_index == len(key): key_index = 0
        else: result.append(char)

    return "".join(result)

def caesar_cipher(string, shift):
    """
    simple Caesar cipher function that shifts characters in a string
    by a specified amount (shift) for encryption.
    
    :param string: The string to be encrypted
    :param shift: The number of positions to shift each character
    :return: The encrypted string
    """
    ciphered_string = ""
    for char in string:
        if char == " ":
            ciphered_string += char
        elif char.isupper():
            ciphered_string += chr((ord(char) + shift - 65) % 26 + 65)
        else:
            ciphered_string += chr((ord(char) + shift - 97) % 26 + 97)

    return ciphered_string

# character set for encryption/decryption
char_set = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
    'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/', '=', '.',
    '_', ' ', '!', '"', "'", '#', '$', '(', ')', '*', '?', ':', ';',
    '[', ']', ',', '-', '\n', '@', '&'
]

def encrypt(text, key):
    """
    encrypts the given text using the provided key.
    
    :param text: plaintext to encrypt
    :param key: key for encryption (must be at least 8 characters mixed)
    :return: encrypted text or False if the key is invalid
    """
    if len(key) >= 8 and re.search("[a-zA-Z]", key) and re.search(r"\d", key):
        total_chars = len(alphabet) * len(key)
        encryption_range = [x for x in range(total_chars, total_chars + 87)]
        mapped_chars = [encryption_range[char_set.index(char)] for char in text]
        combined = "".join(str(e) for e in mapped_chars)
        split_values = []

        for value in combined:
            a = randint(0, int(value))
            b = int(value) - a
            split_values.append(str(a) + str(b))

        joined_split = "".join(split_values)
        final_output = [caesar_cipher(alphabet, len(key))[['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].index(x)] for x in joined_split]
        return vigenere_cipher(key, final_output, "encrypt")
    return False

def decrypt(ciphertext, key):
    """
    decrypts the given ciphertext using the provided key.
    
    :param ciphertext: The encrypted text to decrypt
    :param key: The key for decryption (must be at least 4 characters)
    :return: The decrypted text or 666 if the key is invalid
    """
    if len(key) >= 8 and re.search("[a-zA-Z]", key) and re.search(r"\d", key):
        decrypted_message = vigenere_cipher(key, ciphertext, "decrypt")
        combined_decrypted = "".join(str(i) for i in decrypted_message)
        initial_chars = [i for i in caesar_cipher(alphabet, len(key))[:10]]
        index_mapping = [['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'][initial_chars.index(x)] for x in combined_decrypted]
        numeric_values = list(map(int, index_mapping))
        summed_values = [sum(numeric_values[i:i + 2]) for i in range(0, len(numeric_values), 2)]
        total_chars = len(alphabet) * len(key)
        encryption_indices = [x for x in range(total_chars, total_chars + 87)]
        concatenated_values = "".join(str(i) for i in summed_values)
        split_concatenated = list(map(int, [concatenated_values[i:i + 3] for i in range(0, len(concatenated_values), 3)]))
        final_chars = [char_set[encryption_indices.index(u)] for u in split_concatenated]
        return "".join(str(i) for i in final_chars)
    return False