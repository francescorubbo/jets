
def getsamp(mu='mu20'):
    sampdict = {
        'mu140':'mc12_14TeV_Pythia8_J2_ITK_140_140.root',
        'mu20':'PythJ1and2mc12aJETMET_short.root',
        'sigma_rho_study':'20150309.17.35_pileup.PythJ1and2mc12aJETMET_short.jetmet2012pileupcustom.root',
        'voronoi_cvf':'20150330.09.50_pileup.PythJ1and2mc12aJETMET_short.jetmet2012pileupcustom.root',
        }
    return sampdict[mu]
