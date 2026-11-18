# visualization/style.py
def get_y_annotation(ax):
    ymin, ymax = ax.get_ylim()
    offset = 0.05 * (ymax - ymin)
    return ymin - offset, offset

def pretty_print(x, num_decimals=4):
    """Formatteer floats netjes, zonder overbodige nullen."""
    pretty_x = (f"%.{num_decimals}f" % x).rstrip(".")
    return pretty_x