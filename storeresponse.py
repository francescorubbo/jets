import ROOT as r
from sys import stdout,argv
from math import fabs

mu = 'mu20_clpt2'
from dataset import getsamp
filename = '../data/'+getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 20000

jet = argv[1]

responses = []
truepts = []
recopts = []

for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    jpts = getattr(tree,'%spt'%jet)
    tjpts = getattr(tree,'t%spt'%jet)
    tjetas = getattr(tree,'t%seta'%jet)

    resjet = []
    truept = []
    recopt = []
    for jpt,tjpt,tjeta in zip(jpts,tjpts,tjetas):
        if fabs(tjeta)>1.0: continue
        if tjpt<20: continue
        if jpt<10: continue
        resjet.append(jpt/tjpt)
        truept.append(tjpt)
        recopt.append(jpt)

    responses += resjet
    truepts += truept
    recopts += recopt

print


from numpy import save
save('../output/responses_'+jet+'_'+mu,responses)
save('../output/truepts_'+jet+'_'+mu,truepts)
save('../output/recopts_'+jet+'_'+mu,recopts)
