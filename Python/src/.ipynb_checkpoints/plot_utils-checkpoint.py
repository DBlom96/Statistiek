import matplotlib.pyplot as plt
import numpy as np

# Vaste kleurconstanten voor een consistente huisstijl
PRIMARY_COLOR = '#1f77b4'
SECONDARY_COLOR = '#ff7f0e'
ACCENT_COLOR = '#2ca02c'
GRID_COLOR = '#cccccc'

def setup_plot_style():
    """Stelt de globale Matplotlib-stijl in voor alle notebooks."""
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 11
    plt.rcParams['axes.labelsize'] = 12
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['figure.figsize'] = (8, 5)
    plt.rcParams['figure.dpi'] = 100

def create_histogram(data, title="Histogram", xlabel="Waarde", ylabel="Frequentie"):
    """
    Genereert een gestandaardiseerd histogram op basis van ingevoerde data.
    
    Parameters:
    - data: array-like (numpy array of list) met numerieke data
    - title: string, titel van de grafiek
    - xlabel: string, label voor de x-as
    - ylabel: string, label voor de y-as
    
    Returns:
    - fig: matplotlib.figure.Figure object
    """
    fig, ax = plt.subplots()
    
    ax.hist(data, bins=15, color=PRIMARY_COLOR, edgecolor='black', alpha=0.85)
    
    ax.set_title(title, fontweight='bold')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    
    ax.grid(True, linestyle='--', alpha=0.6, color=GRID_COLOR)
    
    plt.tight_layout()
    return fig