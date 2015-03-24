from numpy import mean,std,array
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
#plt.style.use('atlas')

import json

pltdir = '../plots/'

jetr = 'jvoro'
mu = 'sigma_rho_study'

#jettypes = [jetr+'noarea0',jetr+'noarea5',jetr+'0',jetr+'5',jetr+'voro']
#labels = ['inclusive','$CVF>0.5$','area correction','$CVF>0.5$ + area correction',
#          r'Voronoi ($p_T>\rho\cdot A$)']

jettypes = [jetr+'0',jetr+'1',jetr+'2',jetr+'3',jetr+'4','j0','jnoarea0']
labels = [r'Voronoi ($p_T>\rho\cdot A$)',r'Voronoi ($p_T>\rho\cdot A+\sigma_\rho\cdot\sqrt{A}$)',r'Voronoi ($p_T>\rho\cdot A+2\sigma_\rho\cdot\sqrt{A}$)',    r'Voronoi ($p_T>\rho\cdot A+3\sigma_\rho\cdot\sqrt{A}$)',r'Voronoi ($p_T>\rho\cdot A+4\sigma_\rho\cdot\sqrt{A}$)','area correction','inclusive']

#keys = [35,45,55,65]
keys = [20,25,30,35,40,45]

def getmeans(jet='j0',var='clperjet',ptrange='2030',calibkey='calib'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_pt'+ptrange+'_'+mu+'_'+calibkey+'.json'))
    y = [mean(resdict['%d'%k]) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y

def getstds(jet='j0',var='clperjet',ptrange='2030',calibkey='calib'):
    resdict = json.load(open('../output/'+var+'vsnpv_'+jet+'_pt'+ptrange+'_'+mu+'_'+calibkey+'.json'))
    y = [std(resdict['%d'%k]) for k in keys]
    x = [k-2.5 for k in keys]
    return x,y
    
def plotvar(var,ptrange,calibkey):

    varlabel = {'clperjet':(r'$<clusters~per~jet>$',r'$\sigma(clusters~per~jet)$'),
                'jetperevt':(r'$<jets~per~event>$',r'$\sigma(jets~per~event)$'),
                }

    for jt,l in zip(jettypes,labels):
        x,y = getmeans(jt,var,ptrange,calibkey)
        plt.figure(0)
        jetplot = plt.plot(x,y,'o--',label=l)

#plt.ylim([-10,0])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][0])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvmean_'+mu+'_'+ptrange+'_'+calibkey+'.png')
    plt.close()

    for jt,l in zip(jettypes,labels):
        x,y = getstds(jt,var,ptrange,calibkey)
        plt.figure(0)
        jetplot = plt.plot(x,y,marker='o',linestyle='--',label=l)

#plt.ylim([0,10])
    plt.xlim([min(keys)-5,max(keys)+5])
    plt.xlabel(r'NPV')
    plt.ylabel(varlabel[var][1])
    plt.legend(loc='upper left',frameon=False,numpoints=1)
    plt.savefig(pltdir+jetr+var+'vsnpvstd_'+mu+'_'+ptrange+'_'+calibkey+'.png')
    plt.close()

ptrange='2030'
calibkey='calib'
for var in ['clperjet',
            'jetperevt'
            ]:
    plotvar(var,ptrange,calibkey)
