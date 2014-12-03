import ROOT as r
from sys import stdout
#filename = '../data/20141126.07.56_pileup.PythJXmc12aJETMETshort.jetmet2012.root'
filename = '../data/20141202.11.49_pileup.PythJXmc12aJETMETshort.jetmet2012pileupcustom.root'
k = 0.01

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()
nentries = 1000

npvs = []
ncls = []
ntrks = []
jvfs = []
corrjvfs = []
rpts = []
clpts = []

from utils import getassoctrks,computeJVF,computeJVFcorr,computeRpt
import numpy as np
from math import fabs

for jentry in xrange(nentries):
    
    tree.GetEntry(jentry)

    if not jentry%10:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    clpt = np.array(tree.clpt)
    cleta = np.array(tree.cleta)
    trkpt = np.array(tree.trkpt)
    trkispv = np.array(tree.trkispv)

    npv = tree.NPVtruth
    ncl = len(clpt)
    ntrk = len(trkpt)

    clusters = [[ceta,cphi] for ceta,cphi in zip(cleta,tree.clphi)]
    tracks = [[teta,tphi] for teta,tphi in zip(tree.trketa,tree.trkphi)]
    assoctrks = getassoctrks(tracks,clusters)
    trkispv = np.array(tree.trkispv)
    for asstrk,cpt,ceta in zip(assoctrks,clpt,cleta):
        if fabs(ceta)>2.5:continue
        jvfs.append( computeJVF(asstrk,trkpt,trkispv) )
        corrjvfs.append( computeJVFcorr(asstrk,trkpt,trkispv,k) )
        rpts.append( computeRpt(asstrk,trkpt,trkispv,cpt) )

        npvs.append( npv )
        ncls.append( ncl )
        ntrks.append( ntrk )
        clpts.append( cpt )

for name,data in zip(['jvf','corrjvf','rpt','npv','ncl','ntrk','clpt'],
                     [jvfs,corrjvfs,rpts,npvs,ncls,ntrks,clpts]):
    np.save('../outputdr01/'+name,data)
