import ROOT as r
from sys import stdout,argv
from math import fabs

mu = 'voronoi_cvf'
from dataset import getsamp
filename = '/atlas/output/rubbo/'+getsamp(mu)

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 20000

jet = argv[1]

responses = []
truepts = []
recopts = []

from jetutils import NPVCorrection
npvcorr = NPVCorrection(jet,mu)

for jentry in xrange(nentries):
    tree.GetEntry(jentry)
    
    if not jentry%1000:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    jpts = getattr(tree,'%spt'%jet)
    tjpts = getattr(tree,'t%spt'%jet)
    tjetas = getattr(tree,'t%seta'%jet)
    npv = tree.NPVtruth

    resjet = []
    truept = []
    recopt = []
    for jpt,tjpt,tjeta in zip(jpts,tjpts,tjetas):
        if fabs(tjeta)>1.0: continue
        if tjpt<20: continue
        corrpt = npvcorr.getpt(jpt,npv)
        resjet.append(corrpt/tjpt)
        truept.append(tjpt)
        recopt.append(corrpt)

    responses += resjet
    truepts += truept
    recopts += recopt

print

from numpy import save
save('../output/responses_'+jet+'_'+mu,responses)
save('../output/truepts_'+jet+'_'+mu,truepts)
save('../output/recopts_'+jet+'_'+mu,recopts)
