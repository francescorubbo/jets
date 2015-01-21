import ROOT as r
from sys import stdout
filename = '../data/PythJXmc12aJETMETshort.root'

ff = r.TFile(filename)
tree = ff.Get('tree1/tree')
nentries = tree.GetEntries()

nhs = 0
npu = 0
from numpy import arange,concatenate
cuts = concatenate([arange(0,1,0.1),arange(0.91,1,0.01)])
cutkeys = ['%1.2f'%cut for cut in cuts]
nhsjvt = dict(zip(cutkeys,[0]*len(cuts)))
npujvt = dict(zip(cutkeys,[0]*len(cuts)))

#for jentry in xrange(nentries):
for jentry in xrange(10000):
    
    tree.GetEntry(jentry)

    if not jentry%10:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    for jpt,jeta,tjpt,jvt in zip(tree.jpt,tree.jeta,tree.tjpt,tree.jb2bjvt):
        if jeta<2.5: continue
        if jpt<40.: continue
        if jpt>50.: continue

        if tjpt>0.:
            nhs += 1
            for cut in cuts:
                if jvt>cut or jvt<0:
                    nhsjvt['%1.2f'%cut] += 1
        else:
            npu += 1
            for cut in cuts:
                if jvt>cut or jvt<0:
                    npujvt['%1.2f'%cut] += 1
        

from math import sqrt
def efferr(k,N):
    return sqrt(k*(1-float(k)/N))/N

efficiency = [float(nhsjvt[cut])/nhs for cut in cutkeys]
efficiencyerr = [efferr(nhsjvt[cut],nhs) for cut in cutkeys]
mistag = [float(npujvt[cut])/npu for cut in cutkeys]
mistagerr = [efferr(npujvt[cut],nhs) for cut in cutkeys]

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

plt.errorbar(efficiency,mistag,xerr=efficiencyerr,yerr=mistagerr,fmt='o--')
plt.xlabel('Efficiency')
plt.ylabel('Fake Rate')

plt.savefig('../plots/b2bjvt_pt4050.png')

