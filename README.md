# Instructions to run the BBBF differential xs code for CMSSW_10_X releases

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

## 2. Running the measurement

### 2.1 Running the efficiencies step

Current example running ```mass4l``` variable via ```nohup```. For local testing remove ```nohup``` (and pipelining into a .log file if wanting terminal printout).

```
mkdir datacardInputs

nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4mu" >& effs_mass4l_4mu.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4e" >& effs_mass4l_4e.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "2e2mu" >& effs_mass4l_2e2mu.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4l" >& effs_mass4l_4l.log &

python collectInputs.py # currently only active for mass4l, calls be uncommented for the rest of variables

```
