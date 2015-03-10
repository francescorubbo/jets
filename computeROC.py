from numpy import array
import json
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
plt.style.use('atlas')

ptmin = 30
ptmax = 40

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
    if eff>0.87 and fake<0.7:
        print cut,eff,fake
    return eff,efferror,fake,fakeerror


ptcuts = [10,15,20,25,30]
colors = ['b','g','r','c','m']
dphicuts = [0.2,0.4,0.6,0.8,1.5]
asymmcuts = [0.1,0.2,0.3,0.4,1.0]
markers = ['o','v','^','*','D']

for ptcut,col in zip(ptcuts,colors):
    for a,marker in zip(asymmcuts,markers):
        cuts = ['pt%d_dphi%1.1f_a%1.1f'%(ptcut,dphi,a) for dphi in dphicuts]
        (effs,efferrors,fakes,fakeerrors) = zip(*[geteffs(cut) for cut in cuts])
#        plt.errorbar(effs,fakes,xerr=efferrors,yerr=fakeerrors,fmt=marker,color=col,
#                     label='$p_T^{ctl}>%d$ $GeV$, $A_{p_T}<%1.1f$'%(ptcut,a))
        plt.plot(effs,fakes,marker,color=col,
                 label='$p_T^{ctl}>%d$ $GeV$, $A_{p_T}<%1.1f$'%(ptcut,a))

#plt.plot([0,1],[0,1],'k--')
plt.xlabel('Efficiency')
plt.ylabel('Fake rate')
#plt.ylim([0.4,1.0])
#plt.xlim([0.6,1.0])
lgd = plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=5, borderaxespad=0.,fontsize=6)
plt.savefig('test.png', bbox_extra_artists=(lgd,), bbox_inches='tight')
