# Instructions to run the BBBF differential xs code for CMSSW_10_X relesases

## 1. CMSSW and cobmine release setup

Taken from Combine official instructions: https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/

CC7 release CMSSW_10_2_X - recommended version
Setting up the environment (once):

```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
cd HiggsAnalysis/CombinedLimit
```

Update to a recommended tag - currently the recommended tag is v8.2.0: see release notes

```
cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
git fetch origin
git checkout v8.2.0
scramv1 b clean; scramv1 b # always make a clean build
```
Depending on where the data/mc is stored, one might need:

```
voms-proxy-init -voms cms
```

# Now set is ready for measurement

sh doAllEffs_channels_PAS.sh #This macro is to compute in bins of differential variables the efficiencies, acceptance etc. and corresponding uncertainties.

python collectInputs.py # This will combine, for specified observable(s), all channel-wise computed outputs to a single file and will store in "datacardsInputs" dirctory

sh doAll2DEff_PAS.sh # Will produce 2D plots to see migrated events in reconstruction bins for differential variables

sh doAllTemplates_PAS.sh # This macro is to compute in bins of differential variables the background templates

sh doAllUnc_PAS.sh # This macro is to compute in bins of differential variables the theoretical predictions and uncertainties

sh doAllObs_PAS.sh # This macro will use ingredients produced as outputs of previous steps to give final differential plots.
