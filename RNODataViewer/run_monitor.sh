#export rnog_eventbrowser branch of NuRadioMC 
export PYTHONPATH=/Users/shallmann/software/rnog_eventbrowser:$PYTHONPATH
#export feature/monitoring branch of RNODataViewer
export PYTHONPATH=/Users/shallmann/software/RNODataViewer_Christoph:$PYTHONPATH

export RNO_DATA_DIR="/Users/shallmann/dcachemount" #"/Users/shallmann/Desktop/rnog_field_data"

#gunicorn monitoring:server -b 127.0.0.1:8080
python monitoring.py --port 8049 --open-window
