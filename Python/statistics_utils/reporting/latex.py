def pretty_print(x, num_decimals = 4):
    """Formatteer floats netjes, zonder overbodige nullen."""
    pretty_x = (f"%.{num_decimals}f" % x).rstrip(".")
    return pretty_x