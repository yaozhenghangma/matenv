import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator


# Color list and label
colors = ['black', 'red', 'blue', 'green', 'purple', 'yellow', 'orange', 'grey']
labels = ['1', '2', '3', '4', '5', '6', '7', '8']
xlabel = 'xlabel'
ylabel = 'ylabel'


# Load data from file
data = np.loadtxt('test.dat')


# Width and length for horizontal lines
width_h = 2.0
length_h = 3.0


# Width and length for discontinues lines
width_d = 1.0
length_d = 3.0


# Data process
x_h1 = np.array([0, length_h])
y_h1 = np.zeros_like(x_h1)
x_h2 = np.array([length_d+length_h, length_d+2*length_h])
x_d1 = np.array([length_h, length_d+length_h])
x_d2 = np.array([2*length_h+length_d, 2*length_d+2*length_h])
y_h2_list = []
y_d1_list = []
y_d2_list = []
for i in np.arange(0, data.shape[0]):
    y_h2_list.append(np.full_like(x_h2, data[i, 1]))
    y_d1_list.append(np.array([0, data[i, 1]]))
    y_d2_list.append(np.array([data[i, 1], 0]))
x_h3 = np.array([2*length_d+2*length_h, 2*length_d+3*length_h])
y_h3 = np.zeros_like(x_h3)



# Plot Setting
font = {'family' : 'Times New Roman',
'weight' : 'regular',
'size' : 23
}

font_italic = {'family' : 'Times New Roman',
'style' : "italic",
'weight' : 'regular',
'size' : 23
}

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Times"],
})

figure_size = (8,6)
fig, ax = plt.subplots(figsize=figure_size) # (width, height) in inches

# tick setting
ax.spines["left"]
ax.tick_params(axis='both', which='major', direction='in', length=6, width=1.5, labelsize=20)
ax.tick_params(axis='both', which='minor', direction='in', length=4, width=1.5, labelsize=20)
ax.set_xticks([])
#ax.set_xlim(0, 0.1)
#ax.set_ylim(0, 0.2)
ax.yaxis.set_major_locator(MultipleLocator(0.1))
ax.yaxis.set_minor_locator(MultipleLocator(0.05))

# label setting
ax.set_xlabel(xlabel, font)
ax.set_ylabel(ylabel, font)

# frame setting
frameSize = 1.5
ax.spines['left'].set_linewidth(frameSize)
ax.spines['right'].set_linewidth(frameSize)
ax.spines['top'].set_linewidth(frameSize)
ax.spines['bottom'].set_linewidth(frameSize)


# Plot
ax.plot(x_h1, y_h1, color=colors[0], linewidth=width_h)
ax.plot(x_h3, y_h3, color=colors[0], linewidth=width_h)
for i in np.arange(0, data.shape[0]):
    ax.plot(x_d1, y_d1_list[i], color=colors[i], linestyle='--', linewidth=width_d)
    ax.plot(x_d2, y_d2_list[i], color=colors[i], linestyle='--', linewidth=width_d)
    ax.plot(x_h2, y_h2_list[i], color=colors[i], linestyle='-', label=labels[i], linewidth=width_h)

ax.legend(loc='best', frameon=False, handlelength=1.2, prop=font)
fig.tight_layout()
plt.savefig("split.png", format='png', dpi=600)