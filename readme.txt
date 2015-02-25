Start with data
Run storenpv.py -> Set derivenpvcorr to True, produces resvsnpv_jvoro_pt201000_mu20.json: offsets in NPV bins
Run fitnpv.py -> Derive coefficients of fits of offset vs. NPV
Run storeresponse.py -> Writes arrays of recopt (NPV-corrected), truept, and responses
Run plotresponse.py -> Coefficients of fits of response vs. PT

storeeff.py -> store yields vs. true PT (4 files)
ploteff.py -> plot efficiences vs. PT, fake rate vs. PT
storemulti.py -> clusters per jet, jets per event vs. NPV
plotmulti.py -> plot

storenpv.py with derivenpvcorr to False -> produces plot of offset vs. NPV, SD of offset vs. NPV
