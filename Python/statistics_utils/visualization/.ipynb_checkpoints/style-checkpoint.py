# visualization/style.py

PRIMARY_PLOT_COLOR = "C0" # tab:blue
SECONDARY_PLOT_COLOR = "C8" # tab:olive
TERTIARY_PLOT_COLOR = "C1" # tab:orange

ACCEPTABLE_COLOR = "C2" # tab:green
CRITICAL_COLOR = "C3" # tab:red

# Transparency of shaded areas
OPACITY = 0.3

def get_y_annotation(ax):
    ymin, ymax = ax.get_ylim()
    offset = 0.05 * (ymax - ymin)
    return ymin - offset, offset