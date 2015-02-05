import ROOT as r
from sys import stdout,argv

from math import fabs
mu = 'mu140'
samp = {'mu140':'mc12_14TeV_Pythia8_J2_ITK_140_140.root',
        'mu20':'PythiaJ2mc12aJETMET.root'}
filename = '../data/'+samp[mu]

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 200000

cuts = [35,45,55,65]
#cuts = [10,15,20,25]
resdict = {c:[] for c in cuts}
massdict = {c:[] for c in cuts}
widthdict = {c:[] for c in cuts}

ptmin = 20
ptmax = 30
ptbin = 'pt%d%d'%(ptmin,ptmax)

jet = argv[1]

for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    jpts = getattr(tree,'%spt'%jet)
    tjpts = getattr(tree,'t%spt'%jet)
    tjetas = getattr(tree,'%seta'%jet) #HACK! This should be truth jet eta
    jms = getattr(tree,'%smass'%jet)
    jws = getattr(tree,'%swidth'%jet)

    resjets = []
    massjets = []
    widthjets = []
    for jpt,tjpt,tjeta,jm,jw in zip(jpts,tjpts,tjetas,jms,jws):
        if fabs(tjeta)>1.0: continue
        if tjpt<ptmin or tjpt>ptmax: continue
        resjets.append(jpt-tjpt)
        massjets.append(jm)
        widthjets.append(jw)
            

    npv = tree.NPV

    for cut in cuts:
        if npv<cut:
            resdict[cut] += resjets
            massdict[cut] += massjets
            widthdict[cut] += widthjets
            break


from numpy import save
save('../output/resvsnpv_'+jet+'_'+ptbin+'_'+mu,resdict)
save('../output/massvsnpv_'+jet+'_'+ptbin+'_'+mu,massdict)
save('../output/widthvsnpv_'+jet+'_'+ptbin+'_'+mu,widthdict)
