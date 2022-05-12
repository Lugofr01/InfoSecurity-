#!/usr/bin/env python3
# encoding: UTF-8
"""
Custom VPN. Client
@authors: Frank Lugola
@version: 2022.4
"""

import hmac
from socket import socket, gethostname
from socket import AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR

from typing import Tuple, Dict
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


def parse_proposal(msg: str) -> Dict[str, list]:
    """Parse client's proposal
    
    :param msg: message from the client with a proposal (ciphers and key sizes)
    :return: the ciphers and keys as a dictionary
    """
    message_client = msg[16:]
    previous_cipher = ""
    cipher = ""
    key_size = ""
    key_list = []
    cipher_dictionary = {}

    for item in message_client:
        if item.isalpha():
            cipher = cipher +item
        elif item.isalnum():
            key_size += item
        elif item in ",":
            # {'AES': [128192256]} != {'AES': [128, 192, 256]}
            # comma to separate the vals
            if previous_cipher.isalnum():
                key_list.append(int(key_size))
                key_size = ""
        elif item == "]":
            key_list.append(int(key_size))
            key_size = ""
            cipher_dictionary[cipher] = key_list
            cipher = ""
            key_list = []
        previous_cipher = item

    return cipher_dictionary
            
            
    
    


def select_cipher(supported: dict, proposed: dict) -> Tuple[str, int]:
    """Select a cipher to use
    
    :param supported: dictionary of ciphers supported by the server
    :param proposed: dictionary of ciphers proposed by the client
    :return: tuple (cipher, key_size) of the common cipher where key_size is the longest supported by both
    :raise: ValueError if there is no (cipher, key_size) combination that both client and server support
    """
    # commoncipher = is the intersection between ciphers supported by server and cipher proposed
    # intersect = proposed and supported
    # https://www.programiz.com/python-programming/methods/set/intersection
    
    commoncipher = set(supported.keys()).intersection(proposed.keys())
    cipher = None
    key_size = -1
    

    if commoncipher is not  set():
        
        for item in commoncipher:
           
            current_keysize = max(set([-1]).union(set(supported.get(item)).intersection(proposed.get(item))))
            
            if current_keysize > key_size:
                key_size = current_keysize
                cipher = item

    if not cipher or key_size == -1:
        raise ValueError('Could not agree on a cipher')

    return (cipher, key_size)
        
    
    
    
    
    
    

    


def generate_cipher_response(cipher: str, key_size: int) -> str:
    """Generate a response message
    
    :param cipher: chosen cipher
    :param key_size: chosen key size
    :return: (cipher, key_size) selection as a string
    """
    # AssertionError: assert ('AES', 128) == 'ChosenCipher:AES,128'
    # AssertionError: assert 'ChosenCipher:AES' == 'ChosenCipher:AES,128'
    # https://www.w3schools.com/python/ref_string_format.asp
    
    return "ChosenCipher:{},{}".format(cipher, key_size)
    


def parse_dhm_request(msg: str) -> int:
    """Parse client's DHM key exchange request
    
    :param msg: client's DHMKE initial message
    :return: number in the client's message
    """
    number_in_client_message = int(msg.split(":")[1])
    
    return number_in_client_message

    


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
    DES key must be padded to 64 bits with 0
    Length `ivlen` of IV depends on a cipher
    `iv` is the *last* `ivlen` bytes of the shared key
    Both key and IV must be returned as bytes
    """
# Initialization vector
#     assert generate_cipher_response(cipher, key) == response
#        AssertionError: assert None == 'ChosenCipher:DES,56'
#        +  where None = generate_cipher_response('DES', 56)

    cipher_dictionary = {"DES": DES, "AES": AES, "Blowfish": Blowfish}

    ivlen = {"DES": DES.block_size, "AES": AES.block_size, "Blowfish": Blowfish.block_size}

    cipher = cipher_dictionary.get(cipher_name)
    
    
    key = shared_key[:key_size//8]
    if cipher_name == "DES":
        key = key+'\00'
    key = key.encode("utf-8")
    
    iv = shared_key[-1*ivlen.get(cipher_name):].encode("utf-8")

    return cipher, key, iv
    


def generate_dhm_response(public_key: int) -> str:
    """Generate DHM key exchange response
    
    :param public_key: public portion of the DHMKE
    :return: string according to the specification
    """
    
    dhm_response = "DHMKE:" + str(public_key)
    
    return dhm_response
def read_message(msg_cipher: bytes, crypto: object) -> Tuple[str, str]:
    """Read the incoming encrypted message
    
    :param msg_cipher: encrypted message from the socket
    :crypto: chosen cipher, must be initialized in the `main`
    :return: (plaintext, hmac) tuple
    """
    # crypto = AES.new(key, AES.MODE_CBC, iv)
    #  message, hmac_check = read_message(ciphertext, crypto)
    # To read upcoming message need to decode hmac and decrypt plaintext after decoding
    # AssertionError: assert 'infosec\x00\...0\x00\x00\x00' == 'infosec' remoe zeroes with strip 
    
#    source  # https://www.w3schools.com/python/ref_string_strip.asp

    hmac = msg_cipher[-64:].decode('utf-8')
    # codec can't decode byte 0xa6 in position 0: invalid start byte
    plaintext = (crypto.decrypt(msg_cipher[:-64]).decode('utf-8')).strip('\00')
    
    return (plaintext, hmac)



def validate_hmac(msg_cipher: bytes, hmac_in: str, hashing: object) -> bool:
    """Validate HMAC
    
    :param msg_cipher: encrypted message from the socket
    :param hmac_in: HMAC received from the client
    :param hashing: hashing object, must be initialized in the `main`
    :raise: ValueError is HMAC is invalid
    """
    # test file result
    # validate_hmac(b'\xfb\xd2\xd3\xc4j\xa4\t\x83\x8e\x0b\x15\xf3\x06\xd7<\x1f\x91Q%\xb3\xaf\x1e\xc0\xef2e\xaa}\xa3m:\xea\x0b\xfa=\x16\x1co\xf3\x0f\xedv\x8d\xd4:g \x1d1b072fe79eda09516021f7a5a99107524bb7846ea66efa9ae19b146144791416', '1b072fe79eda09516021f7a5a99107524bb7846ea66efa9ae19b146144791416', <Crypto.Hash.HMAC.HMAC object at 0x7ff5163e4e20>)
    # hashing = HMAC.new(key, digestmod=SHA256)
    #   assert validate_hmac(message, hmac_in, hashing)
    # cipher text at end of char
    
    
    hashing.update(msg_cipher[:-64])
    hash_result = hashing.hexdigest()
    
    if hash_result == hmac_in:
        return True
    else:
        raise ValueError("Bad HMAC")
    # AssertionError: assert 'is HMAC is invalid' == 'Bad HMAC'

def main():
    """Main loop

    See vpn.md for details
    """
    server_sckt = socket(AF_INET, SOCK_STREAM)
    server_sckt.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_sckt.bind((HOST, PORT))
    server_sckt.listen()
    print(f"Listening on {HOST}:{PORT}")
    conn, client = server_sckt.accept()
    print(f"New client: {client[0]}:{client[1]}")

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
        msg_in = conn.recv(4096).decode("utf-8")
        if len(msg_in) < 1:
            conn.close()
            break
        print(f"Received: {msg_in}")
        msg_out = f"Server says: {msg_in[::-1]}"
        conn.send(msg_out.encode())


if __name__ == "__main__":
    main()
