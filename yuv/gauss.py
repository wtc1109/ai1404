import os, numpy

kerner_5x5 = numpy.array([
    [1,4,7,4,1],
    [4,16,26,16,4],
    [7,26,41,26,7],
    [4,16,26,16,4],
    [1,4,7,4,1]
])


if __name__ == '__main__':
    _files = sorted(os.listdir('1808433005'))
    if not os.path.isdir('gauss'):
        os.mkdir('gauss')
    #di = numpy.fromfile('1808433005/' + _files[0], dtype=numpy.uint8, count=500 * 500).reshape(500, 500)
    for _file in _files:
        di2 = numpy.fromfile('1808433005/'+_file, dtype=numpy.uint8, count=500*500).reshape(500,500)
        do = numpy.zeros((500,500), dtype=numpy.uint8).reshape(500,500)
        for i in range(2,500-3,1):
            for j in range(2,500-3,1):
                do[i][j] = (di2[i-2][j-2] + di2[i-1][j-2]*4 + di2[i][j-2]*7 + di2[i+1][j-2]*4 + di2[i+2][j-2] +
                            di2[i - 2][j - 1]*4 + di2[i - 1][j - 1] * 16 + di2[i][j - 1] * 26 + di2[i + 1][j - 1] * 16 +
                            di2[i + 2][j - 1] * 4 +
                            di2[i - 2][j] * 7 + di2[i - 1][j] * 26 + di2[i][j] * 41 + di2[i + 1][j] * 26 + di2[i + 2][j] * 7 +
                            di2[i - 2][j + 1] * 4 + di2[i - 1][j + 1] * 16 + di2[i][j + 1] * 26 + di2[i + 1][
                                j + 1] * 16 +
                            di2[i + 2][j + 1] * 4 +
                            di2[i - 2][j + 2] + di2[i - 1][j + 2] * 4 + di2[i][j + 2] * 7 + di2[i + 1][
                                j + 2] * 4 +
                            di2[i + 2][j + 2]
                            )/273
        _mean = numpy.mean(do)
        do.tofile('gauss/'+_file.split('_')[0]+"_%d.yuv"%_mean)
        print _file