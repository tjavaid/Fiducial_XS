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

1) sh doAllEffs_channels_PAS.sh # To compute in bins of differential variables the efficiencies, acceptance etc. and corresponding uncertainties.

2) python collectInputs.py # This macro will combine, for specified observable(s), all channel-wise computed outputs to a single file and will store in "datacardsInputs" dirctory

3) sh doAll2DEff_PAS.sh # To produce 2D plots to see migrated events in bins for differential variables

4) sh doAllTemplates_PAS.sh # To compute in bins of differential variables the background templates

5) sh doAllUnc_PAS.sh # To compute in bins of differential variables the theoretical predictions and uncertainties

6) sh doAllObs_PAS.sh # To process over ingredients produced as outputs of previous steps to give final differential plots.
