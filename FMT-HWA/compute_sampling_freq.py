import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# import the correlation data
data_corr = np.loadtxt("./data/CorrelationTest", delimiter='\t', skiprows=23)

def estimated_autocorrelation(x):
    n = len(x)
    x = x-x.mean()
    r = np.correlate(x, x, mode = 'full')[-n:]
    result = r/r[0]
    return result

idx_time = 100
corrcoef = estimated_autocorrelation(data_corr[:, 1])[:idx_time]
fig = plt.figure(constrained_layout=True, dpi=150)
plt.plot(data_corr[:idx_time, 0]*1e3, corrcoef, label="signal", marker='.')

# plot threshold correlation
plt.axhline(y=0.1, xmin=0, xmax=data_corr[idx_time, 0]*1e3, c='k', label=r"$\rho_{x}$")

# get interp1d function to find threshold accurately
corr_time_interp = interp1d(corrcoef, data_corr[:idx_time, 0])
corr_interp = interp1d(data_corr[:idx_time, 0], corrcoef)
# get the time of this corr. coeff.
time = float(corr_time_interp(0.1))
time_sampling = 1 / (2 * time)

# plot intersection
plt.scatter(time*1e3, corr_interp(time), c='C01', zorder=3)

plt.text(time*1e3+0.1, corr_interp(time) + 0.005, s=r"$T_{i}=3.2ms$")

plt.xlabel('time (ms)', fontsize=14)
plt.ylabel(r'$\rho_{x}$ [-]', fontsize=14)
plt.legend(prop={"size": 14})
plt.grid()