import ROOT as r
from sys import stdout
from math import fabs

filename = '../data/mc12_14TeV_Pythia8_J2_ITK_140_140.root'

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 50000

keys = ['j0','j5','jnoarea0','jnoarea5']

ntrue = []
nreco      = {k: [] for k in keys}
nrecotrue  = {k: [] for k in keys}

for jentry in xrange(nentries):
    tree.GetEntry(jentry)

    if not jentry%1000:
        stdout.write('\r%d/%d'%(jentry,nentries))
        stdout.flush()

    for k in keys:
        for jeta,jpt,tjpt in zip(getattr(tree,'%seta'%k),getattr(tree,'%spt'%k),getattr(tree,'t%spt'%k)):
            if fabs(jeta)>1.0: continue

            nreco[k].append(jpt)
            nrecotrue[k].append(tjpt)
 
    for tpt,teta in zip(tree.truejetpt,tree.truejeteta):
        if fabs(teta)>1.0: continue
        ntrue.append(tpt)
print


from numpy import histogram, histogram2d

binedges = [-10,0,20,30,40,50,60,70,80,90,100]
bintrue = histogram(ntrue,binedges)[0][2::].tolist()
binrecotrue = {}
binrecofalse = {}
binreco = {}

for k in keys:
    recovstrue = histogram2d(nrecotrue[k],nreco[k],binedges)[0]
    binreco[k] = recovstrue.sum(axis=0)[2::].tolist()
    binrecofalse[k] = recovstrue[0][2::].tolist()
    binrecotrue[k] = recovstrue.diagonal()[2::].tolist()


import json
with open('../output/ntrue.json','w') as outfile:
    json.dump(bintrue,outfile)
with open('../output/nreco.json','w') as outfile:
    json.dump(binreco,outfile)
with open('../output/nrecofalse.json','w') as outfile:
    json.dump(binrecofalse,outfile)
with open('../output/nrecotrue.json','w') as outfile:
    json.dump(binrecotrue,outfile)

