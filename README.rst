
=========================================
FiducialXS README Page
=========================================
Instructions to run the xBF team's framework for differential cross-section measurements for CMSSW_10_X releases.
=========================================

Dependencies:

.. image:: https://img.shields.io/static/v1?label=CMSSW%20version&message=10_2_X&color=brightgreen
.. image:: https://img.shields.io/static/v1?label=Combine%20version&message=8_2_0&color=brightgreen

Framework/documentation:

.. image:: https://readthedocs.org/projects/fiducialxs/badge/?version=latest

Detailed documentation regarding the framework can be found in the dedicated `ReadTheDocs <https://fiducialxs.readthedocs.io/en/latest/?badge=latest>`_ page.
This ``README`` file and the official documentation are written in ``.rst`` (ReStructured Text Markup syntax) in order to better explore the options given by ``sphinx`` and ``ReadTheDocs``.
For more details about the Markup syntax, please consult the `ReStructuredText Primer <https://docutils.sourceforge.io/docs/user/rst/quickstart.html>`_.


1. Setup the correct CMSSW and Combine releases
=========================================
These are formed from from the `official Combine framework instructions <https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/>`_.

CC7 release CMSSW_10_2_X - recommended version
Setting up the environment (once): ::

  export SCRAM_ARCH=slc7_amd64_gcc700
  cmsrel CMSSW_10_2_13
  cd CMSSW_10_2_13/src
  cmsenv
  git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
  cd HiggsAnalysis/CombinedLimit

Update to a recommended tag - currently the recommended tag is v8.2.0: see release notes: ::


  cd $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit
  git fetch origin
  git checkout v8.2.0
  scramv1 b clean; scramv1 b # always make a clean build

Depending on where the data/mc is stored, one might need: ::

  voms-proxy-init -voms cms

Final step is to clone the correct verison of the code. At the moment the working version can be found on the ```CMSSW_10_X``` branch, which can be cloned via the following command: ::

  cd $CMSSW_BASE/src/
  git clone -b CMSSW_10_X git@github.com:vukasinmilosevic/Fiducial_XS.git
  cd Fiducial_XS

2. Running the measurement
=========================================

2.1 Using the ``RunEverything.py`` script:
-----------------------------------------

Now, all steps can be run using script ``RunEverything.py``. The available options are: ::


  usage: RunEverything.py [-h] [-s {1,2,3,4,5}] [-c CHANNELS [CHANNELS ...]]
                        [-p NTUPLEDIR] [-m HIGGSMASS] [-r {0,1}]

  Input arguments

  optional arguments:
    -h, --help            show this help message and exit
    -s {1,2,3,4,5}        Which step to run
    -c CHANNELS [CHANNELS ...]
                          list of channels
    -p NTUPLEDIR          Path of ntuples
    -m HIGGSMASS          Higgs mass
    -r {0,1}              if 1 then it will run the commands else it will just
                          print the commands

Commands to run: ::


  python RunEverything.py -r 1 -s 1 # step-1
  python RunEverything.py -r 1 -s 2 # step-2
  python RunEverything.py -r 1 -s 3 # step-3
  python RunEverything.py -r 1 -s 4 # step-4
  python RunEverything.py -r 1 -s 5 # step-5


2.2 Detailed, step-by-step instructions
---------------------------------------

2.2.1 Running the efficiencies step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Current example running ``mass4l`` variable via ``nohup``. For local testing remove ``nohup`` (and pipelining into a .log file if wanting terminal printout). ::

  nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4mu" >& effs_mass4l_4mu.log &
  nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4e" >& effs_mass4l_4e.log &
  nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "2e2mu" >& effs_mass4l_2e2mu.log &
  nohup python -u efficiencyFactors.py -l -q -b --obsName="mass4l" --obsBins="|105.0|140.0|" -c "4l" >& effs_mass4l_4l.log &

  python collectInputs.py # currently only active for mass4l, calls be uncommented for the rest of variables

Running the plotter: ::

  #skipping for mass4l
  #python -u plot2dsigeffs.py -l -q -b --obsName="pT4l" --obsBins="|0|10|20|30|45|80|120|200|13000|"


2.2.2. Running the uncertainties step
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  python -u getUnc_Unc.py --obsName="mass4l" --obsBins="|105.0|140.0|" >& unc_mass4l.log &
  

2.2.3 Running the background template maker
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

  python -u runHZZFiducialXS.py --dir="/eos/home-v/vmilosev/Skim_2018_HZZ/WoW/" --obsName="mass4l" --obsBins="|105.0|140.0|" --redoTemplates --templatesOnly


2.2.4 Runing the final measurement and plotters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For the last step a data file is needed as input, even for the blinded step (!). I've stored the previous one in my public folder: ::

  /afs/cern.ch/user/v/vmilosev/public/data_13TeV.root
  
or one can copy the data file from the data/mc folder and properly rename it. One additional set of models is needed in order to run the combine step. The HZZ4l specific modules stored here: ::

  /afs/cern.ch/user/v/vmilosev/public/HZZ4l_models/

needs to be added to the corresponding ``$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/python`` collection of libraries.

The command to run the measurement and the plotters is: ::

  nohup python -u runHZZFiducialXS.py --obsName="mass4l" --obsBins="|105.0|140.0|"  --calcSys --asimovMass 125.0  >& log_mass4l_Run2Fid.txt &


Things to fix
-------------------
Specific
^^^^^^^^^^^^^^^^^^^
1. Hardcoded paths in `LoadData.py <https://github.com/vukasinmilosevic/Fiducial_XS/edit/CMSSW_10_X_VM_docs/python/LoadData.py#8/>`_

General
^^^^^^^^^^^^^^^^^^

1. Add the `choices` for argparser whereever its possible. So, that code won't run if we provide wrong arguments.
