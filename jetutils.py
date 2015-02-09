import json
from numpy import log

class Calibration(object):
    
    def __init__(self,jettype='j0',pu='mu20'):
        jetresdict = json.load(open('../output/jetresponse_mu20.json'))
        self.a = jetresdict[jettype][0]
        self.b = jetresdict[jettype][1]

    def getpt(self,jetpt):
        return float(jetpt)/(self.b + self.a/log(jetpt))
    

#test = Calibration()
#print test.getpt(5)
