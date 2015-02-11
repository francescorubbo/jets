mu = 'mu20'

from numpy import load
cljvf = load('../output/cljvfs_'+mu+'.npy')
clpt = load('../output/clpts_'+mu+'.npy')
matchedcl = load('../output/matchedcl_'+mu+'.npy')

pltdir = '../plots/'


import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

hshighpt = cljvf[(matchedcl) & (clpt>2.)]
hslowpt = cljvf[(matchedcl) & (clpt<2.)]
puhighpt = cljvf[(matchedcl==False) & (clpt>2.)]
pulowpt = cljvf[(matchedcl==False) & (clpt<2.)]
plt.hist(hshighpt,normed=True,label='matched to HS, $p_T>2$ GeV',alpha=0.5)
plt.hist(hslowpt,normed=True,label='matched to HS, $p_T<2$ GeV',alpha=0.5)
plt.hist(puhighpt,normed=True,label='unmatched to HS, $p_T>2$ GeV',alpha=0.5,histtype='step')
plt.hist(pulowpt,normed=True,label='unmatched to HS, $p_T<2$ GeV',alpha=0.5,histtype='step')
plt.ylim([0.001,100])
plt.yscale('log')
plt.legend()
plt.savefig('testlog.png')
