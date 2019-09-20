import matplotlib.pyplot as plt
import numpy as np
# plt.plot([1,2,3,4], [1,4,9,16], 'ro')
# plt.axis([0, 6, 0, 20])
# plt.show()
fig = plt.figure()
ax = plt.axes()

for x in range(1,20):
    ax.plot(x, 1/x);
plt.show()
