import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator, tick_params
import numpy as np
from numpy import polyfit, poly1d
plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams["font.family"] = "Helvetica"

fig, ax = plt.subplots()

font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
fig = plt.figure(figsize=(7, 7), dpi = 128)

# ================= global ====================

data = np.loadtxt("Evib_avg_time_avg_vs_N.txt")

plt.plot(1. / data[:,0], data[:,1], 'o-', label = r"$\langle E_{\mathrm{vib}} \rangle$", markersize = 6, color = 'navy')

def rsquare(x, y, degree):
    results = {}

    coeffs = polyfit(x, y, degree)

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y) / len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results

coeff = polyfit(1. / data[:, 0], data[:, 1], 1)

rsquare = rsquare(1. / data[:, 0], 1000 * data[:, 1], degree = 1)
print("1/N fit: ", rsquare)

plt.text(0.1, 0.05, r"$R^2$ $\approx$ %.4f" % rsquare['determination'], size = 15, color = 'red')

N0 = np.linspace(0.9, 10000)
plt.plot(1. / N0, coeff[0] / N0 + coeff[1], '--', color = 'red', label = "linear fitting")

# ==============================================================================================
#                                      plotting set up     
# ==============================================================================================

# x and y range of plotting 
time = 1.1             # x-axis range: (0, time)
y1, y2 = 0.0, 0.12     # y-axis range: (y1, y2)

# scale for major and minor locator
x_major_locator = MultipleLocator(0.5)
x_minor_locator = MultipleLocator(0.1)
y_major_locator = MultipleLocator(0.02)
y_minor_locator = MultipleLocator(0.01)

# x-axis and LHS y-axis
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.xaxis.set_minor_locator(x_minor_locator)
ax.yaxis.set_major_locator(y_major_locator)
ax.yaxis.set_minor_locator(y_minor_locator)
ax.tick_params(which = 'major', length = 8, labelsize = 10)
ax.tick_params(which = 'minor', length = 4)

x1_label = ax.get_xticklabels()
[x1_label_temp.set_fontname('Times New Roman') for x1_label_temp in x1_label]
y1_label = ax.get_yticklabels()
[y1_label_temp.set_fontname('Times New Roman') for y1_label_temp in y1_label]

plt.tick_params(labelsize = 20, which = 'both', direction = 'in')
plt.xlim(0.0, time)
plt.ylim(y1, y2)

# RHS y-axis
ax2 = ax.twinx()
ax2.yaxis.set_major_locator(y_major_locator)
ax2.yaxis.set_minor_locator(y_minor_locator)
ax2.tick_params(which = 'major', length = 8)
ax2.tick_params(which = 'minor', length = 4)
ax2.axes.yaxis.set_ticklabels([])

plt.tick_params(which = 'both', direction = 'in')
plt.ylim(y1, y2)

# name of x, y axis and the panel
ax.set_xlabel(r'$1 / N$', font = 'Times New Roman', size = 20)
ax.set_ylabel(r'$\langle E_{\mathrm{vib}} \rangle$ (eV)', font = 'Times New Roman', size = 20)
# ax.set_title('Average vibrational energy', font = 'Times New Roman', size = 20)

# legend location, font & markersize
ax.legend(loc = 'upper left', prop = font, markerscale = 1)
plt.legend(frameon = False)

# plt.show()

plt.savefig("Fig_Evib_avg_2.pdf", bbox_inches='tight')
