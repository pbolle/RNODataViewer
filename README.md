# RNODataViewer

## Setup guide
### Setting up NuRadioMC
NuRadioMC is needed, the I/O modules for reading in RNO-G .root files are currently still only in the ```rnog_eventbrowser``` branch, you can find install instructions https://github.com/nu-radio/NuRadioMC/wiki in the **manual_installation** section. This should agree with doing the following:

```
pip install numpy scipy matplotlib "tinydb>=4.1.1" tinydb-serialization aenum astropy "radiotools>=0.2.0" h5py pyyaml peakutils requests pymongo dash plotly sphinx
pip install uproot awkward
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

# get the feature/integrate_root_files branch, which is able to use RNO-G .root files
git checkout feature/integrate_root_files

# and add the RNODataViewer to your PYTHONPATH
export PYTHONPATH=$HOME/software/RNODataViewer:$PYTHONPATH
```
## Usage
Execute the ```index.py``` passing either the path to an RNO-G file containing waveform data, or a directory with data files.
```
python RNODataViewer/index.py /some/path/to/combined.root
```
a web browser window should open automatically, where you can choose stations and (one or several) channels and update overview plots using the refresh buttons in the plot windows

This tool is still basic right now ;)
