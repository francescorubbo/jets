import ROOT as r
from sys import stdout
filename = '../data/PythJXmc12aJETMETshort.root'

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()

nreco = {'j0':0,'j5':0}
ntrue = 0
nrecotrue = {'j0':0,'j5':0}
nrecofalse = {'j0':0,'j5':0}
nentries = tree.GetEntries()
for jentry in xrange(nentries):
    tree.GetEntry(jentry)

    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    for jeta,jpt,tjpt in zip(tree.j0eta,tree.j0pt,tree.tj0pt):
        if jeta>2.5: continue
        if jpt<20: continue
        if jpt>30: continue

        nreco['j0'] += 1
        if tjpt>0.:
            nrecotrue['j0'] += 1
        if tjpt<0.:
            nrecofalse['j0'] += 1

    for jeta,jpt,tjpt in zip(tree.j5eta,tree.j5pt,tree.tj5pt):
        if jeta>2.5: continue
        if jpt<20: continue
        if jpt>30: continue

        nreco['j5'] += 1
        if tjpt>20. and tjpt<30:
            nrecotrue['j5'] += 1
        elif tjpt<0.:
            nrecofalse['j5'] += 1
 
    for tpt in tree.truejetpt:
        if tpt<20: continue
        if tpt>30: continue
        ntrue += 1
print

print nreco, nrecotrue, nrecofalse

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

from math import sqrt
def efferr(k,N):
    return sqrt(k*(1-float(k)/N))/N

effarea = float(nrecotrue['j0'])/nreco['j0']
effareaerr = efferr(nrecotrue['j0'],nreco['j0'])
mistagarea = float(nrecofalse['j0'])/nreco['j0']
mistagareaerr = efferr(nrecofalse['j0'],nreco['j0'])

print effarea,mistagarea

plt.errorbar(effarea,mistagarea,xerr=effareaerr,yerr=mistagareaerr,
             fmt='o',label='area subtraction')

effjvf = float(nrecotrue['j5'])/nreco['j5']
effjvferr = efferr(nrecotrue['j5'],nreco['j5'])
mistagjvf = float(nrecofalse['j5'])/nreco['j5']
mistagjvferr = efferr(nrecofalse['j5'],nreco['j5'])
plt.errorbar(effjvf,mistagjvf,xerr=effjvferr,yerr=mistagjvferr,
             fmt='o',label='cluster JVF + area subtraction')

print effjvf,mistagjvf
plt.legend(frameon=False,numpoints=1)
plt.savefig('../plots/efficiencies')
