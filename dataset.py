
def getsamp(mu='mu20'):
    sampdict = {
        'mu140':'mc12_14TeV_Pythia8_J2_ITK_140_140.root',
        'mu20':'PythiaJ2mc12aJETMET.root',
        'mu20_clpt2':'PythiaJ2mc12aJETMET_clpt2.root',
        }
    return sampdict[mu]
