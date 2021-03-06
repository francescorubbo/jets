import numpy as np
def get(name,outdir=''):
    theoutdir = '../output/'+outdir
    out = np.load(theoutdir+name+'.npy')
    return out

import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)

pltdir = '../plots/'

bins=np.arange(0,2,0.1)
plt.hist(get('rpt','pu0/'),bins=bins,alpha=0.5,label=r'$<\mu>=1$',normed=True)
plt.hist(get('rpt','pu40/'),bins=bins,alpha=0.5,label=r'$<\mu>=40$',normed=True)
plt.xlabel(r'$R_{p_T}$')
plt.legend(frameon=False)
plt.savefig(pltdir+'rpt.png')
plt.close()

plt.hist(get('jvf','pu0/'),alpha=0.5,label=r'$<\mu>=1$',normed=True)
plt.hist(get('jvf','pu40/'),alpha=0.5,label=r'$<\mu>=40$',normed=True)
plt.xlabel('JVF')
plt.legend(frameon=False)
plt.savefig(pltdir+'jvf.png')
plt.close()

plt.hist(get('corrjvf','pu0/'),alpha=0.5,label=r'$<\mu>=1$',normed=True)
plt.hist(get('corrjvf','pu40/'),alpha=0.5,label=r'$<\mu>=40$',normed=True)
plt.xlabel('corrJVF')
plt.legend(frameon=False)
plt.savefig(pltdir+'corrjvf.png')
plt.close()

plt.hist(get('clclam','pu0/'),alpha=0.5,label=r'$<\mu>=1$',normed=True)
plt.hist(get('clclam','pu40/'),alpha=0.5,label=r'$<\mu>=40$',normed=True)
plt.xlabel(r'$\lambda_{center}$')
plt.legend(frameon=False)
plt.savefig(pltdir+'clclam.png')
plt.close()

bins=np.arange(0,1,0.1)
plt.hist(get('clfem','pu0/'),alpha=0.5,label=r'$<\mu>=1$',normed=True,bins=bins)
plt.hist(get('clfem','pu40/'),alpha=0.5,label=r'$<\mu>=40$',normed=True,bins=bins)
plt.xlabel(r'$f_{EM}$')
plt.legend(frameon=False)
plt.savefig(pltdir+'clfem.png')
plt.close()

xarr = get('clpt','pu0/')
yarr = get('clfem','pu0/')
xx = []
yy = []
for x,y in zip(xarr,yarr):
    if x<0 or x>3: continue
    if y<0.3 or y>0.8: continue
    xx.append(x)
    yy.append(y)

plt.hexbin(xx,yy,
           cmap=plt.cm.YlOrRd)
plt.xlabel(r'cluster $p_T$ [GeV]')
plt.ylabel(r'$f_{EM}$')
plt.savefig(pltdir+'femvsclpt_pu0.png')
plt.close()

xarr = get('clpt','pu40/')
yarr = get('clfem','pu40/')
xx = []
yy = []
for x,y in zip(xarr,yarr):
    if x<0 or x>3: continue
    if y<0.3 or y>0.8: continue
    xx.append(x)
    yy.append(y)

plt.hexbin(xx,yy,
           cmap=plt.cm.YlOrRd)
plt.xlabel(r'cluster $p_T$ [GeV]')
plt.ylabel(r'$f_{EM}$')
plt.savefig(pltdir+'femvsclpt_pu40.png')
plt.close()

import sys
sys.exit()

bins=np.arange(0,2,0.1)
plt.hist(get('rpt','outputdr01/'),bins=bins,alpha=0.5,label=r'$\Delta R=0.1$')
plt.hist(get('rpt','outputdr02/'),bins=bins,alpha=0.5,label=r'$\Delta R=0.2$')
plt.hist(get('rpt','outputdr03/'),bins=bins,alpha=0.5,label=r'$\Delta R=0.3$')
plt.xlabel(r'$R_{p_T}$')
plt.legend(frameon=False)
plt.savefig(pltdir+'rpt.png')
plt.close()

plt.hist(get('jvf','outputdr01/'),alpha=0.5,label=r'$\Delta R=0.1$')
plt.hist(get('jvf','outputdr02/'),alpha=0.5,label=r'$\Delta R=0.2$')
plt.hist(get('jvf','outputdr03/'),alpha=0.5,label=r'$\Delta R=0.3$')
plt.xlabel('JVF')
plt.legend(frameon=False)
plt.savefig(pltdir+'jvf.png')
plt.close()

plt.hist(get('corrjvf','outputdr01/'),alpha=0.5,label=r'$\Delta R=0.1$')
plt.hist(get('corrjvf','outputdr02/'),alpha=0.5,label=r'$\Delta R=0.2$')
plt.hist(get('corrjvf','outputdr03/'),alpha=0.5,label=r'$\Delta R=0.3$')
plt.xlabel('corrJVF')
plt.legend(frameon=False)
plt.savefig(pltdir+'corrjvf.png')
plt.close()

cpt = get('clpt','outputdr03/')
plt.hist(cpt[cpt<10],alpha=0.5)
plt.xlabel(r'cluster $p_T$')
plt.savefig(pltdir+'clpt.png')
plt.close()

jvf = get('jvf','outputdr02/')
jvfcorr = get('corrjvf','outputdr02/')
jvflowpt = np.select([cpt<1],[jvf])
jvflowpt = jvflowpt[jvflowpt>0]
jvfhipt = np.select([cpt>1],[jvf])
jvfhipt = jvfhipt[jvfhipt>0]
jvfhipt5 = np.select([cpt>5],[jvf])
jvfhipt5 = jvfhipt5[jvfhipt5>0]
jvfcorrlowpt = np.select([cpt<1],[jvf])
jvfcorrlowpt = jvfcorrlowpt[jvfcorrlowpt>0]
jvfcorrhipt = np.select([cpt>1],[jvfcorr])
jvfcorrhipt = jvfcorrhipt[jvfcorrhipt>0]
jvfcorrhipt5 = np.select([cpt>5],[jvfcorr])
jvfcorrhipt5 = jvfcorrhipt5[jvfcorrhipt5>0]

plt.hist(jvflowpt,alpha=0.5,label='cluster $p_T<1$ GeV',normed=True)
plt.hist(jvfhipt,alpha=0.5,label='cluster $p_T>1$ GeV',normed=True)
plt.hist(jvfhipt5,alpha=0.5,label='cluster $p_T>5$ GeV',normed=True)
plt.xlabel(r'JVF')
plt.legend(frameon=False,loc='upper left')
plt.savefig(pltdir+'jvfpt.png')
plt.close()

plt.hist(jvfcorrlowpt,alpha=0.5,label='cluster $p_T<1$ GeV',normed=True)
plt.hist(jvfcorrhipt,alpha=0.5,label='cluster $p_T>1$ GeV',normed=True)
plt.hist(jvfcorrhipt5,alpha=0.5,label='cluster $p_T>5$ GeV',normed=True)
plt.xlabel(r'JVFcorr')
plt.legend(frameon=False,loc='upper left')
plt.savefig(pltdir+'jvfcorrpt.png')
plt.close()


#x = get('clpt','../outputdr02/')
#y = get('jvf','../outputdr02/')
#plt.hexbin(x,y,
#           cmap=plt.cm.YlOrRd,bins='log')
#plt.xlabel(r'cluster $p_T$')
#plt.ylabel('JVF')
#plt.savefig('../plots/jvfvsclpt.png')
#plt.close()

