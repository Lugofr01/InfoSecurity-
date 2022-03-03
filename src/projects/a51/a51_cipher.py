#!/usr/bin/env python3
"""
A5/1 cipher implementation

@authors: Roman Yasinovskyy
@version: 2022.2
"""

from hashlib import sha256
from operator import xor
from pathlib import Path
from pydoc import plain
import re
from unittest import result

from numpy import character, source


def populate_registers(init_keyword: str) -> tuple[str, str, str]:
    """Populate registers

    Important: if the keyword is shorted than 8 characters (64 bits),
    pad the resulting short bit string with zeros (0) up to the required 64 bits

    :param init_keyword: initial secret word that will be used to populate registers X, Y, and Z
    :return: registers X, Y, Z as a tuple
    """
    # TODO: Implement this function
    
    ...
    
    XYZ = ""
    
    for character in init_keyword:
        XYZ = XYZ + bin(ord(character))[2:].zfill(8)
        # bin is to Return the binary representation of an integer.
        # ord is to Return the Unicode code point for a one-character string
        #.zfill is to pad zeros on the left on the given width which at this case is 8 characters or 64 bits
        
# Important: if the keyword is shorted than 8 characters (64 bits),pad the resulting short bit string with zeros (0) up to the required 64 bits

    if len(XYZ) < 64:
        XYZ = XYZ.ljust(64,"0")
        
    X = XYZ[0:19]
    Y = XYZ[19:41]
    Z =XYZ[41:64]
    
    return (X,Y,Z)


def majority(x8_bit: str, y10_bit: str, z10_bit: str) -> str:
    """Return the majority bit

    :param x8_bit: 9th bit from the X register
    :param y10_bit: 11th bit from the Y register
    :param z10_bit: 11th bit from the Z register
    :return: the value of the majority bit
    """
    # TODO: Implement this function
    ...
    
    if x8_bit =="0":
        if y10_bit =="0":
            return "0"
        else:
            if z10_bit =="0":
                return "0"
            else:
                return "1"
    else:
        if y10_bit =="0":
            if z10_bit =="1":
                return "1"
            
            else:
                return "0"
            
        else:
            return "1"
            
        
        
# The approach here involves finding the majority in x,y,z. The if statements check whether the majority is between values 1 and 0
# The majority will always be what is present in two or more registers. ie if x,y,z =(0,0,1) the majority is 0 and vice versa


def step_x(register: str) -> str:
    """Stepping register X

    :param register: X register
    :return: new value of the X register
    """
    # TODO: Implement this function
    ...
    #from page 53, "information security and principles mark stamp" t = x13 xor x16 xor x17 xor x18
    
    x13 = register[13]
    x16 = register[16]
    x17 = register[17]
    x18 = register[18]
    
    t = int(x13)^int(x16)^int(x17)^int(x18)
    
    register = str(t) + register[:-1]
    
    return register
    


def step_y(register: str) -> str:
    """Stepping register Y

    :param register: Y register
    :return: new value of the Y register
    """
    # TODO: Implement this function
    
    ...
    #from page 53, "information security and principles mark stamp" t = y20 xor y21
    
    y20 = register[20]
    y21 = register[21]
    
    t = int(y20)^int(y21)
    register = str(t) + register[:-1]
    
    return register
    

def step_z(register: str) -> str:
    """Stepping register Z

    :param register: Z register
    :return: new value of the Z register
    """
    # TODO: Implement this function
    ...
    #from page 53, "information security and principles mark stamp" t = z7 xor z20 xorz21 xor z22
    
    z7 = register[7]
    z20 = register[20]
    z21 = register[21]
    z22 = register[22]
    
    t = int(z7)^int(z20)^int(z21)^int(z22)
    register = str(t) + register[:-1]
    return register


def generate_bit(x: str, y: str, z: str) -> int:
    
    """Generate a keystream bit

    :param x: X register
    :param y: Y register
    :param z: Z register
    :return: a single keystream bit
    """
    # TODO: Implement this function
    ...
      
    #from page 54, we see that a single key stream is generated as x18 xor y21 xor z22
    x=x[18]
    y=y[21]
    z=z[22]
    single_key_stream_bit= int(x)^int(y)^int(z)
    return single_key_stream_bit


def generate_keystream(plaintext: str, x: str, y: str, z: str) -> str:
    """Generate stream of bits to match length of plaintext

    :param plaintext: plaintext to be encrypted
    :param x: X register
    :param y: Y register
    :param z: Z register
    :return: keystream of the same length as the plaintext
    """
    # TODO: Implement this function
    ...
    answer =""
    binarytext = ""
    
    for character in plaintext:
        binarytext = binarytext + bin(ord(character))[2:].zfill(8)
        
    for i in range(0,len(binarytext)):
        mj = majority(x[8], y[10], z[10])
        if x[8]== mj:
            x = step_x(x)
            
        if y[10]==mj:
            y = step_y(y)
        
        if z[10] == mj:
            z = step_z(z)
            
        keystream = generate_bit(x,y,z)
        answer = answer + str(keystream)
    
    return answer

def encrypt(plaintext: str, keystream: str) -> str:
    """Encrypt plaintext using A5/1

    :param plaintext: plaintext to be encrypted
    :param keystream: keystream
    :return: ciphertext
    """
    # TODO: Implement this function
    ...
    
    ciphertext = ""
    binarytext = ""
    for character in plaintext:
        binarytext = binarytext + bin(ord(character))[2:].zfill(8)

    for i in range(0,len(binarytext)):
        
        ciphertext = ciphertext + str(int(binarytext[i])^int(keystream[i]))
        
    return ciphertext

    
def decrypt(ciphertext: str, keystream: str) -> str:
    """Decrypt ciphertext using A5/1

    :param ciphertext: ciphertext to be decrypted
    :param keystream: keystream
    :return: plaintext
    """
    # TODO: Implement this function
    ...
    plaintext = ""
    binarytext = ""
    for character in ciphertext:
        binarytext = binarytext + chr(ord(character))

    for i in range(0,len(binarytext)):
        
        plaintext = plaintext + str(int(binarytext[i])^int(keystream[i]))
        
        
        
    return plaintext
    
    # plaintext = ""
    
    # for i in range(len(ciphertext)):
    #     character = ciphertext[i]
        
    #     plaintext = plaintext + (chr(ord(character)^ord(keystream[i])))
        
    # return plaintext
    # plaintext = ""
    # binarytext = []
    
    # i = 0
    # while(i<len(ciphertext)):
    #     binarytext.insert(i,int(ciphertext[i]))
        
    #     plaintext = plaintext + str(binarytext[i]^keystream[i])
        
    #     i+=1
    # return (str(plaintext))
    
    # for character in ciphertext:
    #     binarytext = binarytext + bin(ord(character))[2:].zfill(8)

    # for i in range(0,len(binarytext)):
        
    #     plaintext = plaintext + str(int(binarytext[i])^int(keystream[i]))
        
    # return ciphertext


def encrypt_file(filename: str, secret: str) -> None:
    """Encrypt a file

    For the sake of output comparison you should preserve end-of-line (\n) symbols
    in the output file.

    :param filename: filename to be encrypted
    :param secret: secret to initialize registers
    :return: write the result to filename.secret
    """
    # TODO: Implement this function
    ...
    r = open(filename, "r")
    w = open("data/projects/a51/preamble.secret", "w")
    w = open("data/projects/a51/simple.secret", "w")
    
    for line in r:
        x, y, z = populate_registers(secret)
        keystream = generate_keystream(line, x, y, z)
        
        w.write(hex(int(encrypt(line, keystream), 2)) + '\n')


def main():
    """Main function"""
    # NOTE: Use this space as you see fit
    ...
    encrypt_file("data/projects/a51/preamble","constitution")
    encrypt_file("data/projects/a51/simple","")
    
    r = sha256(open("data/projects/a51/roster.secret", "rb").read()).hexdigest()
    


if __name__ == "__main__":
    main()
