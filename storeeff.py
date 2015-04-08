import ROOT as r
from sys import stdout
from math import fabs

mu = 'voronoi_cvf'
from dataset import getsamp
filename = getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 50000
#nentries = 1000 

jetr='jvoro'
keys = ['j0','jnoarea0','j0cvf',jetr+'0',jetr+'1',jetr+'10',jetr+'0cvf5',jetr+'0cvfx',jetr+'1cvf5',jetr+'1cvfx',jetr+'s',jetr+'cvf5s',jetr+'cvfxs']

jvtcut = {'jvt2':0.2,'jvt4':0.4,'jvt7':0.7}

isolated_true=True
isolated_reco=True
if isolated_true:
	extra='_isolatedt'
	if isolated_reco:
		extra+='r'
	extra+='jets'
else:
	extra='2'

ntrue = []
nreco_calibpt      = {k: [] for k in keys}
nrecotrue  = {k: [] for k in keys}
nreco_truept  = {k: [] for k in keys}

from jetutils import Calibration,NPVCorrection
calibdict = {key: Calibration(key,mu) for key in keys if 'jvt' not in key}
npvcorrdict = {key: NPVCorrection(key,mu) for key in keys if 'jvt' not in key}

from numpy import histogram, histogram2d
binedges = [-10,10,20,30,40,50,60,70,80,90,100]

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
        for ijet,(jeta,jpt,tjpt,tjeta,tjmindr,jmindr) in enumerate(
            zip(getattr(tree,'%seta'%jetname),getattr(tree,'%spt'%jetname),getattr(tree,'t%spt'%jetname),getattr(tree,'t%seta'%jetname),getattr(tree,'t%smindr'%jetname),getattr(tree,'%smindr'%jetname))):
            if dojvt:
                if tree.j0jvt[ijet]>0. and tree.j0jvt[ijet]<jvtcut[k]:
                    continue
            if fabs(jeta)>1.0: continue
            
	    calibpt = jpt
	    belowzero=0
            if not dojvt:
                calibpt = npvcorrdict[k].getpt(calibpt,npv)
		if calibpt<0:
			belowzero=1	
			print(k)
                calibpt = calibdict[k].getpt(calibpt)
		if belowzero>0:
			calibpt=0	
            nreco_calibpt[k].append(calibpt)
            nreco_truept[k].append(tjpt)

	    if isolated_true:
	    	if tjmindr < 0.8:
			continue
		if isolated_reco:
			if jmindr < 0.8:
				continue

            if fabs(tjeta)<1.0:
                nrecotrue[k].append(tjpt)

    for tpt,teta,tmindr in zip(tree.truejetpt,tree.truejeteta,tree.truejetmindr):
        if fabs(teta)>1.0: continue
	if isolated_true:
		if tmindr < 0.8:
			continue
        ntrue.append(tpt)
print


bintrue = histogram(ntrue,binedges)[0][2::].tolist()
binrecotrue = {}
binrecofalse = {}
binreco = {}

for k in keys:
    binreco[k] = histogram(nreco_calibpt[k],binedges)[0][2::].tolist()
    
    recovstrue = histogram2d(nreco_truept[k],nreco_calibpt[k],binedges)[0]
    binrecofalse[k] = recovstrue[0][2::].tolist()

    binrecotrue[k] = [float(x) for x in histogram(nrecotrue[k],binedges)[0][2::]]

import json
with open('../output/ntrue_'+mu+extra+'.json','w') as outfile:
    json.dump(bintrue,outfile)
with open('../output/nreco_'+mu+extra+'.json','w') as outfile:
    json.dump(binreco,outfile)
with open('../output/nrecofalse_'+mu+extra+'.json','w') as outfile:
    json.dump(binrecofalse,outfile)
with open('../output/nrecotrue_'+mu+extra+'.json','w') as outfile:
    json.dump(binrecotrue,outfile)

