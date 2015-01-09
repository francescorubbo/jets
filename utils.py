from sklearn.neighbors import NearestNeighbors
neigh = NearestNeighbors()
from numpy import select

def getassoctrks(tracks,clusters):
    neigh.fit(tracks)
    assoctrks = neigh.radius_neighbors(clusters, 0.2, return_distance=False)
    return assoctrks

def computeJVF(assoctrks,trkpt,trkispv):
    if len(assoctrks)<1:return -1
    totpt = trkpt[assoctrks].sum()
    ptpv = (trkpt*trkispv)[assoctrks].sum()
    return ptpv/totpt

def computeJVFcorr(assoctrks,trkpt,trkispv,k):
    if len(assoctrks)<1:return -1
    trknotpv = (1-trkispv)
    if trknotpv[assoctrks].sum()<1:return 1
    ptpu = (trkpt*trknotpv)[assoctrks].sum()
    ptpv = (trkpt*trkispv)[assoctrks].sum()
    return ptpv/(ptpv+ptpu/(trkpt.size*k))

def computeRpt(assoctrks,trkpt,trkispv,clpt):
    ptpv = (trkpt*trkispv)[assoctrks].sum()
    return ptpv/clpt

#def weighttrkpt(trkpt,trketa,trkphi,ceta,cphi):
    
