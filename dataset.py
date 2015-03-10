
def getsamp(mu='mu20'):
    sampdict = {
        'mu140':'mc12_14TeV_Pythia8_J2_ITK_140_140.root',
        'mu20':'PythJ1and2mc12aJETMET_short.root',
        'mu20_b2bjvt_jetpt20_trkjetpt5':'PythJ1and2mc12aJETMET_short_b2bjvt_jetpt20_trkjetpt5.root',
        'vbf_b2bjvt_jetpt20_trkjetpt5':'VBFH125_ZZ4lep_jetpt20_trkjetpt5.root',
        'vbf_b2bjvt_jetpt10_trkjetpt2':'VBFH125_ZZ4lep_jetpt10_trkjetpt2.root',
        'vbf_b2bjvt_scan':'VBFH125_ZZ4lep_scanmatchingeff.root'
#        'mu20_clpt2':'PythiaJ2mc12aJETMET_clpt2.root',
        }
    return sampdict[mu]
