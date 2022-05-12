#!/usr/bin/env python3
"""
Custom VPN. Client
@authors: Frank Lugola
@version: 2022.4
"""
from base64 import encode
from posixpath import split
from statistics import mode
from typing import Tuple
from socket import socket, gethostname, AF_INET, SOCK_STREAM
from Crypto.Cipher import AES,DES,Blowfish
from rsa import encrypt
from cryptography.fernet import Fernet



HOST = gethostname()
PORT = 4600


def generate_cipher_proposal(supported: dict) -> str:
    
    
    """Generate a cipher proposal message
    :param supported: cryptosystems supported by the client
    :return: proposal as a string
    """
    ...

    # # # # for selected_cipher, values in supported.items():
        
    # # x= str(supported.items())
    
    # # for run in x:
        
    
        
       
    #     #  ProposedCiphers:AES:[128,192,256],Blowfish:[112,224,448],DES:[56]
    for selected_cipher, values in supported.items():
        

         
        Proposal = "ProposedCiphers:" + ','.join([selected_cipher + ':[' + ','.join([str(x) for x in values]) + ']'for selected_cipher, values in supported.items()])
    return Proposal
    
    # # for x in supported:
    # #     # if x == "AES" and x =="Blowfish" and x =="DES":
            
        
    # #     return "ProposedCiphers:" + ([str(x) for ]) +":" + str(supported[x])
    


def parse_cipher_selection(msg: str) -> tuple[str, int]:
    """Parse server's response
    :param msg: server's message with the selected cryptosystem
    :return: (cipher_name, key_size) tuple extracted from the message
    """
    ...
    
    list = msg.split(':')[1].split(',')
    cipher_name,key_size = list[0], int(list[1])
    return cipher_name, key_size

# split the msg which is divided with ":" and "'" first part corresponds to cipher name and second part corresponds the key size


def generate_dhm_request(public_key: int) -> str:
    """Generate DHM key exchange request
    :param: client's DHM public key
    :return: string according to the specification
    """
    ...
    
    dhm_request = "DHMKE:" + str(public_key)
    return dhm_request


def parse_dhm_response(msg: str) -> int:
    """Parse server's DHM key exchange request
    :param msg: server's DHMKE message
    :return: number in the server's message
    """
    ...
    number_in_server_message = int(msg.split(":")[1])
    
    return number_in_server_message


def get_key_and_iv(
    shared_key: str, cipher_name: str, key_size: int
) -> Tuple[object, bytes, bytes]:
    """Get key and IV from the generated shared secret key
    :param shared_key: shared key as computed by `diffiehellman`
    :param cipher_name: negotiated cipher's name
    :param key_size: negotiated key size
    :return: (cipher, key, IV) tuple
    cipher_name must be mapped to a Crypto.Cipher object
    `key` is the *first* `key_size` bytes of the `shared_key`
    DES key must be padded to 64 values with 0
    Length `ivlen` of IV depends on a cipher
    `iv` is the *last* `ivlen` bytes of the shared key
    Both key and IV must be returned as bytes
    """
    ...
    
    ciphers = {"DES": DES, "AES": AES, "Blowfish": Blowfish}

    ivlen = {"DES": DES.block_size, "AES": AES.block_size, "Blowfish": Blowfish.block_size}

    cipher = ciphers.get(cipher_name)
    
    
    # for key
    key = shared_key[:key_size//8]
    if cipher_name == "DES":
        key = key+'\00'
    key = key.encode("utf-8")
    
    
    
    # # Initialization vector
    
    iv = shared_key[-1 * ivlen.get(cipher_name):].encode("utf-8")

    return cipher, key, iv

def add_padding(message: str) -> str:
    """Add padding (0x0) to the message to make its length a multiple of 16
    :param message: message to pad
    :return: padded message
    """
    ...
    padding = len(message)
    while padding % 16 != 0:
    
        padding = padding + 1
    padding = padding - len(message)
    padded_message = message + '\00' * padding
    
    return padded_message
    
    


def encrypt_message(message: str, crypto: object, hashing: object) -> tuple[bytes, str]:
    """
    Encrypt the message
    :param message: plaintext to encrypt
    :param crypto: chosen cipher, must be initialized in the `main`
    :param hashing: hashing object, must be initialized in the `main`
    :return: (ciphertext, hmac) tuple
    1. Pad the message, if necessary
    2. Encrypt using cipher `crypto`
    3. Compute HMAC using `hashing`
    """
    ...
    # crypto = AES.new(key, AES.MODE_CBC, iv)
    # mode = AES.MODE_CBC
    # hashing = HMAC.new(key, digestmod=SHA256)
    # ciph_out, hmac_out = encrypt_message(plaintext, crypto, hashing)
#    https://github.com/Legrandin/pycryptodome/issues/259


    message = add_padding(message)
    message = message.encode("utf-8")
    # ciphertext = crypto.encrypt(message)
    ciphertext = crypto.encrypt(message)
    hashing.update(ciphertext)
    # to return hexadecimal digits
    hmacvalue = hashing.hexdigest()
    return ciphertext, hmacvalue

    # print(ciphertext, hmacvalue)


def main():
    """Main event loop
    See vpn.md for details
    """
    client_sckt = socket(AF_INET, SOCK_STREAM)
    client_sckt.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    print("Negotiating the cipher")
    cipher_name = "CS"
    key_size = 460
    # Follow the description
    print(f"We are going to use {cipher_name}{key_size}")

    print("Negotiating the key")
    # Follow the description
    print("The key has been established")

    print("Initializing cryptosystem")
    # Follow the description
    print("All systems ready")

    while True:
        msg_out = input("Enter message: ")
        if msg_out == "\\quit":
            client_sckt.close()
            break
        client_sckt.send(msg_out.encode())
        msg_in = client_sckt.recv(4096)
        print(msg_in.decode("utf-8"))


if __name__ == "__main__":
    main()