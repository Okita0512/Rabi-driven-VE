import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

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

folder_names = sorted(
    [
        name
        for name in os.listdir(".")
        if os.path.isdir(name) and os.path.exists(os.path.join(name, "pop_summary.csv"))
    ],
    key=lambda x: float(x),
)

if not folder_names:
    raise FileNotFoundError("No subfolder with pop_summary.csv was found.")

all_data = []
for folder in folder_names:
    data = np.genfromtxt(os.path.join(folder, "pop_summary.csv"), delimiter=",", names=True)
    all_data.append(data)
    plt.plot(data["cv"], data["P_g_n1_avg"], "-", label=f"{folder}")

# set x-limits from all loaded data
x_min = min(np.min(data["cv"]) for data in all_data)
x_max = max(np.max(data["cv"]) for data in all_data)

# legend location, font & markersize
plt.legend(loc = 'upper left', frameon = False, prop = font, markerscale = 1, ncol = 1)
# plt.legend(title = '(a)', loc = 'upper left', bbox_to_anchor=(legend_x, legend_y), frameon = False, title_fontsize = legendsize)

# ==============================================================================================

plt.show()
