import numpy as np
def get(name,suffix=''):
    theoutdir = '../output/'
    out = np.load(theoutdir+name+suffix+'.npy')
    return out

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

pltdir = '../plots/'

pusamples = ['mu1','mu40','mu80']
pos = [1,40,80]
dr = '_dr03'

def plotmean(var='',color='b'):
    data = [get(var,'_'+mu+dr) for mu in pusamples]
    datamean = [x.mean() for x in data]

    plot = plt.plot(pos,datamean,color=color,marker='o',linestyle='--')

    return plot[0]

j0res = plotmean('j0res','b')
j1res = plotmean('j1res','g')
j2res = plotmean('j2res','r')
j3res = plotmean('j3res','c')
j4res = plotmean('j4res','m')
j5res = plotmean('j5res','y')
plt.ylim([-30,0])
plt.xlabel(r'$\mu$')
plt.ylabel(r'$<p_T^{reco}-p_T^{true}>$ [GeV]')
plt.legend([j0res,j1res,j2res,j3res,j4res,j5res],
           ['incl.','$corrJVF>0.1$','$corrJVF>0.2$','$corrJVF>0.3$','$corrJVF>0.4$','$corrJVF>0.5$'],
           loc='upper left',frameon=False,numpoints=1)
plt.savefig(pltdir+'jresmean'+dr+'.png')
plt.close()

def plotstd(var='',color='b'):
    data = [get(var,'_'+mu+dr) for mu in pusamples]
    datastd = [x.std() for x in data]

    plot = plt.plot(pos,datastd,color=color,marker='o',linestyle='--')

    return plot[0]

j0res = plotstd('j0res','b')
j1res = plotstd('j1res','g')
j2res = plotstd('j2res','r')
j3res = plotstd('j3res','c')
j4res = plotstd('j4res','m')
j5res = plotstd('j5res','y')
plt.ylim([0,30])
plt.xlabel(r'$\mu$')
plt.ylabel(r'$\sigma(p_T^{reco}-p_T^{true})$ [GeV]')
plt.legend([j0res,j1res,j2res,j3res,j4res,j5res],
           ['incl.','$corrJVF>0.1$','$corrJVF>0.2$','$corrJVF>0.3$','$corrJVF>0.4$','$corrJVF>0.5$'],
           loc='upper left',frameon=False,numpoints=1)
plt.savefig(pltdir+'jresstd'+dr+'.png')
plt.close()

def plothists(var='',varlabel='',varbins=10):
    data = [get(var,'_'+mu+dr) for mu in pusamples]

    [plt.hist(xx,alpha=0.5,label=mu,bins=varbins,histtype='stepfilled') 
     for xx,mu in zip(data,['$\mu=1$','$\mu=40$','$\mu=80$'])]

    plt.xlabel(varlabel)
    plt.legend(loc='upper left',frameon=False)

    plt.savefig(pltdir+var+'hist'+dr+'.png')
    plt.close()

varbins = np.arange(-100,100,20)
varlabel = '$p_T^{reco}-p_T^{true}$ [GeV]'
plothists('j0res',varlabel,varbins)
plothists('j1res',varlabel,varbins)
plothists('j2res',varlabel,varbins)
plothists('j3res',varlabel,varbins)
plothists('j4res',varlabel,varbins)
plothists('j5res',varlabel,varbins)

varbins = np.arange(0,5,1)
varlabel = '$\#~of~jets~/~evt$'
plothists('njet0',varlabel,varbins)
plothists('njet1',varlabel,varbins)
plothists('njet2',varlabel,varbins)
plothists('njet3',varlabel,varbins)
plothists('njet4',varlabel,varbins)
plothists('njet5',varlabel,varbins)
