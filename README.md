# RNODataViewer

## Aim of the monitoring branch
The monitoring branch is intended to provide a broad overview of the DAQ history of the detector for a selected period, and give the possibility to look deeper into a bunch runs for an individual station, or individual events of a specific data file. To this end it feaures three tabs:
* Monitoring Overview
* Run Browser
* Event Browser

## Setup guide
### Setting up NuRadioMC
NuRadioMC is needed, the I/O modules for reading in RNO-G .root files are currently still only in the ```rnog_eventbrowser``` branch, you can find install instructions https://github.com/nu-radio/NuRadioMC/wiki in the **manual_installation** section. This should agree with doing the following:

- if did not install NuRadioMC before
```
pip install numpy scipy matplotlib tinydb>=4.1.1 tinydb-serialization aenum astropy radiotools>=0.2.0 h5py pyyaml peakutils requests pymongo dash plotly sphinx
pip install cython
pip install uproot, awkward
```
- To install the rnog_eventbrowser branch of NuRadioMC to $HOME/software/NuRadioMC
```
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
git checkout feature/monitoring
# and add the RNODataViewer to your PYTHONPATH
export PYTHONPATH=$HOME/software/RNODataViewer:$PYTHONPATH
```
## Usage
Execute the ```monitoring.py```. It requires the `RNO_DATA_DIR` variable to be set to the top level of the data containing files as `stationXX/runXXX/combined.root` (As in the data directories in WISC/DESY)

After adapting the paths therein to your local install and data directories, you can also run:
```
bash run_monitoring.sh
```
a web browser window should open automatically.
