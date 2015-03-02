import matplotlib.pyplot as plt
plt.style.use('atlas')
from matplotlib import rc
rc('text', usetex=True)

ptbin = 'pt3040'

vars = ['jb2bcorrjvf','jb2bcorrjvf_trk2','jb2bcorrjvf_trk4']

labeldict = {
    'jjvt':'JVT',
    'jcorrjvf':'corrJVF',
    'jrpt':'$R_{p_T}$',
    'jb2bjvt':'B2BJVT',
    'jb2bcorrjvf':'B2BcorrJVF',
    'jb2brpt':'B2BRpT',
    'jb2bjvt_trk':'track B2BJVT',
    'jb2bcorrjvf_trk':'track B2BcorrJVF',
    'jb2bcorrjvf_trk2':'track-jet R=0.2 B2BcorrJVF',
    'jb2bcorrjvf_trk4':'track-jet R=0.4 B2BcorrJVF',
    'jb2brpt_trk':'track B2BRpT'
    }

import json
def plot(var='jb2bjvt'):
    rocdict = json.load(open('../output/roc_'+var+'_'+ptbin+'.json'))
    efficiency = rocdict['efficiency']
    efficiencyerr = rocdict['efficiencyerr']
    mistag = rocdict['mistag']
    mistagerr = rocdict['mistagerr']

    plt.errorbar(efficiency,mistag,
                 xerr=efficiencyerr,yerr=mistagerr,
                 fmt='o--',
                 label=labeldict[var])

for var in vars:
    plot(var)
plt.xlabel('Efficiency')
plt.ylabel('Fake Rate')
plt.legend(loc='upper left')
plt.xlim([0.75,1.0])
#plt.yscale('log')
plt.ylim([0.4,1.0])
plt.savefig('../plots/roc_'+ptbin+'.png')

