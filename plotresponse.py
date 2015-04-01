from numpy import load,log,linspace,digitize,array,mean,std
from scipy.optimize import curve_fit
from scipy.stats import norm

pu = 'voronoi_cvf'
jetr='jvoro'
jets = ['j0','jnoarea0','j0cvf',jetr+'0',jetr+'1',jetr+'10',jetr+'0cvf5',jetr+'0cvfx',jetr+'1cvf5',jetr+'1cvfx',jetr+'s',jetr+'cvf5s',jetr+'cvfxs']

def func(x,a,b,c):
    return a + b*log(x) + c*log(x)**2

ptedges = range(20,200,10)

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)
#plt.style.use('atlas')
import matplotlib.mlab as mlab

sigma_frac=0.8

def fitres(jet='j0'):
    responses = load('../output/responses_'+jet+'_'+pu+'.npy')
    truepts = load('../output/truepts_'+jet+'_'+pu+'.npy')
    recopts = load('../output/recopts_'+jet+'_'+pu+'.npy')

    ptbins = digitize(truepts,ptedges)
    avgres = []
    avgpt = []
    for ptbin in xrange(1,len(ptedges)): 
        resdata = responses[ptbins==ptbin]
        ptdata = recopts[ptbins==ptbin]
        if ptbin==1: 
            resdata = resdata[resdata<mean(resdata)+sigma_frac*std(resdata)]
            ptdata = ptdata[resdata<mean(resdata)+sigma_frac*std(resdata)]
        gfunc = norm
        (mu,sigma) = gfunc.fit(resdata)
        n,bins,patches = plt.hist(resdata,normed=True,bins=50)
        y = gfunc.pdf( bins, mu, sigma)
        l = plt.plot(bins, y, 'r--', linewidth=2)
        plt.xlabel('$p_T^{reco}/p_T^{true}$')
        plt.ylabel('a.u.')
        plt.savefig('../plots/resbin%d_'%ptbin+jet+'_'+pu+'.png')
        plt.close()
        avgres.append(mu)
        avgpt.append(mean(ptdata))
    
    popt, pcov = curve_fit(func, avgpt, avgres)
    print jet
    print popt
    print pcov
    
    xp = linspace(10,200,100)
    plt.plot(recopts,responses,'.',avgpt,avgres,'o',xp,func(xp,*popt),'r-')
    plt.xlabel('$p_T^{reco}$ [GeV]')
    plt.ylabel('$p_T^{reco}/p_T^{true}$')
    plt.savefig('../plots/jetresponse_'+jet+'_'+pu+'.png')
    plt.close()
    return popt

resparams = {}
for jet in jets:
    resparams[jet] = fitres(jet).tolist()

print resparams

import json
with open('../output/jetresponse_'+pu+'.json','w') as outfile:
    json.dump(resparams,outfile)

#closure

from jetutils import Calibration
calibdict = {key: Calibration(key,pu) for key in jets}

from numpy import vectorize

for jet in jets:
    truepts = load('../output/truepts_'+jet+'_'+pu+'.npy')
    recopts = load('../output/recopts_'+jet+'_'+pu+'.npy')
    vgetpt = vectorize(calibdict[jet].getpt)
    recopts = vgetpt(recopts)
    responses = recopts/truepts
    ptbins = digitize(truepts,ptedges)
    avgres = []
    avgpt = []
    for ptbin in xrange(1,len(ptedges)): 
        resdata = responses[ptbins==ptbin]
        ptdata = recopts[ptbins==ptbin]
        if ptbin==1: 
            resdata = resdata[resdata<mean(resdata)+sigma_frac*std(resdata)]
            ptdata = ptdata[resdata<mean(resdata)+sigma_frac*std(resdata)]
        gfunc = norm
        (mu,sigma) = gfunc.fit(resdata)
        n,bins,patches = plt.hist(resdata,normed=True,bins=50)
        y = gfunc.pdf( bins, mu, sigma)
        l = plt.plot(bins, y, 'r--', linewidth=2)
        plt.xlabel('$p_T^{reco}/p_T^{true}$')
        plt.ylabel('a.u.')
        plt.savefig('../plots/closure_resbin%d_'%ptbin+jet+'_'+pu+'.png')
        plt.close()
        avgres.append(mu)
        avgpt.append(mean(ptdata))

    xp = linspace(20,200,100)
    plt.plot(recopts,responses,'.',avgpt,avgres,'o')
    plt.xlabel('$p_T^{reco}$ [GeV]')
    plt.ylabel('$p_T^{reco}/p_T^{true}$')
    plt.savefig('../plots/closure_jetresponse_'+jet+'_'+pu+'.png')
    plt.close()
