import numpy,matplotlib
from PIL import Image


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


def yuv444_torgb888_list(width, height, yuv):
    rgb_bytes = bytearray(width*height*3)

    red_index = 0
    green_index = 1
    blue_index = 2
    y_index = 0
    for row in range(height):
        u_index = width*height+(row)*(width)
        v_index = width*height*2+(row)*(width)
        for column in range(width):
            Y = yuv[y_index]
            U = yuv[u_index]
            V = yuv[v_index]
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


def f2(fi, fo, w, h):
    print "open file"
    f = open(fi, "rb")
    yuv = f.read()
    f.close()
    _y = numpy.array(bytearray(yuv), dtype=numpy.uint8)
    #_b = _y[2179]
    _pix_all = w*h
    _y_average = numpy.average(_y[:_pix_all])
    #_y_mean = numpy.mean(_y[:9240])
    yuv2=[]
    for i in range(_pix_all):
        if _y[i] > _y_average:
            yuv2.append(_y[i])
        else:
            yuv2.append(0)
    for i in range(_pix_all):
        if _y[i] > _y_average:
            yuv2.append(_y[i+_pix_all])
        else:
            yuv2.append(128)
    for i in range(_pix_all):
        if _y[i] > _y_average:
            yuv2.append(_y[i+_pix_all+_pix_all])
        else:
            yuv2.append(128)

    _y_nz = 0
    for i in range(_pix_all):
        if 0 != yuv2[i]:
            _y_nz += 1
    _y_average2 = numpy.sum(yuv2[:_pix_all])/_y_nz
    yuv3 = []
    for i in range(_pix_all):
        if yuv2[i] > _y_average2:
            yuv3.append(yuv2[i])
        else:
            yuv3.append(0)
    for i in range(_pix_all):
        if yuv2[i] > _y_average2:
            yuv3.append(yuv2[i + _pix_all])
        else:
            yuv3.append(128)
    for i in range(_pix_all):
        if yuv2[i] > _y_average2:
            yuv3.append(yuv2[i + _pix_all + _pix_all])
        else:
            yuv3.append(128)

    rgb_bytes = yuv444_torgb888(w, h, yuv)
    img = Image.frombytes("RGB", (w, h), bytes(rgb_bytes))
    data1 = numpy.array(rgb_bytes,dtype=numpy.uint8)
    data2 = data1.reshape(_pix_all,3)
    img.save("%s.bmp"%fo, "BMP")

    rgb_bytes2 = yuv444_torgb888_list(w, h, yuv2)
    img = Image.frombytes("RGB", (w, h), bytes(rgb_bytes2))
    img.save("%s_2.bmp"%fo, "BMP")
    print "bmp"

    rgb_bytes3 = yuv444_torgb888_list(w, h, yuv3)
    img = Image.frombytes("RGB", (w, h), bytes(rgb_bytes3))
    img.save("%s_3.bmp" % fo, "BMP")
    print "bmp"

if __name__ == '__main__':
   f2("1_1534780442_235402_G16_E2106159_Y80_U138_V120_45730_404_774_543_839_140x66.yuv","442",140,66)
   f2("1_1534759013_175653_G16_E2106159_Y90_U131_V125_2478_838_640_957_689_120x50.yuv", "9013", 120, 50)