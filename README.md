<h2> Constraining the delay time distribution of Type-Ia supernovae in galaxy clusters via MCMC modeling </h2>

<p align="justify">
The delay time distribution (DTD) of Type-Ia supernovae (SNe Ia) is the rate of SNe Ia, as a function of time, that explode in a hypothetical stellar population of unit mass formed in a brief burst at time t=0. It is important for understanding chemical evolution, SN Ia progenitors, and SN Ia physics. This python program uses a Markov chain Monte Carlo (MCMC) Bayesian method and the spectral-population synthesis code <a href="http://www2.iap.fr/users/fioc/Pegase/Pegase.3/"  style="text-decoration:none" class="type1">Pégase.3</a> to simultaneously fit the integrated galaxy-light photometry in several bands and the SN Ia numbers discovered in high-redshift clusters to constrain the DTD, allowing extended star formation histories. It has been used in the following article: 
</p>

<p align="justify">
<a href="https://ui.adsabs.harvard.edu/abs/2020arXiv201200793F/abstract"  style="text-decoration:none" class="type1"><b>The delay time distribution of Type-Ia supernovae in galaxy clusters: the impact of extended star-formation histories</b></a> 
<a href="https://ui.adsabs.harvard.edu/link_gateway/2020arXiv201200793F/EPRINT_PDF" style="text-decoration:none" class="type1">[PDF]</a> by Jonathan Freundlich & Dan Maoz
</p>

<p align="justify">
  This article proposes revised fluxes and SN Ia numbers for the cluster sample at <i>z=1.13-1.75</i> studied by <a href="https://ui.adsabs.harvard.edu/abs/2018MNRAS.479.3563F/abstract"  style="text-decoration:none" class="type1">Friedmann & Maoz (2018)</a> and derives a prior on the DTD parameters from the lower-redshift measurements compiled by <a href="https://ui.adsabs.harvard.edu/abs/2017ApJ...848...25M/abstract"  style="text-decoration:none" class="type1">Maoz & Graur (2017)</a>, which are both fed to the MCMC algorithm. The star formation history of each cluster is described by four parameters, and the universal DTD by a two-parameter power-law. 
</p>

<p align="justify">
  The different steps of the calculations can be seen in <a href="./DTD_MCMC.ipynb"  style="color:#FF0000;" class="type1" color="red"><b>DTD_MCMC.ipynb</b></a>. 
</p>
