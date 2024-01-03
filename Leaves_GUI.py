import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

# Creating the main window.
root = tk.Tk()
root.title("RSRP and Temperature over Time")

# Creating the figure and axes.
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(8, 6))

# Creating some data.
np.random.seed(0)
rolling_avg_rsrp = pd.Series(np.random.rand(100), index=pd.date_range(start='2020-01-01', periods=100, freq='D'))
rolling_avg_temp = pd.Series(np.random.rand(100), index=pd.date_range(start='2020-01-01', periods=100, freq='D'))

# Determining the starting index.
start_idx = 0

# Determining the previous month.
prev_month = rolling_avg_rsrp.index[0].month

# Plotting the data.
sinr_segment = rolling_avg_rsrp[start_idx:]
temp_segment = rolling_avg_temp[start_idx:]

# Determining the color and label based on the previous month.
if prev_month in list(range(49, 52)) + list(range(1, 12)):
    color = 'red'
    label = 'NL: Dec-Mar'
elif prev_month in list(range(13, 17)) + list(range(44, 48)):
    color = 'blue'
    label = 'SL: Apr, Oct-Nov'
elif prev_month in list(range(18, 43)):
    color = 'green'
    label = 'LL: May-Oct'

ax.plot(sinr_segment.index, sinr_segment, color=color, label=label, linewidth=5)
ax2.plot(temp_segment.index, temp_segment, color="gray")

# Creating a Tkinter canvas for the Matplotlib figure.
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Starting the Tkinter main loop to display the graph.
root.mainloop()