#export rnog_eventbrowser branch of NuRadioMC 
export PYTHONPATH=/Users/shallmann/software/rnog_eventbrowser:$PYTHONPATH
#export feature/monitoring branch of RNODataViewer
export PYTHONPATH=/Users/shallmann/software/RNODataViewer_Christoph:$PYTHONPATH

export RNO_DATA_DIR="/Users/shallmann/dcachemount" #"/Users/shallmann/Desktop/rnog_field_data"
python monitoring.py
