import ROOT as r
from numpy import array,absolute
reco = False
showClusters = False
jet = 'j0' if reco else 'truejet'
jvtcut = 0.7

mu = 'mu20'
pu='PU80'
filename = '../data/Pythia'+pu+'_dR01_atCalo.root'
filename = '../data/PythJ1and2mc12aJETMET_short.root'

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')

tree.GetEntry(3758)

jeteta = array([x for x in tree.truejeteta])
jetphi = array([x for x in tree.truejetphi])
jetpt = array([x for x in tree.truejetpt])
area = [3.14*0.4*0.4]*len(jetpt)

if reco:
    jeteta = array([x for x in getattr(tree,'%seta'%jet)])
    jetphi = array([x for x in getattr(tree,'%sphi'%jet)])
    jetpt  = array([x for x in getattr(tree,'%spt'%jet)])
    if jvtcut>0.:
        jvt = array([x if x>0. else -1. for x in tree.j0jvt])
        jeteta = jeteta[absolute(jvt)>jvtcut]
        jetphi = jetphi[absolute(jvt)>jvtcut]
        jetpt = jetpt[absolute(jvt)>jvtcut]
    from jetutils import Calibration,NPVCorrection
    npv = tree.NPVtruth
    calib = Calibration(jet,mu) 
    npvcorr = NPVCorrection(jet,mu) 
    jetpt = array([calib.getpt(npvcorr.getpt(pt,npv)) for pt in jetpt])

jeteta = jeteta[jetpt>20.]
jetphi = jetphi[jetpt>20.]
jetpt =  jetpt[jetpt>20.]

print jetpt

cleta = [x for x in tree.cleta]
clphi = [x for x in tree.clphi]
cljvf = [x for x in tree.cljvfcorr]

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

fig = plt.figure()
ax1 = fig.add_subplot(111)

pltdir = '../plots/'
pltdir+='dr01'

from plotutils import circles
jets = circles(jeteta,jetphi,area,c=jetpt,alpha=0.5
               ,vmin=15.,vmax=150.
               )
plt.xlabel(r'$\eta$')
plt.ylabel(r'$\phi$')
cbjet = fig.colorbar(jets)
cbjet.set_label(r'jet $p_T$ [GeV]')

if showClusters:
    cm = plt.cm.hot
    clusters = ax1.scatter(cleta,clphi,c=cljvf,cmap=cm)
    cbcl = fig.colorbar(clusters)
    cbcl.set_label(r'$CVF$')

plt.xlim(-2.5,2.5)
plt.ylim(-3.14,3.14)
if jvtcut>0. and reco: jet+='jvt%0.1f'%jvtcut
plt.savefig(pltdir+'evtdisp_'+jet+'.png')
