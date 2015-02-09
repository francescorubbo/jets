import ROOT as r
from sys import stdout

mu = 'mu20'
samp = {'mu140':'mc12_14TeV_Pythia8_J2_ITK_140_140.root',
        'mu20':'PythiaJ2mc12aJETMET.root'}
filename = '../data/'+samp[mu]

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 10

cljvfs = []
clpts = []
matchedcl = []
dr2matching = 0.4*0.4

for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    for cleta,clphi,cljvf,clpt in zip(tree.cleta,tree.clphi,
                                      tree.cljvfcorr,tree.clpt):
        if cleta>2.4: continue
        cljvfs.append(cljvf)
        clpts.append(clpt)
        match = False
        for teta,tphi in zip(tree.truejeteta,tree.truejetphi):
            deta = teta-cleta
            dphi = tphi-clphi
            if deta*deta+dphi*dphi<dr2matching:
                match = True
                break
        matchedcl.append(match)

from numpy import save
save('../output/cljvfs_'+mu,   cljvfs)
save('../output/clpts_'+mu,    clpts)
save('../output/matchedcl_'+mu,matchedcl)




