import exifread
from PIL import Image
from PIL.ExifTags import TAGS
import piexif
img = Image.open("org.jpg")
img2 = Image.open("123.jpg")
print img.app["COM"]
img.app.update({"COM":"ABCDEFEG"})
img.applist.append(('COM','ADBCDEFG'))

if hasattr(img, '_getexif'):
    exifinfo = img._getexif()
    if None != exifinfo:
        for tag, value in exifinfo.items():
            decoded = TAGS.get(tag, tag)
            print decoded

filein = open("org.jpg","rb")
da = exifread.process_file(filein, debug=True)
f2 = open("org2.jpg","rb")
da2 = exifread.process_file(f2)
filein.close()
f2.close()
exif_dict2 = piexif.load("org.jpg")
im = Image.open("org.jpg")
exif_dict = piexif.load(im.info["exif"])
w,h = im.size
print exif_dict["0th"]
exif_dict["0th"][piexif.ImageIFD.XResolution] = (w,1)
exif_dict["0th"][piexif.ImageIFD.YResolution] = (h,1)
exif_dict["Exif"][piexif.ExifIFD.UserComment] = "wyscsddgdfg"
#exif_dict.update({"Image":{305:"wyscsddgdfg"}})
exif_dict["0th"][piexif.ImageIFD.Software] = "1212122wyscsddgdfg"
exif_bytes = piexif.dump(exif_dict)
im.app.update({"COM":"ABCDEFEG"})
im.applist.append(('COM','ADBCDEFG'))
encd = Image._getencoder()
im.save("oorg.jpg","jpeg",exif=exif_bytes,app=im.app, applist=im.applist,encoderinfo=im.encoderinfo)
im2 = Image.open("oorg.jpg")
exif_dict21 = piexif.load("oorg.jpg")
print da