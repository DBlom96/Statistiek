import matplotlib.pyplot as plt

# ==========================================
# PRESENTATIE-GEOPTIMALISEERD PALET (OFF-WHITE)
# ==========================================
PRIMARY_PLOT_COLOR = "#2563EB"     # Helder modern blauw (zeer goed zichtbaar)
SECONDARY_PLOT_COLOR = "#64748B"   # Slate grijs voor hulplijnen en gemiddelden
TERTIARY_PLOT_COLOR = "#D97706"    # Warm amber / oranje accent

ACCEPTABLE_COLOR = "#16A34A"       # Krachtig groen (acceptatiegebieden / veilig)
CRITICAL_COLOR = "#DC2626"         # Helder rood (kritieke gebieden / waarschuwingen)
HIGHLIGHT_COLOR = "#0F172A"        # Diep antraciet/zwart voor markeringen en puntschattingen

OPACITY = 0.25                     # Subtiele transparantie voor gearceerde vlakken
LINE_WIDTH = 2.4                   # Stevige, dikke lijnen zodat ze goed zichtbaar zijn vanaf afstand


def apply_plot_style(use_latex_fonts=False):
    """
    Past een oogvriendelijke presentatiestijl toe via rcParams.
    De achtergrond is een zachte, lichte off-white tint (#F8F9FA) i.p.v. felwit,
    gecombineerd met scherpe, donkere typografie voor maximale leesbaarheid in slides.
    """
    style_dict = {
        # Figuur & Resolutie (groot genoeg voor presentaties)
        "figure.figsize": (10, 5.5),
        "figure.dpi": 150,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        
        # Oogvriendelijke, zachte off-white achtergrond (minder fel dan puur wit)
        "figure.facecolor": "#F8F9FA", 
        "axes.facecolor": "#F8F9FA",   

        # Strakke sans-serif typografie voor schermen/slides
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "mathtext.fontset": "dejavusans",
        "font.size": 12, # Iets groter voor betere leesbaarheid in slides
        
        # Donkere, contrastrijke typografie voor optimale zichtbaarheid
        "text.color": "#0F172A",
        "axes.titlesize": 14,
        "axes.titleweight": "bold",
        "axes.titlecolor": "#0F172A",
        
        "axes.labelsize": 12,
        "axes.labelweight": "semibold",
        "axes.labelcolor": "#0F172A",
        
        "xtick.labelsize": 11,
        "ytick.labelsize": 11,
        "xtick.color": "#334155",
        "ytick.color": "#334155",
        
        "legend.fontsize": 11,
        "legend.labelcolor": "#0F172A",

        # Assen & Spines (Strakke, donkere omranding)
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.spines.left": True,
        "axes.spines.bottom": True,
        "axes.edgecolor": "#CBD5E1",   
        "axes.linewidth": 1.5,
        
        # Grid (Subtiel raster dat niet afleidt)
        "axes.grid": True,
        "grid.linestyle": "--",
        "grid.alpha": 0.6,
        "grid.color": "#E2E8F0",

        # Lijnen, Punten & Legenda
        "lines.linewidth": LINE_WIDTH,
        "lines.markersize": 7,
        "legend.frameon": True,
        "legend.framealpha": 0.95,
        "legend.edgecolor": "#CBD5E1",
        "legend.facecolor": "#FFFFFF", # Wit legendavlak steekt mooi af op off-white
    }
    plt.rcParams.update(style_dict)


def style_axis_clean(ax):
    """
    Zorgt voor een strakke indeling van de assen met goed zichtbare ticks.
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(direction="out", length=5, colors="#334155")
    ax.margins(x=0.05, y=0.08)