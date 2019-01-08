import os, numpy
import matplotlib.pyplot as plt
import scipy
from scipy import stats
import math

if __name__ == '__main__':
    _files = sorted(os.listdir('sub1'))
    if not os.path.isdir('sub11'):
        os.mkdir('sub11')
    di = numpy.fromfile('sub1/' + _files[0], dtype=numpy.uint8, count=500 * 500).reshape(500, 500)
    x = numpy.arange(0,500,1)

    for _file in _files:
        di2 = numpy.fromfile('sub1/'+_file, dtype=numpy.uint8, count=500*500).reshape(500,500)
        do = numpy.zeros((500,500), dtype=numpy.uint8).reshape(500,500)
        y1 = numpy.arange(0,500,1)
        y2 = numpy.arange(0.0, 500, 1)
        _gmean = math.ceil(float(_file.split('_')[1].split('.')[0]))
        for i in range(500):
            for j in range(500):
                if di2[i][j] > _gmean:
                    do[i][j] = di2[i][j] - _gmean
        for i in range(500):
            y1[i] = numpy.mean(do[i][:])
            y2[i] = y1[i] * y1[i]
        gmean1 = stats.gmean(y1)
        gmean2 = numpy.mean(y2)
        cnt = 0
        cnt4 = 0
        cnt6 = 0
        _2gmean2 = 2* gmean2
        _4gmean2 = 4 * gmean2
        _6gmean2 = 6 * gmean2
        for i in range(500):
            if y2[i] < 400:
                continue
            if y2[i] > _2gmean2:
                cnt += 1
            if y2[i] > _4gmean2:
                cnt4 +=1
            if y2[i] > _6gmean2:
                cnt6 += 1
        _filen = _file.split('.')
        do.tofile('sub11/'+_filen[0]+'.'+_filen[1]+'_%f_%f_%d.yuv'%(gmean1, gmean2, cnt))

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(x, y1, label='mean');
        ax1.set_ylabel('Y values for exp(-x)');
        ax2 = ax1.twinx()  # this is the important function

        ax2.plot(x, y2, 'r', label='y1^2')
        ax2.set_xlim([min(x) - 1, max(x) + 1])
        ax2.set_ylabel('100% Percent')
        ax2.set_xlabel('Hour')
        ax1.legend()
        ax2.legend(loc=0)
        #plt.show()
        plt.savefig("sub11/%s_%d_%d_%d.png"%(_filen[0], cnt, cnt4, cnt6), format='png')
        plt.close()
        """
        y2 = numpy.array([int(numpy.mean(do))]*500)
        y3 = numpy.arange(0,500,1)
        corrcoef = numpy.corrcoef(y1,y2)
        print corrcoef[0][1]
        corrcoef2 = numpy.corrcoef(y1,y3)
        """
        di = di2.copy()
        print _file