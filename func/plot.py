import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

x = np.arange(0., np.e, 0.01)
y1 = np.exp(-x)
y2 = np.log(x+1)
fig = plt.figure()
ax1 = fig.add_subplot(111)
ax1.plot(x, y1,label='bb');
ax1.set_ylabel('Y values for exp(-x)');
ax2 = ax1.twinx() # this is the important function

ax2.plot(x, y2, 'r',label = 'aa');
ax2.set_xlim([0, np.e]);
ax2.set_ylabel('Y values for ln(x)');
ax2.set_xlabel('Same X for both exp(-x) and ln(x)');
ax1.legend()
ax2.legend(loc=0)
plt.savefig("using.png",format='png')
plt.show()