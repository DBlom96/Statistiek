import numpy as np
import matplotlib.pyplot as plt

class KansverdelingPlotter:
    def __init__(self, title="Kansverdeling", xlabel="x", ylabel="Probability", num_xsteps=1_000):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.num_xsteps = num_xsteps
        self.fig, self.ax = plt.subplots()
    
    def set_title(self, title):
        """Voeg een titel toe aan de plot."""
        self.title = title
        self.ax.set_title(title)
    
    def add_labels(self, xlabel, ylabel):
        """Voeg labels toe aan de x- en y-assen."""
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.ax.set_xlabel(xlabel, loc='right')
        self.ax.set_ylabel(ylabel)
    
    def add_legend(self):
        """Voeg een legenda toe aan de plot."""
        self.ax.legend()
    
    def add_text(self, x, y, text, color="red"):
        """Voeg tekst toe aan de plot."""
        self.ax.text(x, y, text, ha='center', va='center', color=color)
    
    def add_vertical_line(self, xval, yval=None, text=None, color="red", linestyle="--", pos=0.1, **kwargs):
        """Voeg een verticale lijn x=xval toe aan de plot.
           Optioneel: voeg tekst toe op lijn op fractie pos van de lijn."""
        assert self.x[0] <= xval <= self.x[-1]
        
        if yval == None:
            yval = self.dist.pdf(xval, **self.params)
            
        if text:
            ext = 0.05
            self.ax.plot([xval, xval], [0, (pos-ext)*yval], color=color, linestyle=linestyle, **kwargs)
            self.ax.plot([xval, xval], [yval, (pos+ext)*yval], color=color, linestyle=linestyle,**kwargs)
            self.add_text(x=xval, y=pos*yval, text=text, color=color)
        else:
            self.ax.plot([xval, xval], [0, yval], color=color, linestyle=linestyle, **kwargs)
        
    def show(self):
        """Toon de grafiek."""
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        plt.show()
    
    def save_figure(self, filename, fmt='png'):
        """Sla de figuur op als een bestand."""
        self.fig.savefig(f"../output/{self.dist_type}/{filename}.{fmt}", format=fmt)
        print(f"Figuur opgeslagen als {filename}.{fmt}")