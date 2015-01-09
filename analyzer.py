import ROOT as r
from sys import stdout
#filename = '../data/PythiaNoPU_dR01.root'
#filename = '../data/PythiaPU40_dR03.root'
filename = '../data/PythiaPU80_dR01.root'
suffix = '_mu80_dr01'

ff = r.TFile(filename)
tree = ff.Get('tree0/tree')
nentries = tree.GetEntries()

npvs = []
ncls = []
njets0 = []
njets1 = []
njets2 = []
njets3 = []
njets4 = []
njets5 = []
j0ncls = []
j1ncls = []
j2ncls = []
j3ncls = []
j4ncls = []
j5ncls = []
j0res = []
j1res = []
j2res = []
j3res = []
j4res = []
j5res = []

from numpy import mean,save,array

for jentry in xrange(nentries):
    
    tree.GetEntry(jentry)

    if not jentry%10:
        stdout.write('\r%d'%jentry)
        stdout.flush()

    jetptdict = {}
    for ijet in range(6):
        jpts = []
        tjpts = []
        jncls = []
        for jpt,tjpt,jncl in zip(getattr(tree,'j%dpt'%ijet),getattr(tree,'tj%dpt'%ijet),getattr(tree,'j%dncl'%ijet)):
            if jpt<20: continue
            if jpt>30: continue
            jpts.append(jpt)
            tjpts.append(tjpt)
            jncls.append(jncl)
        jetptdict['j%dpt'%ijet] = array(jpts)
        jetptdict['tj%dpt'%ijet] = array(tjpts)
        jetptdict['j%dncl'%ijet] = array(jncls)
        
    j0pt = jetptdict['j0pt']
    j1pt = jetptdict['j1pt']
    j2pt = jetptdict['j2pt']
    j3pt = jetptdict['j3pt']
    j4pt = jetptdict['j4pt']
    j5pt = jetptdict['j5pt']
    tj0pt = jetptdict['tj0pt']
    tj1pt = jetptdict['tj1pt']
    tj2pt = jetptdict['tj2pt']
    tj3pt = jetptdict['tj3pt']
    tj4pt = jetptdict['tj4pt']
    tj5pt = jetptdict['tj5pt']

    j0res += [jpt-tjpt for jpt,tjpt in zip(j0pt,tj0pt) if tjpt>0]
    j1res += [jpt-tjpt for jpt,tjpt in zip(j1pt,tj1pt) if tjpt>0]
    j2res += [jpt-tjpt for jpt,tjpt in zip(j2pt,tj2pt) if tjpt>0]
    j3res += [jpt-tjpt for jpt,tjpt in zip(j3pt,tj3pt) if tjpt>0]
    j4res += [jpt-tjpt for jpt,tjpt in zip(j4pt,tj4pt) if tjpt>0]
    j5res += [jpt-tjpt for jpt,tjpt in zip(j5pt,tj5pt) if tjpt>0]
    
    npv = tree.NPVtruth
    ncl = len(tree.clpt)
    njet0 = len(j0pt)
    njet1 = len(j1pt)
    njet2 = len(j2pt)
    njet3 = len(j3pt)
    njet4 = len(j4pt)
    njet5 = len(j5pt)
    j0ncl = 0 if njet0==0 else mean(jetptdict['j0ncl'])
    j1ncl = 0 if njet1==0 else mean(jetptdict['j1ncl'])
    j2ncl = 0 if njet2==0 else mean(jetptdict['j2ncl'])
    j3ncl = 0 if njet3==0 else mean(jetptdict['j3ncl'])
    j4ncl = 0 if njet4==0 else mean(jetptdict['j4ncl'])
    j5ncl = 0 if njet5==0 else mean(jetptdict['j5ncl'])

    npvs.append( npv )
    ncls.append( ncl )
    njets0.append( njet0 )
    njets1.append( njet1 )
    njets2.append( njet2 )
    njets3.append( njet3 )
    njets4.append( njet4 )
    njets5.append( njet5 )
    j0ncls.append( j0ncl )
    j1ncls.append( j0ncl )
    j2ncls.append( j0ncl )
    j3ncls.append( j0ncl )
    j4ncls.append( j0ncl )
    j5ncls.append( j0ncl )

for name,data in zip(['npv','ncl',
                      'njet0','njet1','njet2','njet3','njet4','njet5',
                      'j0ncl','j1ncl','j2ncl','j3ncl','j4ncl','j5ncl',
                      'j0res','j1res','j2res','j3res','j4res','j5res'],
                     [npvs,ncls,
                      njets0,njets1,njets2,njets3,njets4,njets5,
                      j0ncls,j1ncls,j2ncls,j3ncls,j4ncls,j5ncls,
                      j0res,j1res,j2res,j3res,j4res,j5res]):
    save('../output/'+name+suffix,data)
