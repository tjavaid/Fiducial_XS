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
Final step is to clone the correct verison of the code. At the moment the working version can be found on the ```CMSSW_10_X``` branch, which can be cloned via the following command:
```
cd $CMSSW_BASE/src/
#git clone -b CMSSW_10_X git@github.com:vukasinmilosevic/Fiducial_XS.git
git clone -b CMSSW_10_X_Combine git@github.com:vukasinmilosevic/Fiducial_XS.git
```

## 2. Running the measurement

### 2.1 Running the efficiencies step

Current example running ```mass4l``` variable via ```nohup```. For local testing remove ```nohup``` (and pipelining into a .log file if wanting terminal printout).

```
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4mu"  --year="2018" >& effs_mass4l_4mu_2018.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4e"  --year="2018" >& effs_mass4l_4e_2018.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "2e2mu"  --year="2018" >& effs_mass4l_2e2mu_2018.log &
nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4l"  --year="2018" >& effs_mass4l_4l_2018.log &
# for the various observables and all three years:

sh doAllEffs_channels_2016.sh
sh doAllEffs_channels_2017.sh
sh doAllEffs_channels_2018.sh

# merge the channel outputs to single:
python -u collectInputs.py --obsName="mass4l" --year="2018"
# for the various observables and all three years:

sh collectInputs_2016.sh
sh collectInputs_2017.sh
sh collectInputs_2018.sh

```

#Running the plotter:

```
#skipping for mass4l 
#python -u plot2dsigeffs.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|"
```

### 2.2. Running the uncertainties step

```
nohup python -u getUnc_Unc.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" --year="2018" >& unc_mass4l_2018.unc &

# for the various observables :
sh doAllUnc_2018.sh
```

### 2.3. Obtaining the interpolated values of eff./acc. for 125.38 (run only if the channel output is merged, all three years in case of full Run2 measurement.)

```
nohup python -u interpolate_differential_full.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --year="2018" >& full_interpolation_mass4l_2018.txt &

# for the various observables in years:
sh interpolate_differential_full_all_2016.sh
sh interpolate_differential_full_all_2017.sh
sh interpolate_differential_full_all_2018.sh

## for theory uncertainties interpolation
nohup python -u interpolate_differential_pred.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --year="2018" >& pred_interpolation_mass4l_2018.txt &
# for several observables:
sh interpolate_differential_pred_all_2018.sh

```
### 2.4 Running the background template maker

```
nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|" --redoTemplates --templatesOnly --era="2018" >& templates_mass4l_2018.log &
# suggested to simultaneously run for all three years
nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|" --redoTemplates --templatesOnly --era="Full" >& templates_mass4l_Full.log &
# for various observables (full Run2):
sh doAllTemplates_Full.sh

```

### 2.5 Runing the final measurement and plotters

```

# for individual year:
nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --calcSys --era="2018"  >& log_mass4l_2018.txt &

# for full Run 2:

nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --calcSys --era="Full"  >& log_mass4l_Full.txt & 

#full Run2 and various observables
sh doAllObs_Full.sh

# output of this step are likelihood scan, asimov fits, differential yield and differential measurement plots. 


```
