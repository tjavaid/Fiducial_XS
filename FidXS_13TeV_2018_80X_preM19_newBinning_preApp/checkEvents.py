from ROOT import *

#f = TFile("data_13TeV.root","READ")
f = TFile("data_13TeV_old.root","READ")
t = f.Get("passedEvents")


aveErr_lo=0.0; nlo=0;
aveErr_mid=0.0; nmid=0;
aveErr_hi=0.0; nhi=0;

for i in xrange(t.GetEntriesFast()):
  t.GetEntry(i)

  if (t.finalState==2): continue
  if (t.CMS_zz4l_mass<122.0 or t.CMS_zz4l_mass>128.0): continue

  if (t.melaLD>0.75): 
    aveErr_hi+=t.CMS_zz4l_massErr/t.CMS_zz4l_mass
    nhi+=1
  if (t.melaLD>0.25 and t.melaLD<0.75): 
    aveErr_mid+=t.CMS_zz4l_massErr/t.CMS_zz4l_mass
    nmid+=1
  if (t.melaLD<0.25): 
    aveErr_lo+=t.CMS_zz4l_massErr/t.CMS_zz4l_mass
    nlo+=1
    

print "hi KD",(aveErr_hi/nhi),nhi
print "mid KD",(aveErr_mid/nmid),nmid
print "lo KD",(aveErr_lo/nlo),nlo
