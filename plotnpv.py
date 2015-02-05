from numpy import load,mean,std,array,median

pltdir = '../plots/'

ptbin = 'pt2030'
jetr = 'j'
mu = 'mu140'

jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5']
labels = ['inclusive','$CVF>0.5$','area correction','$CVF>0.5$ + area correction']

keys = [35,45,55,65]

def getmeans(jet='j0',var='res'):
    resdict = load('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.npy')
    resdict = resdict[()]
    y = [mean(resdict[k]) for k in keys]
    x = [k-5 for k in keys]
    return x,y

def getstds(jet='j0',var='res'):
    resdict = load('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.npy')
    resdict = resdict[()]
    y = [std(resdict[k]) for k in keys]
    x = [k-5 for k in keys]
    return x,y
    
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)


def plotvar(var):

    varlabel = {'res':(r'$<p_T^{reco}-p_T^{true}>$ [GeV]',r'$\sigma(p_T^{reco}-p_T^{true})$ [GeV]'),
                'mass':(r'$<jet~fmass>$ [GeV]',r'$\sigma(jet~mass)$ [GeV]'),
                'width':(r'$<jet~width>$',r'$\sigma(jet~width)$')
                }

    for jt,l in zip(jettypes,labels):
        x,y = getmeans(jt,var)
        jetplot = plt.plot(x,y,marker='o',linestyle='--',label=l)

#plt.ylim([-10,0])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][0])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvmean'+'_'+ptbin+'_'+mu+'.png')
    plt.close()

    for jt,l in zip(jettypes,labels):
        x,y = getstds(jt)
        jetplot = plt.plot(x,y,marker='o',linestyle='--',label=l)

#plt.ylim([0,10])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][1])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvstd_'+ptbin+'_'+mu+'.png')
    plt.close()

for var in ['res','mass','width']:
    plotvar(var)
