
def getsamp(mu='mu20'):
    sampdict = {
        'mu140':'mc12_14TeV_Pythia8_J2_ITK_140_140.root',
        'mu20':'PythJ1and2mc12aJETMET_short.root',
        'sigma_rho_study':'20150309.17.35_pileup.PythJ1and2mc12aJETMET_short.jetmet2012pileupcustom.root',
        #'voronoi_cvf':'/atlas/output/rubbo/20150330.09.50_pileup.PythJ1and2mc12aJETMET_short.jetmet2012pileupcustom.root',
        'voronoi_cvf':'/atlas/output/acukierm/20150406.11.52_pileup.PythJ1and2mc12aJETMET_short.jetmet2012pileupcustom.root',
	'voronoi_cvf_short':'/ProofAna/run/20150402.14.20_pileup.PythJ1and2mc12aJETMET_short.jetmet2012pileupcustom.root',
        }
    return sampdict[mu]
