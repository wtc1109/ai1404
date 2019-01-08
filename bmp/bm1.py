from PIL import Image


img = Image.open('8m.bmp')
img2 = img.load()
width = img.size[0]
height = img.size[1]
rgb_bytes = bytearray(width*height*3)
red_index = 0
green_index = 1
blue_index = 2
for y in range(height):
    for x in range(width):
        r,g,b = img2[x,y]
        M = max(r,g,b)
        m = min(r,g,b)
        C = M-m
        if 0 == C:
            h1 = 0

        elif M == r:
            h1 = 1.0*(g-b)/C
            while h1 > 6:
                h1 -= 6
        elif M == g:
            h1 = 1.0*(b-r)/C +2
        elif M == b:
            h1 = 1.0*(r-g)/C +4
        H = h1*60
        Y = 0.299*r + 0.586*g + 0.114*b
        y2 = (Y*Y*Y/(180*180*180))**0.5
        r1 = r*y2
        g1 = g*y2
        b1 = b*y2
        """
        if Y < 40:
            R = 0
            G = 0
            B = 0
        elif Y > 140:
            R = 255
            G = 255
            B = 255
        else:
            if H > 210 and H < 270:
                R = r
                G = g
                B = b
            else:
                R = r
                G = g
                B = b
        """

        R = int(min(r1,255))
        G = int(min(g1,255))
        B = int(min(b1,255))
        """
        if H > 235 and H < 245:
            R = 0
            G = 0
            B = 255
        """
        rgb_bytes[red_index] = R
        rgb_bytes[green_index] = G
        rgb_bytes[blue_index] = B
        red_index += 3
        green_index += 3
        blue_index += 3

img = Image.frombytes("RGB", (width,height), bytes(rgb_bytes))
img.save("8m_1.jpg", "JPEG")
img.save("8m_1.bmp", "BMP")

print '1'