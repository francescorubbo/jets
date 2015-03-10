from numpy import load,mean,linspace,polyfit,poly1d
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
#plt.style.use('atlas')

from scipy.stats import norm

pltdir = '../plots/'

ptbin = 'pt201000'
jetr = 'j'
mu = 'mu20'

jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5',jetr+'voro']
labels = ['inclusive','$CVF>0.5$','area correction','$CVF>0.5$ + area correction',
          r'Voronoi ($p_T>\rho\cdot A$)']

#keys = [35,45,55,65]
keys = [15,20,25,30,35,40,45]

import json

def getmeans(jet='j0',var='res'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.json'))
    y = [mean(resdict['%d'%k]) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y
    
def plotvar(var):

    varlabel = {'res':(r'$<p_T^{reco}-p_T^{true}>$ [GeV]',r'$\sigma(p_T^{reco}-p_T^{true})$ [GeV]'),
                }

    npvcorrs = {}
    for jt,l in zip(jettypes,labels):
        x,y = getmeans(jt,var)
        fitpar = polyfit(x, y, 1)
        func = poly1d(fitpar)
        plt.figure(0)
        jetplot = plt.plot(x,y,'o',label=l)
        xp = linspace(10,45)
        plt.plot(xp,func(xp),'-',color=jetplot[0].get_color())
        npvcorrs[jt] = fitpar.tolist()

    with open('../output/npvcorrection_'+mu+'.json','w') as outfile:
        json.dump(npvcorrs,outfile)

#plt.ylim([-10,0])
    plt.xlim([min(keys)-5,max(keys)])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][0])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvmean'+'_'+ptbin+'_'+mu+'.png')
    plt.close()

plotvar('res')
