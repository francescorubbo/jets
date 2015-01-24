import ROOT as r
from sys import stdout
filename = '../data/PythJXmc12aJETMETshort.root'

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()

cuts = [10,20,30,40,50]
resdict = dict(zip(cuts,[[] for c in cuts]))

jet = 'j4'

nentries = tree.GetEntries()
for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%100:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    jpts = getattr(tree,'%spt'%jet)
    tjpts = getattr(tree,'t%spt'%jet)
    resjets = [jpt-tjpt for jpt,tjpt in zip(jpts,tjpts)
            if tjpt>20 and tjpt<30]

    npv = tree.NPVtruth

    for cut in cuts:
        if npv<cut:
            resdict[cut] += resjets
            break


from numpy import save
save('../output/resvsnpv_'+jet,resdict)
