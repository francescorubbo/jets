import ROOT as r
from sys import stdout,argv

mu = 'mu20_b2bjvt_trkjet'
from dataset import getsamp
filename = '../data/'+getsamp(mu)

var = argv[1]

ff = r.TFile(filename)
tree = ff.Get('tree1/tree')
nentries = tree.GetEntries()

ptmin = 20
ptmax = 30
ptbin = 'pt%d%d'%(ptmin,ptmax)

nhs = 0
npu = 0
from numpy import arange,concatenate
cuts = concatenate([arange(0,1,0.1),arange(0.91,1,0.01)])
cutkeys = ['%1.2f'%cut for cut in cuts]
nhsjvt = dict(zip(cutkeys,[0]*len(cuts)))
npujvt = dict(zip(cutkeys,[0]*len(cuts)))

for jentry in xrange(nentries):
    
    tree.GetEntry(jentry)

    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    for jpt,jeta,tjpt,jvt in zip(tree.jpt,tree.jeta,tree.tjpt,getattr(tree,var)):
        if jeta<2.5: continue
        if jpt<ptmin: continue
        if jpt>ptmax: continue

        if tjpt>10.:
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
mistagerr = [efferr(npujvt[cut],npu) for cut in cutkeys]

rocdict = {'efficiency': efficiency,
           'efficiencyerr': efficiencyerr,
           'mistag': mistag,
           'mistagerr': mistagerr,
           }

import json
with open('../output/roc_'+var+'_'+ptbin+'.json','w') as outfile:
    json.dump(rocdict,outfile)
