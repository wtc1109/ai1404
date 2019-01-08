import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc

time = np.arange(10)
data1,data2 = np.random.random(10)*30,np.random.random(10)*100-10

fig = plt.figure()
ax = fig.add_subplot(111)

lns1 = ax.plot(time, data1, '-', label = 'data1')

ax2 = ax.twinx()
lns2 = ax2.plot(time, data2, '-r', label = 'data2')
ax2.tick_params(axis='y', colors='red') # scale color
ax2.spines['right'].set_color('red') # Y asis color
#setp(ax2.get_yticklabels(),color='r') # label color
lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax.legend(lns, labs, loc=0)

ax.grid()
ax.set_xlabel("Time")
ax.set_ylabel(r"Radiation ")
ax2.set_ylabel(r"Temperature")

ax2.set_ylim(-20,100)
ax.set_ylim(0, 35)
plt.savefig("using2.png",format='png')
plt.show()