from numpy import mean,std,array
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')

import json

pltdir = '../plots/'

ptbin = 'pt201000'
jetr = 'j'
mu = 'mu20'

jettypes = [jetr+'noarea0',
#            jetr+'noarea5',
            jetr+'0',
#            jetr+'5',
            jetr+'voro'
            ]
labels = ['inclusive',
#          '$CVF>0.5$',
          'area correction',
#          '$CVF>0.5$ + area correction',
          r'Voronoi ($p_T>\rho\cdot A + \sigma_{\rho}\cdot A$)'
          ]
colors = ['b',
#          'g',
          'r',
#          'c',
          'm'
          ]

#keys = [35,45,55,65]
keys = [20,25,30,35,40,45]

def getmeans(jet='j0',var='clperjet'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.json'))
    y = [mean(resdict['%d'%k]) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y

def getstds(jet='j0',var='clperjet'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_'+ptbin+'_'+mu+'.json'))
    y = [std(resdict['%d'%k]) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y
    
def plotvar(var):

    varlabel = {'clperjet':(r'$<clusters~per~jet>$',r'$\sigma(clusters~per~jet)$'),
                'jetperevt':(r'$<jets~per~event>$',r'$\sigma(jets~per~event)$'),
                }

    for jt,l,c in zip(jettypes,labels,colors):
        x,y = getmeans(jt,var)
        plt.figure(0)
        jetplot = plt.plot(x,y,'o--',label=l,color=c)

#plt.ylim([-10,0])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][0])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvmean_'+ptbin+'_'+mu+'.png')
    plt.close()

    for jt,l,c in zip(jettypes,labels,colors):
        x,y = getstds(jt,var)
        plt.figure(0)
        jetplot = plt.plot(x,y,marker='o',linestyle='--',label=l,color=c)

#plt.ylim([0,10])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][1])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvstd_'+ptbin+'_'+mu+'.png')
    plt.close()

for var in ['clperjet',
            'jetperevt'
            ]:
    plotvar(var)
