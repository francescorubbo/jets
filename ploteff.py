keys = ['jnoarea0','jnoarea5','j0','j5']
labels = ['inclusive','$CVF>0.5$','area correction','$CVF>0.5$ + area correction']

import json
from numpy import array,vectorize
ntrue = array(json.load(open('../output/ntrue.json')))
nreco = json.load(open('../output/nreco.json'))
nrecotrue = json.load(open('../output/nrecotrue.json'))
nrecofalse = json.load(open('../output/nrecofalse.json'))

import matplotlib.pyplot as plt
plt.style.use('atlas')
from matplotlib import rc
rc('text', usetex=True)

from math import sqrt
def efferr(k,N):
    return sqrt(k*(1-k/N))/N
vefferr = vectorize(efferr)

ptbins = [25,35,45,55,65,75,85,95]

def ploteff(key,label):
    recotrue = array(nrecotrue[key])
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
plt.ylim([0.1,1.1])
plt.savefig('../plots/efficiencies.png')
plt.close()

for k,l in zip(keys,labels):
    plotmistag(k,l)
plt.ylabel('Fake rate')
plt.xlabel('jet $p_T$ [GeV]')
plt.ylim([0.,1.])
plt.legend(frameon=False,numpoints=1,loc="upper right")
plt.savefig('../plots/mistags.png')
