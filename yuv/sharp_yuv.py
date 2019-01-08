import os, shutil, numpy

if __name__ == '__main__':
    _files = sorted(os.listdir('1808433005'))
    if not os.path.isdir('sharp'):
        os.mkdir('sharp')
    for _file in _files:
        fdatai = numpy.fromfile('1808433005/'+_file, dtype=numpy.uint8, count=500*500).reshape(500,500)


        for i in range(500):
            for j in range(500):
                fdatai[i][j] = fdatai[i][j]&0xF8
        fdatai.tofile('sharp/'+_file)
