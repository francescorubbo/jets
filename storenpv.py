import ROOT as r
from sys import stdout
filename = '../data/mc12_14TeV_Pythia8_J2_ITK_140_140.root'

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
#nentries = 1000

cuts = [35,45,55,65]
resdict = {c:[] for c in cuts}
massdict = {c:[] for c in cuts}
widthdict = {c:[] for c in cuts}

ptmin = 20
ptmax = 30
ptbin = 'pt%d%d'%(ptmin,ptmax)

jet = 'j0'

for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    jpts = getattr(tree,'%spt'%jet)
    tjpts = getattr(tree,'t%spt'%jet)
    jms = getattr(tree,'%smass'%jet)
    jws = getattr(tree,'%swidth'%jet)

    resjets = []
    massjets = []
    widthjets = []
    for jpt,tjpt,jm,jw in zip(jpts,tjpts,jms,jws):
        if tjpt<ptmin or tjpt>ptmax: continue
        resjets.append(jpt-tjpt)
        massjets.append(jm)
        widthjets.append(jw)
            

    npv = tree.NPV

    for cut in cuts:
        if npv<cut:
            resdict[cut] += resjets
            massdict[cut] += massjets
            widthdict[cut] += massjets
            break


from numpy import save
save('../output/resvsnpv_'+jet+'_'+ptbin,resdict)
save('../output/massvsnpv_'+jet+'_'+ptbin,massdict)
save('../output/widthvsnpv_'+jet+'_'+ptbin,widthdict)
