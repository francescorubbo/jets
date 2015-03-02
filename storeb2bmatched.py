import ROOT as r
from sys import stdout,argv
from math import fabs,pi,sqrt

mu = 'vbf_b2bjvt_jetpt20_trkjetpt5'
from dataset import getsamp
filename = '../data/'+getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree1/tree')
nentries = tree.GetEntries()
#nentries = 200000

hsorpu = 'jishs'
ptcuts = [10,15,20,25,30]

fwdjetpts = []
ctljetpts = {k:[] for k in ptcuts}
ctljetispu = {k:[] for k in ptcuts}
ctljetishs = {k:[] for k in ptcuts}

for jentry in xrange(nentries):

    tree.GetEntry(jentry)

    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    if tree.NPV<5: continue
    if tree.VtxDzTruth>0.1: continue

    fwdjetpt = 0
    fwdjetphi = 0
    for jeta,jphi,jpt,ispuhs in zip(tree.jeta,tree.jphi,tree.jpt,
                                    getattr(tree,hsorpu)):
        if jpt<20:         continue
        if fabs(jeta)<2.5: continue  
        if not ispuhs:     continue
        fwdjetpt = jpt
        fwdjetphi = jphi
        break

    if fwdjetpt==0: continue
    fwdjetpts.append(fwdjetpt)
    
    ctljet = {k:False for k in ptcuts}
    ctlispu = {k:False for k in ptcuts}
    ctlishs = {k:False for k in ptcuts}
    maxdphi = {k:0. for k in ptcuts}
    for jeta,jphi,jpt,ispu,ishs in zip(tree.jeta,tree.jphi,tree.jpt,tree.jispu,tree.jishs):
        if fabs(jeta)>2.4: continue
        for ptcut in ptcuts:
            if jpt<ptcut: continue
            dphi = fabs(jphi-fwdjetphi)
            if dphi>pi: dphi = 2*pi-dphi
            if dphi<2.: continue
            if dphi>maxdphi[ptcut]:
                ctljet[ptcut] = True
                maxdphi[ptcut] = dphi
                ctlispu[ptcut] = ispu
                ctlishs[ptcut] = ishs

    for ptcut in ptcuts:
        if ctljet[ptcut]:
            ctljetpts[ptcut].append(fwdjetpt)
            ctljetispu[ptcut].append(ctlispu[ptcut])
            ctljetishs[ptcut].append(ctlishs[ptcut])

import json
with open('../output/fwdmatched_'+hsorpu+'.json','w') as outfile:
    json.dump(ctljetpts,outfile)
with open('../output/fwdall_'+hsorpu+'.json','w') as outfile:
    json.dump(fwdjetpts,outfile)
with open('../output/ctlispu_'+hsorpu+'.json','w') as outfile:
    json.dump(ctljetispu,outfile)
with open('../output/ctlishs_'+hsorpu+'.json','w') as outfile:
    json.dump(ctljetishs,outfile)
