from Crypto.Cipher import AES
iv = b'\0'*16
#obj = AES.new("hsylgwk-2012aaaa", AES.MODE_ECB, 'This is an IV456')
obj = AES.new("hsylgwk-2012aaaa", AES.MODE_ECB, "hsylgwk-2012aaaa")
message = "1234567890"
message += b'\6'*6
out1 = ''
for i in range(16):
    out1 += "%02X"%ord(message[i])
ciphertext = obj.encrypt(message)
out = ''
for i in range(16):
    out += "%02X"%ord(ciphertext[i])
obj2 = AES.new("hsylgwk-2012aaaa", AES.MODE_ECB, 'This is an IV456')
msg = obj2.decrypt(ciphertext)
print msg