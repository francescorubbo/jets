from numpy import array
import json
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')

ptmin = 20
ptmax = 30

fwdptallhs = array(json.load(open('../output/fwdall_jishs.json')))
fwdptallpu = array(json.load(open('../output/fwdall_jispu.json')))

matchedfwdhs = json.load(open('../output/fwdmatched_jishs.json'))
matchedfwdpu = json.load(open('../output/fwdmatched_jispu.json'))

ctlpufwdhs = json.load(open('../output/ctlispu_jishs.json'))
ctlhsfwdhs = json.load(open('../output/ctlishs_jishs.json'))
ctlpufwdpu = json.load(open('../output/ctlispu_jispu.json'))
ctlhsfwdpu = json.load(open('../output/ctlishs_jispu.json'))

def efferr(k,N):
    return sqrt(k*(1-float(k)/N))/N

def geteffs(cut):
    
    fwdptfwdhs = array(matchedfwdhs[cut])
    fwdptfwdpu = array(matchedfwdpu[cut])

    ctlispufwdhs = array(ctlpufwdhs[cut])
    ctlishsfwdhs = array(ctlhsfwdhs[cut])
    ctlispufwdpu = array(ctlpufwdpu[cut])
    ctlishsfwdpu = array(ctlhsfwdpu[cut])
    
    allhs = len(fwdptallhs[(fwdptallhs>ptmin) & (fwdptallhs<ptmax)])
    matchedhs = len(fwdptfwdhs[(fwdptfwdhs>ptmin) & (fwdptfwdhs<ptmax)])
    taggedhs = len(fwdptfwdhs[(fwdptfwdhs>ptmin) & (fwdptfwdhs<ptmax) & 
                              (ctlispufwdhs==False)])
    ntrue = allhs-matchedhs+taggedhs
    eff = float(ntrue)/allhs
    efferror = efferr(ntrue,allhs)

    allpu = len(fwdptallpu[(fwdptallpu>ptmin) & (fwdptallpu<ptmax)])
    matchedpu = len(fwdptfwdpu[(fwdptfwdpu>ptmin) & (fwdptfwdpu<ptmax)])
    taggedpu = len(fwdptfwdpu[(fwdptfwdpu>ptmin) & (fwdptfwdpu<ptmax) & 
                              (ctlispufwdpu==False)])
    nfake = allpu-matchedpu+taggedpu
    fake = float(nfake)/allpu
    fakeerror = efferr(nfake,allpu)
    if fake<0.55: print cut,eff,fake
    return eff,efferror,fake,fakeerror


ptcuts = [10,15,20,25,30]
dphicuts = [0.2,0.4,0.6,0.8,1.5]
asymmcuts = [0.1,0.2,0.3,0.4,1.0]

for ptcut in  ptcuts:
    cuts = ['pt%d_dphi%1.1f_a%1.1f'%(ptcut,dphi,a) for dphi in dphicuts for a in asymmcuts]
    (effs,efferrors,fakes,fakeerrors) = zip(*[geteffs(cut) for cut in cuts])
    plt.errorbar(effs,fakes,xerr=efferrors,yerr=fakeerrors,fmt='o',label='$p_T^{ctl}>%d$ GeV'%ptcut)

plt.xlabel('Efficiency')    
plt.ylabel('Fake rate')    
plt.legend(loc='upper left')
plt.savefig('test.png')
