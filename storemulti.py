import ROOT as r
from sys import stdout,argv
from math import fabs

jet = argv[1]

ptmin = 20
ptmax = 30
ptbin = 'pt%d%d'%(ptmin,ptmax)

mu = 'mu20'
from dataset import getsamp
filename = '../data/'+getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()

cuts = [10,15,20,25,30,35,40,45]
clperjetdict = {c:[] for c in cuts}
jetperevtdict = {c:[] for c in cuts}

from jetutils import Calibration,NPVCorrection
calib = Calibration(jet,mu)
npvcorr = NPVCorrection(jet,mu)

for jentry in xrange(nentries):
    tree.GetEntry(jentry)

    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()
    
    jpts = getattr(tree,'%spt'%jet)
    jetas = getattr(tree,'%seta'%jet)
    ncls = getattr(tree,'%sncl'%jet)

    njets = 0
    clperjet = []

    npv = tree.NPVtruth

    for ncl,jpt,jeta in zip(ncls,jpts,jetas):
        if fabs(jeta)>1.0: continue
        calibpt = npvcorr.getpt(jpt,npv)
        calibpt = calib.getpt(calibpt)
        if calibpt<ptmin: continue
        if calibpt>ptmax: continue
        njets+=1
        clperjet.append(ncl)
    
    if njets<1 : continue
    
    for cut in cuts:
        if npv<cut:
            clperjetdict[cut] += clperjet
            jetperevtdict[cut].append(njets)
            break

import json
with open('../output/clperjetvsnpv_'+jet+'_'+ptbin+'_'+mu+'.json','w') as outfile:
    json.dump(clperjetdict,outfile)
with open('../output/jetperevtvsnpv_'+jet+'_'+ptbin+'_'+mu+'.json','w') as outfile:
    json.dump(jetperevtdict,outfile)
