import matplotlib.pyplot as plt
from kansverdelingen import BinomialeVerdelingPlotter, PoissonVerdelingPlotter
from kansverdelingen import NormaleVerdelingPlotter, ExponentieleVerdelingPlotter, TVerdelingPlotter, ChikwadraatVerdelingPlotter

# Terug naar default instellingen en laad de custom stylesheet
plt.rcParams.update(plt.rcParamsDefault)
# plt.style.use('../styles/stylesheet.mplstyle')

# Voorbeeld gebruik van de Binomiale verdeling met highlight
binom_plotter = BinomialeVerdelingPlotter(n=10, p=0.5)
binom_plotter.plot_pmf(left=0, right=3)
binom_plotter.show()
binom_plotter.save_figure("binom", "pdf")

# Voorbeeld gebruik van de Normale verdeling met highlight
norm_plotter = NormaleVerdelingPlotter(mu=0, sigma=1)
norm_plotter.plot_pdf()
norm_plotter.highlight_interval(a=-1, b=1)
norm_plotter.show()
norm_plotter.save_figure("norm", "pdf")

# Voorbeeld gebruik van de Poisson verdeling met highlight
poisson_plotter = PoissonVerdelingPlotter(mu=3)
poisson_plotter.plot_pmf()
poisson_plotter.highlight_interval(a=2, b=6)
poisson_plotter.show()
poisson_plotter.save_figure("poisson", "pdf")

# Voorbeeld gebruik van de Exponentiële verdeling met highlight
exp_plotter = ExponentieleVerdelingPlotter(lam=1.5)
exp_plotter.plot_pdf()
exp_plotter.highlight_interval(a=1, b=5)
exp_plotter.show()
exp_plotter.save_figure("expon", "pdf")

# Voorbeeld gebruik van de t-verdeling met highlight
t_plotter = TVerdelingPlotter(df=7)
t_plotter.plot_pdf()
t_plotter.highlight_interval(a=1, b=5)
t_plotter.show()
t_plotter.save_figure("t", "pdf")

# Voorbeeld gebruik van de Exponentiële verdeling met highlight
chi2_plotter = ChikwadraatVerdelingPlotter(df=12)
chi2_plotter.plot_pdf()
chi2_plotter.highlight_interval(a=1, b=5)
chi2_plotter.show()
chi2_plotter.save_figure("chi2", "pdf")