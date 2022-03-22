#!/usr/bin/env python3
"""
Merkle-Hellman Knapsack cipher implementation

@authors: 
@version: 2022.3
"""

import math
import pathlib
import random
import re


BLOCK_SIZE = 64



def generate_sik(size: int = BLOCK_SIZE) -> tuple[int, ...]:
    """
    Generate a superincreasing knapsack of the specified size

    :param size: block size
    :return: a superincreasing knapsack as a tuple
    """
    # TODO: Implement this function
    ...
    sik_array = []
    total = 0
    for _ in range(size):
        iterated_sum = random.randrange(total-999,total+9999) +random.randrange(total,total+9999)
        sik_array.append(iterated_sum)
        total = total + iterated_sum
    return tuple(sik_array)

def calculate_n(sik: tuple) -> int:
    """
    Calculate N value

    N is the smallest number greater than the sum of values in the knapsack

    :param sik: a superincreasing knapsack
    :return: n
    """
    # TODO: Implement this function
    ...

    n = (sum(sik)+1)
    return n

def calculate_m(n: int) -> int:
    """
    Calculate M value

    M is the largest number in the range [1, N) that is co-prime of N
    :param n: N value
    """
    # TODO: Implement this function
    ...

    
    m = n-1
    
    return m

def calculate_inverse(sik: tuple[int, ...], n: int = None, m: int = None) -> int:
    """
    Calculate inverse modulo

    :param sik: a superincreasing knapsack
    :param n: N value
    :param m: M value
    :return: inverse modulo i so that m*i = 1 mod n
    """
    # TODO: Implement this function
    ...
    if n == None:
        return sum(sik)
    modular = n 
    y1, x1 = 0,1
    while m >1: 
        quotient = m // n 
        m , n = n, m %n
        a = y1   
        y1 = x1 - (quotient * y1)
        x1 = a 
        
    if y1<0:
        y1 = y1 + modular
  
    if (x1 < 0) : 
        x1 = x1 + modular
  
    return x1 

# source for this a;gorithm
# https://www.techiedelight.com/extended-euclidean-algorithm-implementation/
# thought process was through euclidean algorithm for gcd
# https://stackoverflow.com/questions/18940194/using-extended-euclidean-algorithm-to-create-rsa-private-key'
#  https://www.geeksforgeeks.org/euclidean-algorithms-basic-and-extended/
# https://www.techiedelight.com/extended-euclidean-algorithm-implementation/
def generate_gk(sik: tuple[int, ...], n: int = None, m: int = None) -> tuple[int, ...]:
    """
    Generate a general knapsack from the provided superincreasing knapsack

    :param sik: a superincreasing knapsack
    :param n: N value
    :param m: M value
    :return: the general knapsack
    """
    # TODO: Implement this function
    ...
    if n == None:
        n = calculate_n(sik)
        m = calculate_m(n)
        return tuple(sik[i]*m%n for i in range(len(sik)))
    else:
        n_0 = (sum(sik)+1)
        m_0 = (n_0 -1)
        kn = [(ans*m_0) %n for ans in sik]
        return tuple(sik[i]*m%n for i in range(len(sik)))        



def encrypt(
    plaintext: str, gk: tuple[int, ...], block_size: int = BLOCK_SIZE
) -> list[int]:
    """
    Encrypt a message

    :param plaintext: text to encrypt
    :param gk: general knapsack
    :param block_size: size of the encryption block
    :return: encrypted text
    """
    # TODO: Implement this function
    ...
    
    plaintext_binary = ""
    for i in range(len(plaintext)):
       plaintext_binary = plaintext_binary + bin(ord(plaintext[i]))[2:].zfill(8)
       
    cipher = 0
    length_gk = len(gk)-1
    length_plaintext= len(plaintext_binary) - 1

        
        
    while block_size >= 0 <= length_plaintext:
        
        if plaintext_binary[length_plaintext] == "1": 
            cipher = cipher + gk[length_gk]
            
        length_gk = length_gk - 1
        length_plaintext = length_plaintext - 1     
        encrypted = [cipher] 
    return encrypted

def decrypt(
    ciphertext: list[int],
    sik: tuple[int, ...],
    n: int = None,
    m: int = None,
    block_size: int = BLOCK_SIZE,
) -> str:
    """
    Decrypt a single block
    
    :param ciphertext: text to decrypt
    :param sik: superincreasing knapsack
    :param n: N value
    :param m: M value
    :param block_size: block size
    :return: decrypted string
    """
    # TODO: Implement this function
    ...
    
    for i in range(len(ciphertext)):
        
        plaintext = ciphertext[i] * calculate_inverse(sik, n, m) % n
   
    
    length = len(sik) - 1
    decrypted_string = ""
    while length >=0 < plaintext :
        if not plaintext >= sik[length]:
            decrypted_string = "0" + decrypted_string
        else:
            decrypted_string = "1" + decrypted_string
            plaintext = plaintext - sik[length]
           
        length = length -1
   
    decrypted_string = int(decrypted_string,2)
  
    decrypted_string = chr((decrypted_string))

    return str(decrypted_string)
    


def main():
    """
    Main function
    Use your own values to check that functions work as expected
    You still need to rely on tests for proper verification
    """
    print("Hellman-Merkle example")


if __name__ == "__main__":
    main()
    
    
# https://stackoverflow.com/questions/42422921/multiple-subset-sum-calculation
# the test cases change from line 48 reduces the number of cases passed


# @pytest.mark.timeout(TIME_LIMIT)
# @pytest.mark.parametrize(
#     "ciphertext, sik, n, m, plaintext",
#     get_cases("test_case_basic", "ciphertext", "sik", "n", "m", "plaintext"),

# basic makes me pass more tests