import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.ticker import ScalarFormatter
from matplotlib.pyplot import MultipleLocator, tick_params
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def set_helvetica():
    candidates = []
    direct_path = r"C:\Windows\Fonts\Helvetica.ttf"
    if os.path.exists(direct_path):
        candidates.append(direct_path)
    for font_entry in fm.fontManager.ttflist:
        if font_entry.name.lower().startswith("helvetica"):
            candidates.append(font_entry.fname)
    for path in fm.findSystemFonts():
        if "helvetica" in os.path.basename(path).lower():
            candidates.append(path)
    if not candidates:
        return
    def font_score(path):
        name = os.path.basename(path).lower()
        score = 0
        if "regular" in name or "roman" in name:
            score -= 2
        if "bold" in name or "black" in name:
            score += 2
        if "italic" in name or "oblique" in name:
            score += 1
        return (score, len(name))
    best_path = sorted(candidates, key=font_score)[0]
    fm.fontManager.addfont(best_path)
    font_name = fm.FontProperties(fname=best_path).get_name()
    plt.rcParams["font.family"] = font_name

plt.rcParams['font.family'] = 'DeJavu Serif'
plt.rcParams["font.family"] = "Helvetica"
set_helvetica()

font = {'family':'Times New Roman', 'weight': 'roman', 'size':18}
fig = plt.figure(figsize=(6, 6), dpi = 128)
# fig.subplots_adjust(hspace = 0.2, wspace = 0.35)

legend_x, legend_y = - 0.35, 1.03
transparency = .4
legendsize = 48         # size for legend

# ==============================================================================================
#                                      Fig s4     
# ==============================================================================================

data = np.loadtxt("./0.20 - 1fs/Xg.dat")

plt.plot(data[:,0] / 1000, data[:,1], '-', label = r"1 fs")

data = np.loadtxt("./0.20 - 2fs/Xg.dat")

plt.plot(data[:,0] / 1000, data[:,1], '-', label = r"2 fs")

data = np.loadtxt("./0.20 - 5fs/Xg.dat")

plt.plot(data[:,0] / 1000, data[:,1], '-', label = r"5 fs")

data = np.loadtxt("./0.20 - 10fs/Xg.dat")

plt.plot(data[:,0] / 1000, data[:,1], '-', label = r"10 fs")

data = np.loadtxt("./0.20 - 20fs/Xg.dat")

plt.plot(data[:,0] / 1000, data[:,1], '-', label = r"20 fs")


plt.show()
# plt.savefig("FigS6-2.pdf", bbox_inches='tight')
