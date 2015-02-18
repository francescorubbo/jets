from numpy import load,mean,std,array,median
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
from scipy.stats import norm

pltdir = '../plots/'

ptbin = 'pt2030'
jetr = 'j'
mu = 'mu20'

jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5',jetr+'voro']
jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5']
labels = ['inclusive','$CVF>0.5$','area correction','$CVF>0.5$ + area correction',
          r'Voronoi ($p_T>\rho\cdot A$)']

#keys = [35,45,55,65]
keys = [20,25,30,35,40]

import json

def fitgaus(data,jet):
    data = array(data)
    plt.figure(1)
    (a,b) = norm.fit(data)
    n,bins,patches = plt.hist(data,normed=True,bins=50)
    y = norm.pdf(bins,a,b)
    plt.plot(bins,y,'r--',linewidth=2)
    plt.xlabel('$p_T^{reco}/p_T^{true}$')
    plt.ylabel('a.u.')
    plt.savefig('../plots/gausfit_resvsnpv%s_'%ptbin+jet+'_'+mu+'.png')
    plt.close()
    print jet
    print std(data)
    print b
    return b

def getmeans(jet='j0',var='res'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.json'))
    y = [mean(resdict['%d'%k]) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y

def getstds(jet='j0',var='res'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.json'))
    y = [std(resdict['%d'%k]) for k in keys]
#    y = [fitgaus(resdict['%d'%k],jet) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y
    
def plotvar(var):

    varlabel = {'res':(r'$<p_T^{reco}-p_T^{true}>$ [GeV]',r'$\sigma(p_T^{reco}-p_T^{true})$ [GeV]'),
                'mass':(r'$<jet~fmass>$ [GeV]',r'$\sigma(jet~mass)$ [GeV]'),
                'width':(r'$<jet~width>$',r'$\sigma(jet~width)$')
                }

    for jt,l in zip(jettypes,labels):
        x,y = getmeans(jt,var)
        plt.figure(0)
        jetplot = plt.plot(x,y,marker='o',linestyle='--',label=l)

#plt.ylim([-10,0])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][0])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvmean'+'_'+ptbin+'_'+mu+'.png')
    plt.close()

    for jt,l in zip(jettypes,labels):
        x,y = getstds(jt,var)
        plt.figure(0)
        jetplot = plt.plot(x,y,marker='o',linestyle='--',label=l)

#plt.ylim([0,10])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][1])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvstd_'+ptbin+'_'+mu+'.png')
    plt.close()

for var in ['res',
            #'mass',
            #'width'
            ]:
    plotvar(var)
