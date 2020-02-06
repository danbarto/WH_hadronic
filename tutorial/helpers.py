import ROOT

from math import *

def getEList(chain, cut, newname='eListTMP'):
    chain.Draw('>>eListTMP_t', cut)
    #elistTMP_t = ROOT.gROOT.Get('eListTMP_t')
    elistTMP_t = ROOT.gDirectory.Get('eListTMP_t')
    elistTMP = elistTMP_t.Clone(newname)
    del elistTMP_t
    return elistTMP

def deltaPhi(phi1, phi2):
    dphi = phi2-phi1
    if  dphi > pi:
        dphi -= 2.0*pi
    if dphi <= -pi:
        dphi += 2.0*pi
    return abs(dphi)

def deltaR2(l1, l2):
    return deltaPhi(l1['phi'], l2['phi'])**2 + (l1['eta'] - l2['eta'])**2

def deltaR(l1, l2):
    return sqrt(deltaR2(l1,l2))

def getVarValue(c, var, n=-1):
    try:
        att = getattr(c, var)
    except AttributeError:
        return float('nan')
    if n>=0:
        if n<att.__len__():
            return att[n]
        else:
            return float('nan')
    return att

def getObjDict(c, prefix, variables, i):
    res={var: getVarValue(c, prefix+var, i) for var in variables}
    res['index']=i
    return res

def getCollection(c, prefix, variables, counter_variable):
    return [getObjDict(c, prefix+'_', variables, i) for i in range(int(getVarValue(c, counter_variable)))]

jetVars = ['eta','pt','phi','btagDeepB', 'btagCSVV2', 'jetId', 'area', 'rawFactor', 'corr_JER']

def jetId(j, ptCut=30, absEtaCut=2.4, ptVar='pt', idVar='jetId', corrFactor=None):
  j_pt = j[ptVar] if not corrFactor else j[ptVar]*j[corrFactor]
  return j_pt>ptCut and abs(j['eta'])<absEtaCut and ( j[idVar] > 0 if idVar is not None else True )

def isBJet(j, tagger = 'DeepCSV', year = 2016):
    if tagger == 'CSVv2':
        if year == 2016:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
            return j['btagCSVV2'] > 0.8484
        elif year == 2017 or year == 2018:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            return j['btagCSVV2'] > 0.8838
        else:
            raise (NotImplementedError, "Don't know what cut to use for year %s"%year)
    elif tagger == 'DeepCSV':
        if year == 2016:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
            return j['btagDeepB'] > 0.6321
        elif year == 2017:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation94X
            return j['btagDeepB'] > 0.4941
        elif year == 2018:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation102X
            return j['btagDeepB'] > 0.4184
        else:
            raise (NotImplementedError, "Don't know what cut to use for year %s"%year)

def getJets(c, jetVars=jetVars, jetColl="Jet"):
    jets = [getObjDict(c, jetColl+'_', jetVars, i) for i in range(int(getVarValue(c, 'n'+jetColl)))]
    return [ j for j in jets if jetId(j)]

def getBJets(c, jetVars=jetVars, jetColl="Jet", year=2018):
    jets = [getObjDict(c, jetColl+'_', jetVars, i) for i in range(int(getVarValue(c, 'n'+jetColl)))]
    return [ j for j in jets if (jetId(j) and isBJet(j, year=year))]

