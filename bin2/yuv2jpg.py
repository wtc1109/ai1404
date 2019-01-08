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


def yuv2jpg(fi, fo, w, h):
    print "open file"
    f = open(fi, "rb")
    yuv = f.read()
    f.close()

    rgb_bytes = yuv444_torgb888(w, h, yuv)

    img1 = Image.frombytes("RGB", (w, h), bytes(rgb_bytes))

    #ImagePIL.Image.save(img1, fo, "JPEG", quality=99)
    img1.save(fo, "JPEG", quality=99)
