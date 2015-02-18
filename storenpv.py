import ROOT as r
from sys import stdout,argv

from math import fabs
mu = 'mu20'
from dataset import getsamp
filename = '../data/'+getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
#nentries = 200000

#cuts = [35,45,55,65]
cuts = [15,20,25,30,35,40,45]
resdict = {c:[] for c in cuts}
massdict = {c:[] for c in cuts}
widthdict = {c:[] for c in cuts}

ptmin = 20
ptmax = 30
ptbin = 'pt%d%d'%(ptmin,ptmax)

jet = argv[1]

from jetutils import Calibration,NPVCorrection
calib = Calibration(jet,mu)
npvcorr = NPVCorrection(jet,mu)

for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    jpts = getattr(tree,'%spt'%jet)
    tjpts = getattr(tree,'t%spt'%jet)
    tjetas = getattr(tree,'t%seta'%jet)
    jms = getattr(tree,'%smass'%jet)
    jws = getattr(tree,'%swidth'%jet)

    resjets = []
    massjets = []
    widthjets = []
    
    npv = tree.NPVtruth

    for jpt,tjpt,tjeta,jm,jw in zip(jpts,tjpts,tjetas,jms,jws):
        if fabs(tjeta)>1.0: continue
        if tjpt<ptmin or tjpt>ptmax: continue
        calibpt = npvcorr.getpt(jpt,npv)
        calibpt = calib.getpt(calibpt)
#        if calibpt<8: continue
        resjets.append(calibpt-tjpt)
        massjets.append(jm)
        widthjets.append(jw)
            
    for cut in cuts:
        if npv<cut:
            resdict[cut] += resjets
            massdict[cut] += massjets
            widthdict[cut] += widthjets
            break

import json
with open('../output/resvsnpv_'+jet+'_'+ptbin+'_'+mu+'.json','w') as outfile:
    json.dump(resdict,outfile)
with open('../output/massvsnpv_'+jet+'_'+ptbin+'_'+mu+'.json','w') as outfile:
    json.dump(massdict,outfile)
with open('../output/widthvsnpv_'+jet+'_'+ptbin+'_'+mu+'.json','w') as outfile:
    json.dump(widthdict,outfile)
