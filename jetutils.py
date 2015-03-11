import json
from numpy import log

class Calibration(object):
    
    def __init__(self,jettype='j0',pu='mu20'):
        jetresdict = json.load(open('../output/jetresponse_'+pu+'.json'))
        self.a = jetresdict[jettype][0]
        self.b = jetresdict[jettype][1]

    def getpt(self,jetpt):
        return float(jetpt)/(self.b + self.a/log(jetpt))

class NPVCorrection(object):
    
    def __init__(self,jettype='j0',pu='mu20'):
        jetresdict = json.load(open('../output/npvcorrection_'+pu+'.json'))
        self.a = jetresdict[jettype][1]
        self.b = jetresdict[jettype][0]

    def getpt(self,jetpt,npv):
        return jetpt-self.b*npv
    

#test = Calibration()
#print test.getpt(5)
