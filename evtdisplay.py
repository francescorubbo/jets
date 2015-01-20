import ROOT as r
pu='NoPU'
reco = False
#filename = '../data/Pythia'+pu+'_dR01.root'
filename = '../data/defaultcoord/Pythia'+pu+'_dR01_10evts.root'

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')

tree.GetEntry(3)

jeteta = [x for x in tree.truejeteta]
jetphi = [x for x in tree.truejetphi]
jetpt = [x for x in tree.truejetpt]
area = [3.14*0.4*0.4]*len(jetpt)

print jetpt

if reco:
    jeteta = [x for x in tree.j5eta]
    jetphi = [x for x in tree.j5phi]
    jetpt = [x for x in tree.j5pt]

cleta = [x for x in tree.cleta]
clphi = [x for x in tree.clphi]
cljvf = [x for x in tree.cljvfcorr]

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
pltdir = '../plots/'
pltdir+='dr01'

from plotutils import circles
jets = circles(jeteta,jetphi,area,c=jetpt,alpha=0.5)
plt.xlim(-2.5,2.5)
plt.ylim(-3.14,3.14)
plt.colorbar(jets)

cm = plt.cm.hot
clusters = plt.scatter(cleta,clphi,c=cljvf,cmap=cm)
plt.colorbar(clusters)

plt.savefig(pltdir+'evtdisp'+pu+'.png')
