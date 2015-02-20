keys = ['jnoarea0','jnoarea5','j0','j5','jvoro','jvt7']
labels = ['inclusive','$|CVF|>0.5$','area correction','$|CVF|>0.5$ + area correction',r'Voronoi ($p_T>\rho\cdot A$)',
          'area correction + $|JVT|>0.7$']

mu = 'mu20'

import json
from numpy import array,vectorize
ntrue = array(json.load(open('../output/ntrue_'+mu+'.json')))
nreco = json.load(open('../output/nreco_'+mu+'.json'))
nrecotrue = json.load(open('../output/nrecotrue_'+mu+'.json'))
nrecofalse = json.load(open('../output/nrecofalse_'+mu+'.json'))

import matplotlib.pyplot as plt
plt.style.use('atlas')
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')

from math import sqrt
def efferr(k,N):
    return sqrt(k*(1-k/N))/N
vefferr = vectorize(efferr)

ptbins = [25,35,45,55,65,75,85,95]

def ploteff(key,label):
    recotrue = array(nrecotrue[key])
    print key
    print recotrue
    print ntrue
    eff = recotrue/ntrue
    print eff
    err = vefferr(recotrue,ntrue)
    plt.errorbar(ptbins,eff,yerr=err,
                 fmt='o--',label=label)

def plotmistag(key,label):
    recofalse = array(nrecofalse[key])
    reco = nreco[key]
    mistag = recofalse/reco
    err = vefferr(recofalse,reco)
    plt.errorbar(ptbins,mistag,yerr=err,
                 fmt='o--',label=label)

for k,l in zip(keys,labels):
    ploteff(k,l)
plt.ylabel('Efficiency')
plt.xlabel('jet $p_T$ [GeV]')
plt.legend(frameon=False,numpoints=1,loc="lower right")
plt.ylim([0.9,1.01])
plt.savefig('../plots/efficiencies_'+mu+'.png')
plt.close()

for k,l in zip(keys,labels):
    plotmistag(k,l)
plt.ylabel('Fake rate')
plt.xlabel('jet $p_T$ [GeV]')
plt.ylim([0.,0.6])
plt.legend(frameon=False,numpoints=1,loc="upper right")
plt.savefig('../plots/mistags_'+mu+'.png')
