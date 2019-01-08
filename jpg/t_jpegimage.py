from PIL import JpegImagePlugin
from PIL import Image, ImageFile, _binary
import struct,binascii
fd = open("124.jpg")
fd2 = open("125.jpg","wr")
fdp = fd.read()
fd.close()
msg1 = "hello xxsfsdf"

msg = struct.pack(">BBH%ds"%len(msg1),255,254,len(msg1)+2,msg1)
print binascii.hexlify(msg)
fd2.write(fdp[:2])
fd2.write(msg)
fd2.write(fdp[2:])
fd2.close()
img = Image.open("125.jpg")
info1 = JpegImagePlugin(img)
print info1