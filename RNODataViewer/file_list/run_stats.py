import numpy as np
import os
import astropy.time
import pandas as pd

class RunStats:
    summary_csv = "https://www.zeuthen.desy.de/~shallman/rnog_run_summary.csv"
    def __init__(self, top_level_dir):
        self.run_summary_from_csv(self.summary_csv, top_level_dir)
        self.filter_available_runs()
    def run_summary_from_csv(self, csv, top_level_dir="."):
        self.run_table = pd.read_csv(csv)
        self.run_table["mjd_first_event"] = np.array(astropy.time.Time(np.array(self.run_table["time first event"]).astype("str"), format='iso').mjd)
        self.run_table["mjd_last_event"] = np.array(astropy.time.Time(np.array(self.run_table["time last event"]).astype("str"), format='iso').mjd)
        filenames_root = ["/".join([top_level_dir, path]) for path in self.run_table.path]
        self.run_table["filenames_root"] = filenames_root
    def filter_available_runs(self):
        is_there  = np.array([os.path.isfile(f) for f in self.run_table.filenames_root], dtype=bool)
        self.run_table = self.run_table[is_there]
    def get_table(self):
        return self.run_table

DATA_DIR="/Users/shallmann/Desktop/rnog_field_data"
