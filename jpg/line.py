from PIL import ImageDraw, Image
import glob

if __name__ == '__main__':
    img = Image.open('11.jpg')
    draw = ImageDraw.Draw(img)
    draw.line((0,0,200,200),fill=0xFF)
    img.save('l11.jpg')
    f1 = glob.glob("l1*.jpg")
    pass