# Fiducial_XS

SCRAM_ARCH=slc6_amd64_gcc491

cmsrel CMSSW_7_4_7

cd CMSSW_7_4_7/src/

cmsenv

git clone git@github.com:tjavaid/fiducial_xs.git

git clone git@github.com:cms-analysis/higgsanalysis-combinedlimit.git HiggsAnalysis/CombinedLimit

cp /afs/cern.ch/user/t/tjavaid/public/models/*.py $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/python/

scramv1 b 

cd ..

scramv1 b 

cd Fiducial_XS/FidXS_13TeV_2018_80X_preM19_newBinning_preApp

voms-proxy-init -voms cms

# Now set is ready for measurement

sh doAllEffs_channels_PAS.sh #This macro is to compute in bins of differential variables the efficiencies, acceptance etc. and corresponding uncertainties.

python collectInputs.py # This will combine, for specified observable(s), all channel-wise computed outputs to a single file and will store in "datacardsInputs" dirctory

sh doAll2DEff_PAS.sh # Will produce 2D plots to see migrated events in reconstruction bins for differential variables

sh doAllTemplates_PAS.sh # This macro is to compute in bins of differential variables the background templates

sh doAllUnc_PAS.sh # This macro is to compute in bins of differential variables the theoretical predictions and uncertainties

sh doAllObs_PAS.sh # This macro will use ingredients produced as outputs of previous steps to give final differential plots.
