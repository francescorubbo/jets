from numpy import load,mean,std,array,median

pltdir = '../plots/'

def getmeans(jet='j0'):
    resdict = load('../output/resvsnpv_'+jet+'.npy')
    keys = [10,20,30,40,50]
    resdict = resdict[()]
    y = [mean(resdict[k]) for k in keys]
    x = [k-5 for k in keys]
    return x,y

def getstds(jet='j0'):
    resdict = load('../output/resvsnpv_'+jet+'.npy')
    keys = [10,20,30,40,50]
    resdict = resdict[()]
    y = [std(resdict[k]) for k in keys]
    x = [k-5 for k in keys]
    return x,y
    
import matplotlib.pyplot as plt
from matplotlib import rc
rc('text', usetex=True)


x,y = getmeans('j0')
j0 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getmeans('j1')
j1 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getmeans('j2')
j2 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getmeans('j3')
j3 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getmeans('j4')
j4 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getmeans('j5')
j5 = plt.plot(x,y,marker='o',linestyle='--')

plt.ylim([-10,0])
plt.xlim([0,50])
plt.xlabel(r'NPV')
plt.ylabel(r'$<p_T^{reco}-p_T^{true}>$ [GeV]')
#plt.legend([j0res,j1res,j2res,j3res,j4res,j5res],
#           ['incl.','$corrJVF>0.1$','$corrJVF>0.2$','$corrJVF>0.3$','$corrJVF>0.4$','$corrJVF>0.5$'],
#           loc='upper left',frameon=False,numpoints=1)
plt.savefig(pltdir+'jresvsnpvmean.png')
plt.close()

x,y = getstds('j0')
j0 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getstds('j1')
j1 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getstds('j2')
j2 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getstds('j3')
j3 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getstds('j4')
j4 = plt.plot(x,y,marker='o',linestyle='--')
x,y = getstds('j5')
j5 = plt.plot(x,y,marker='o',linestyle='--')

plt.ylim([0,10])
plt.xlim([0,50])
plt.xlabel(r'NPV')
plt.ylabel(r'$\sigma(p_T^{reco}-p_T^{true})$ [GeV]')
#plt.legend([j0res,j1res,j2res,j3res,j4res,j5res],
#           ['incl.','$corrJVF>0.1$','$corrJVF>0.2$','$corrJVF>0.3$','$corrJVF>0.4$','$corrJVF>0.5$'],
#           loc='upper left',frameon=False,numpoints=1)
plt.savefig(pltdir+'jresvsnpvstd.png')
plt.close()
