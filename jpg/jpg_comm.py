from pyexiv2 import ImageMetadata
if __name__ == '__main__':
    metadata1 = ImageMetadata('IMG_TEST_001.jpg')
    metadata1.read()
    info1 = metadata1._get_comment()
    print 'EXIF keys:', metadata1.exif_keys
    #img.close()