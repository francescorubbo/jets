import matplotlib.pyplot as plt
plt.style.use('atlas')
from matplotlib import rc
rc('text', usetex=True)
from numpy import histogram,vectorize,array
from math import sqrt
import json

puorhs = 'jishs'
ptcuts = ['10','15','20','25','30']

fwdjets = json.load(open('../output/fwdall_'+puorhs+'.json'))
fwdmatchedjets = json.load(open('../output/fwdmatched_'+puorhs+'.json'))

def efferr(k,N):
    return sqrt(k*(1-k/N))/N
vefferr = vectorize(efferr)

binedges = [20,30,40,50,70,100]
bincenters = [25,35,45,60,85]
den = histogram(fwdjets,binedges)[0]
print den
for ptcut in ptcuts:
    numint = histogram(fwdmatchedjets[ptcut],binedges)[0]
    num = numint.view('float64')
    num[:] = numint
    eff = num/den
    efferr = vefferr(num,den)
    plt.errorbar(bincenters,eff,yerr=efferr,
                 fmt='o--',label='$p_T^{ctl}>%s$ GeV'%ptcut)
    
plt.xlabel('$p_T^{fwd}$ [GeV]')    
plt.ylim([0.,1.])
plt.legend(loc='lower right')
plt.savefig('../plots/matcheff_'+puorhs+'.png')
plt.close()

ctljetispu = json.load(open('../output/ctlispu_'+puorhs+'.json'))
ctljetishs = json.load(open('../output/ctlishs_'+puorhs+'.json'))

for ptcut in ptcuts:
    puctljets = array(ctljetispu[ptcut])
    fwdjets = array(fwdmatchedjets[ptcut])
    den = histogram(fwdjets,binedges)[0]
    
    numint = histogram(fwdjets[puctljets],binedges)[0]
    num = numint.view('float64')
    num[:] = numint
    eff = num/den
    efferr = vefferr(num,den)
    puplt = plt.errorbar(bincenters,eff,yerr=efferr,
                 fmt='o--',label='$p_T^{ctl}>%s$ GeV'%ptcut)
                 
plt.xlabel('$p_T^{fwd}$ [GeV]')    
plt.ylim([0.,1.])
plt.legend(loc='lower right')
plt.savefig('../plots/matchedpueff_'+puorhs+'.png')
plt.close()


for ptcut in ptcuts:
    puctljets = array(ctljetispu[ptcut])
    hsctljets = array(ctljetishs[ptcut])
    fwdjets = array(fwdmatchedjets[ptcut])
    den = histogram(fwdjets,binedges)[0]
    print 'den',den

    numint = histogram(fwdjets[hsctljets],binedges)[0]
    num = numint.view('float64')
    num[:] = numint
    eff = num/den
    efferr = vefferr(num,den)
    plt.errorbar(bincenters,eff,yerr=efferr,
                 fmt='*--',label='$p_T^{ctl}>%s$ GeV'%ptcut)

plt.xlabel('$p_T^{fwd}$ [GeV]')    
plt.ylim([0.,1.])
plt.legend(loc='lower right')
plt.savefig('../plots/matchedhseff_'+puorhs+'.png')
plt.close()
