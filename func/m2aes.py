from M2Crypto.EVP import Cipher
from M2Crypto import m2
from M2Crypto import util
import binascii

ENCRYPT_OP = 1
DECRYPT_OP = 0
hex1= binascii.a2b_hex("abcd")
hex2 = ord(hex1[0])
iv = '\0' * 16  # init not used for aes_128_ecb
PRIVATE_KEY = "hsylgwk-2012aaaa"


def Encrypt(data):

    cipher = Cipher(alg='aes_128_ecb', key=PRIVATE_KEY, iv=iv, op=ENCRYPT_OP)
    buf = cipher.update(data)
    buf = buf + cipher.final()
    del cipher

    output = ''
    for i in buf:
        output += '%02X' % (ord(i))
    return output


def Decrypt(data):

    #data = util.h2b(data)
    data1 = binascii.a2b_hex(data)
    #for i in len(data)/2:
    #    data1 += binascii.a2b_hex()
    cipher = Cipher(alg='aes_128_ecb', key=PRIVATE_KEY, iv=iv, op=DECRYPT_OP)
    buf = cipher.update(data1)
    buf = buf + cipher.final()
    del cipher
    return buf

if __name__ == '__main__':
    enc = Encrypt("1234567890")
    """2AE607673874F6DC8EC15C40E5645AF3
"""
    num = b'\0\0\0\0'
    print len(num)
    dec = Decrypt(enc)
    print dec