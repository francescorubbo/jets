import ROOT as r
from sys import stdout,argv
from math import fabs,pi,sqrt

mu = 'vbf_b2bjvt_jetpt20_trkjetpt5'
from dataset import getsamp
filename = '../data/'+getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree1/tree')
nentries = tree.GetEntries()
#nentries = 20000

ctljettype = 'j'
hsorpu = 'jispu'
ptcuts = [10,15,20,25,30]
dphicuts = [0.2,0.4,0.6,0.8,1.5]
asymmcuts = [0.1,0.2,0.3,0.4,1.0]

cuts = ['pt%d_dphi%1.1f_a%1.1f'%(pt,dphi,a) for pt in ptcuts for dphi in dphicuts for a in asymmcuts]

fwdjetpts = []
ctljetfwdpts = {k:[] for k in cuts}
ctljetpts = {k:[] for k in cuts}
ctlfwddphi = {k:[] for k in cuts}
ctljetispu = {k:[] for k in cuts}
ctljetishs = {k:[] for k in cuts}

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
    
    ctljet = {k:False for k in cuts}
    ctljetpt = {k:0. for k in cuts}
    ctlispu = {k:False for k in cuts}
    ctlishs = {k:False for k in cuts}
    maxdphi = {k:99. for k in cuts}
    for jeta,jphi,jpt,ispu,ishs in zip(getattr(tree,ctljettype+'eta'),getattr(tree,ctljettype+'phi'),
                                       getattr(tree,ctljettype+'pt'),getattr(tree,ctljettype+'ispu'),getattr(tree,ctljettype+'ishs')):
        if fabs(jeta)>2.4: continue

        dphi = fabs(jphi-fwdjetphi)
        if dphi>pi: dphi = 2*pi-dphi
        dphi = pi-dphi 
        
        ptasymm = fabs(fwdjetpt-jpt)/(fwdjetpt+jpt)

        for ptcut in ptcuts:
            if jpt<ptcut: continue

            for dphicut in dphicuts:
                if dphi>dphicut: continue

                for asymmcut in asymmcuts:
                    if ptasymm>asymmcut: continue
                    cut = 'pt%d_dphi%1.1f_a%1.1f'%(ptcut,dphicut,asymmcut)
                    if dphi<maxdphi[cut]:
                        ctljet[cut] = True
                        ctljetpt[cut] = jpt
                        maxdphi[cut] = dphi
                        ctlispu[cut] = ispu
                        ctlishs[cut] = ishs

    for cut in cuts:
        if ctljet[cut]:
            ctljetpts[cut].append(ctljetpt[cut])
            ctlfwddphi[cut].append(maxdphi[cut])
            ctljetfwdpts[cut].append(fwdjetpt)
            ctljetispu[cut].append(ctlispu[cut])
            ctljetishs[cut].append(ctlishs[cut])

import json
with open('../output/fwdmatched_'+hsorpu+'.json','w') as outfile:
    json.dump(ctljetfwdpts,outfile)
with open('../output/ctlmatched_'+hsorpu+'.json','w') as outfile:
    json.dump(ctljetpts,outfile)
with open('../output/dphimatched_'+hsorpu+'.json','w') as outfile:
    json.dump(ctlfwddphi,outfile)
with open('../output/fwdall_'+hsorpu+'.json','w') as outfile:
    json.dump(fwdjetpts,outfile)
with open('../output/ctlispu_'+hsorpu+'.json','w') as outfile:
    json.dump(ctljetispu,outfile)
with open('../output/ctlishs_'+hsorpu+'.json','w') as outfile:
    json.dump(ctljetishs,outfile)
