from numpy import load,mean,std,array,median,sqrt,histogram
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
#plt.style.use('atlas')

from scipy.stats import norm

pltdir = '../plots/'

ptbin = 'pt2030'
jetr = 'jvoro'
mu = 'sigma_rho_study'

#jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5',jetr+'voro']
#labels = ['inclusive','$CVF>0.5$','area correction','$CVF>0.5$ + area correction', r'Voronoi ($p_T>\rho\cdot A$)']
jettypes = [jetr+'0',jetr+'1',jetr+'2',jetr+'3',jetr+'4','j0','jnoarea0']
labels = [r'Voronoi ($p_T>\rho\cdot A$)',r'Voronoi ($p_T>\rho\cdot A+\sigma_\rho\cdot\sqrt{A}$)',r'Voronoi ($p_T>\rho\cdot A+2\sigma_\rho\cdot\sqrt{A}$)',r'Voronoi ($p_T>\rho\cdot A+3\sigma_\rho\cdot\sqrt{A}$)',r'Voronoi ($p_T>\rho\cdot A+4\sigma_\rho\cdot\sqrt{A}$)','Jet $\\rho$-area correction','Inclusive']

keys = [15,20,25,30,35,40,45]
npvlabels=['$<$15','15-20','20-25','25-30','30-35','35-40','40-45']

import json
    
def plotvar(jet='j0',var='res'):

    varlabel = {'res':(r'$p_T^{reco}-p_T^{true}$ [GeV]',r'$\sigma(p_T^{reco}-p_T^{true})$ [GeV]'),
                'mass':(r'$<jet~fmass>$ [GeV]',r'$\sigma(jet~mass)$ [GeV]'),
                'width':(r'$<jet~width>$',r'$\sigma(jet~width)$')
                }

    #histo = makehisto(jt,var)
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.json'))
    for k in range(len(keys)):
    	plt.hist(resdict['%d'%keys[k]],histtype='step',normed=1,bins=50,range=(-20,80),label='NPV: '+npvlabels[k])

    plt.xlabel(varlabel[var][0])
    plt.ylabel('Arbitrary Units')
    plt.title(labels[jettypes.index(jet)])
    plt.legend(loc='upper right',frameon=False,numpoints=1)
    plt.savefig(pltdir+jet+'_'+var+'_distr_npvbins'+'_'+ptbin+'_'+mu+'.png')
    plt.close()


for var in ['res',#'mass',#'width'
            ]:
	for jets in jettypes:
    		plotvar(jet=jets,var=var)
