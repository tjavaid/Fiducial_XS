# Fiducial_XS

SCRAM_ARCH=slc6_amd64_gcc491

cmsrel CMSSW_7_4_7

cd CMSSW_7_4_7/src/

cmsenv

git clone git@github.com:tjavaid/Fiducial_XS.git

git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

scramv1 b 

cd ..

scramv1 b 

cd Fiducial_XS/FidXS_13TeV_2018_80X_preM19_newBinning_preApp

voms-proxy-init -voms cms

# Now setup is ready for measurement

