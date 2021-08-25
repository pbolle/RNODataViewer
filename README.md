# RNODataViewer

## Setup guide
### Setting up NuRadioMC
NuRadioMC is needed, the I/O modules for reading in RNO-G .root files are currently still only in the ```rnog_eventbrowser``` branch, you can find install instructions https://github.com/nu-radio/NuRadioMC/wiki in the **manual_installation** section. This should agree with doing the following:

```
pip install numpy scipy matplotlib tinydb>=4.1.1 tinydb-serialization aenum astropy radiotools>=0.2.0 h5py pyyaml peakutils requests pymongo dash plotly sphinx
pip install cython
cd $HOME/software #or any other install directory
git clone https://github.com/nu-radio/NuRadioMC.git
cd NuRadioMC
# get the rnog_eventbrowser branch
git checkout rnog_eventbrowser
# and add NuRadioMC to your PYTHONPATH
export PYTHONPATH=$HOME/software/NuRadioMC:$PYTHONPATH
```
### Setting up The RNODataViewer
```
cd $HOME/software #or any other install directory
git clone git@github.com:RNO-G/RNODataViewer.git
cd RNODataViewer
git checkout feature/integrate_root_files
# and add the RNODataViewer to your PYTHONPATH
export PYTHONPATH=$HOME/software/RNODataViewer:$PYTHONPATH
```

