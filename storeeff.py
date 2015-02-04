import ROOT as r
from sys import stdout
from math import fabs

mu = 'mu20'

samp = {'mu140':'mc12_14TeV_Pythia8_J2_ITK_140_140.root',
        'mu20':'PythiaJ2mc12aJETMET.root'}

filename = '../data/'+samp[mu]

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 50000

keys = ['j0','j5','jnoarea0','jnoarea5']

ntrue = []
nreco      = {k: [] for k in keys}
nrecotrue  = {k: [] for k in keys}
nrecofalse  = {k: [] for k in keys}

for jentry in xrange(nentries):
    tree.GetEntry(jentry)

    if not jentry%1000:
        stdout.write('\r%d/%d'%(jentry,nentries))
        stdout.flush()

    for k in keys:
        for jeta,jpt,tjpt,tjeta in zip(getattr(tree,'%seta'%k),getattr(tree,'%spt'%k),getattr(tree,'t%spt'%k),getattr(tree,'t%seta'%k)):
            if fabs(tjeta)<1.0:
                nrecotrue[k].append(tjpt)
            if fabs(jeta)>1.0: continue
            nrecofalse[k].append(tjpt)
            nreco[k].append(jpt)

    for tpt,teta in zip(tree.truejetpt,tree.truejeteta):
        if fabs(teta)>1.0: continue
        ntrue.append(tpt)
print

from numpy import histogram, histogram2d

binedges = [-10,10,20,30,40,50,60,70,80,90,100]
bintrue = histogram(ntrue,binedges)[0][2::].tolist()
binrecotrue = {}
binrecofalse = {}
binreco = {}

for k in keys:
    binreco[k] = histogram(nreco[k],binedges)[0][2::].tolist()
    
    recovstrue = histogram2d(nrecofalse[k],nreco[k],binedges)[0]
    binrecofalse[k] = recovstrue[0][2::].tolist()

    binrecotrue[k] = [float(x) for x in histogram(nrecotrue[k],binedges)[0][2::]]
    binrecotrue[k] = [rt if rt<t else t for t,rt in zip(bintrue,binrecotrue[k])]

import json
with open('../output/ntrue_'+mu+'.json','w') as outfile:
    json.dump(bintrue,outfile)
with open('../output/nreco_'+mu+'.json','w') as outfile:
    json.dump(binreco,outfile)
with open('../output/nrecofalse_'+mu+'.json','w') as outfile:
    json.dump(binrecofalse,outfile)
with open('../output/nrecotrue_'+mu+'.json','w') as outfile:
    json.dump(binrecotrue,outfile)

