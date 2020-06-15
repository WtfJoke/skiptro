import numpy as np
import matplotlib.pyplot as plt

file = open("file1.aac.bin", "r")
samples = np.fromfile(file, dtype=np.int16)
plt.plot(samples)
plt.show()
