import ROOT as r
from sys import stdout
from math import fabs

mu = 'sigma_rho_study'
from dataset import getsamp
filename = '../data/'+getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 50000

jetr='jvoro'
keys = [jetr+'0',jetr+'1',jetr+'2',jetr+'3',jetr+'4','j0','jnoarea0']

jvtcut = {'jvt2':0.2,'jvt4':0.4,'jvt7':0.7}

ntrue = []
nreco      = {k: [] for k in keys}
nrecotrue  = {k: [] for k in keys}
nrecofalse  = {k: [] for k in keys}

from jetutils import Calibration,NPVCorrection
calibdict = {key: Calibration(key,mu) for key in keys if 'jvt' not in key}
npvcorrdict = {key: NPVCorrection(key,mu) for key in keys if 'jvt' not in key}

for jentry in xrange(nentries):
    tree.GetEntry(jentry)

    if not jentry%1000:
        stdout.write('\r%d/%d'%(jentry,nentries))
        stdout.flush()

    npv = tree.NPVtruth

    for k in keys:
        jetname = k
        dojvt = 'jvt' in jetname
        if dojvt: jetname = 'j0'
        for ijet,(jeta,jpt,tjpt,tjeta) in enumerate(
            zip(getattr(tree,'%seta'%jetname),getattr(tree,'%spt'%jetname),getattr(tree,'t%spt'%jetname),getattr(tree,'t%seta'%jetname))):
            if dojvt:
                if tree.j0jvt[ijet]>0. and tree.j0jvt[ijet]<jvtcut[k]:
                    continue

            if fabs(tjeta)<1.0:
                nrecotrue[k].append(tjpt)
            if fabs(jeta)>1.0: continue
            nrecofalse[k].append(tjpt)
            calibpt = jpt
            if not dojvt:
                calibpt = npvcorrdict[k].getpt(calibpt,npv)
                calibpt = calibdict[k].getpt(calibpt)
            nreco[k].append(calibpt)

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

import json
with open('../output/ntrue_'+mu+'.json','w') as outfile:
    json.dump(bintrue,outfile)
with open('../output/nreco_'+mu+'.json','w') as outfile:
    json.dump(binreco,outfile)
with open('../output/nrecofalse_'+mu+'.json','w') as outfile:
    json.dump(binrecofalse,outfile)
with open('../output/nrecotrue_'+mu+'.json','w') as outfile:
    json.dump(binrecotrue,outfile)

