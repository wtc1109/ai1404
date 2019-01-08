#import Tyf
from PIL import Image
#from PIL import JpegImagePlugin
import piexif



def yuv444_torgb888(width, height, yuv):
    rgb_bytes = bytearray(width*height*3)

    red_index = 0
    green_index = 1
    blue_index = 2
    y_index = 0
    for row in range(height):
        u_index = width*height+(row)*(width)
        v_index = width*height*2+(row)*(width)
        for column in range(width):
            Y = ord(yuv[y_index])
            U = ord(yuv[u_index])
            V = ord(yuv[v_index])
            C = (Y-16)*298
            D = U-128
            E = V-128
            R = (C + 409*E + 128)//256
            G = (C - 100*D -208*E + 128)//256
            B = (C + 516*D + 128) // 256
            R = 255 if(R>255) else (0 if(R < 0) else R)
            G = 255 if(G > 255) else (0 if(G < 0) else G)
            B = 255 if(B > 255) else (0 if(B < 0) else B)
            rgb_bytes[red_index] = R
            rgb_bytes[green_index] = G
            rgb_bytes[blue_index] = B
            u_index += 1
            v_index += 1
            y_index += 1
            red_index += 3
            green_index += 3
            blue_index += 3
    return rgb_bytes

def FtestConversion(source, dest):
    print "open file"
    f = open(source,"rb")
    yuv = f.read()
    f.close()
    str1 = source.split('_')
    str2 = str1[-1].split('.')
    str3 = str2[0].split('x')
    _width = int(str3[0])
    _height = int(str3[1])
    rgb_bytes = yuv444_torgb888(_width,_height,yuv)
    img = Image.frombytes("RGB",(_width,_height),bytes(rgb_bytes))

    img.save(dest, "JPEG",quality=99)

    img=Image.open("icc_profile_big.jpg")
    """
    _app_list = img.app
    img.app.update({"COM":"102738762"})
    #img.app["COM"] = "102738762"
    img.applist.pop()
    img.applist.append(("COM","102738762"))
    del img.app["APP1"]
    """
    #JpegImagePlugin.COM(img,"907988768667")
    #fp = img.tempfile("125.jpg")
    #img.save("125.jpg")
    #img.applist.pop()
    #img.save("111.jpg")

    img = Image.open("111.jpg")
    _exif = piexif.load("1603430078.jpeg")
    img2 = Image.open("1603430078.jpeg")
    #img3 = Tyf.open("test/IMG_TEST_001.jpg")
    img2.close()
    _exif_dict_ifd = {piexif.ExifIFD.ImageUniqueID:"adcdg",piexif.ExifIFD.ISOSpeed:100}
    _zero_ifd = {piexif.ImageIFD.Software:"ojerg",piexif.ImageIFD.Artist:"sdfhn",piexif.ImageIFD.UniqueCameraModel:"12378962386",
                 piexif.ImageIFD.ExifTag:1,}
    _gps_ifd = {piexif.GPSIFD.GPSDestLatitudeRef:"sdfryh"}
    _exif.update({"0th":_zero_ifd})
    _exif_dict = {"0th":_zero_ifd,"Exif":_exif_dict_ifd,"GPS":_gps_ifd}
    _exif_str = piexif.dump(_exif_dict)
    img.save("11.jpg",exif=_exif_str)
   
    #img.show()
    #img.close()

def f2(fi, fo, w, h):
    print "open file"
    f = open(fi, "rb")
    yuv = f.read()
    f.close()

    rgb_bytes = yuv444_torgb888(w, h, yuv)
    img = Image.frombytes("RGB", (w, h), bytes(rgb_bytes))

    img.save(fo, "JPEG", quality=99)

if __name__ == '__main__':

    f2("1532399921_103841_G46_E79687_Y122_U89_V141_281.yuv",'ab.jpg',246,100)
    FtestConversion("1_1523117076_272109_000436135_37_15_157_75_162x78.yuv", "1.jpg")
    FtestConversion("1_1523173402_1210_154322396_42_16_102_37_116x40.yuv", "2.jpg")