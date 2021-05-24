import numpy as np
import matplotlib.pyplot as plt

# import the correlation data
data_corr = np.loadtxt("./data/CorrelationTest", delimiter='\t', skiprows=23)

def estimated_autocorrelation(x):
    n = len(x)
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    result = r/r[0]
    return result

plt.plot(data_corr[:, 0]*1e3, estimated_autocorrelation(data_corr[:, 1]))
plt.xlabel('time (s)')
plt.ylabel(r'$\rho_{x}$')
plt.show()