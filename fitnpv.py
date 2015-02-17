from numpy import load,mean,linspace
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
from scipy.stats import norm

pltdir = '../plots/'

ptbin = 'pt201000'
jetr = 'j'
mu = 'mu20'

jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5',jetr+'voro']
jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5']
labels = ['inclusive','$CVF>0.5$','area correction','$CVF>0.5$ + area correction',
          r'Voronoi ($p_T>\rho\cdot A$)']

#keys = [35,45,55,65]
keys = [20,25,30,35,40]

import json

def getmeans(jet='j0',var='res'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.json'))
    y = [mean(resdict['%d'%k]) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y

from scipy.optimize import curve_fit
def func(x,a,b):
    return a+b*x
    
def plotvar(var):

    varlabel = {'res':(r'$<p_T^{reco}-p_T^{true}>$ [GeV]',r'$\sigma(p_T^{reco}-p_T^{true})$ [GeV]'),
                }

    npvcorrs = {}
    for jt,l in zip(jettypes,labels):
        x,y = getmeans(jt,var)
        popt, pcov = curve_fit(func, x, y)
        print popt
        plt.figure(0)
        jetplot = plt.plot(x,y,'o',label=l)
        xp = linspace(15,40)
        plt.plot(xp,func(xp,*popt),'-')
        npvcorrs[jt] = popt.tolist()

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
