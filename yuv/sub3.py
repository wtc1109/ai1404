import os, numpy
import matplotlib.pyplot as plt
import scipy
from scipy import stats

if __name__ == '__main__':
    _files = sorted(os.listdir('1808433005'))
    if not os.path.isdir('sub1'):
        os.mkdir('sub1')
    di = numpy.fromfile('1808433005/' + _files[0], dtype=numpy.uint8, count=500 * 500).reshape(500, 500)
    x = numpy.arange(0,500,1)

    for _file in _files:
        di2 = numpy.fromfile('1808433005/'+_file, dtype=numpy.uint8, count=500*500).reshape(500,500)
        do = numpy.zeros((500,500), dtype=numpy.uint8).reshape(500,500)
        y1 = numpy.arange(0,500,1)
        for i in range(500):
            for j in range(500):
                do[i][j] = int(max(di2[i][j],di[i][j]) - min(di2[i][j],di[i][j]))
        for i in range(500):
            y1[i] = numpy.mean(do[i][:])
        gmean = stats.gmean(y1)
        _filen1 = _file.split('_')[0]
        do.tofile('sub1/'+_filen1+'_%f.yuv'%gmean)
        """
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.plot(x, y1, label='bb');
        ax1.set_ylabel('Y values for exp(-x)');
        ax2 = ax1.twinx()  # this is the important function

        plt.show()
        y2 = numpy.array([int(numpy.mean(do))]*500)
        y3 = numpy.arange(0,500,1)
        corrcoef = numpy.corrcoef(y1,y2)
        print corrcoef[0][1]
        corrcoef2 = numpy.corrcoef(y1,y3)
        """
        di = di2.copy()
        print _file