import NuRadioReco.utilities.metaclasses
import six
from NuRadioReco.modules.io.rno_g.readRNOGData import readRNOGData
import uproot
import numpy as np


@six.add_metaclass(NuRadioReco.utilities.metaclasses.Singleton)
class RNODataProviderRoot:
    def __init__(self, channels=None):
        self.__filenames = None
        self.__event_io = None
        self.__channels = channels
        self.uproot_iterator_data = None
        self.uproot_iterator_header = None

    def set_filenames(self, filenames):
        self.__filenames = filenames
        self.__event_io = readRNOGData()
        self.__event_io.begin(filenames)
        self.__event_io.run(channels=self.__channels)

    def set_iterators(self):
        self.__event_io = readRNOGData()
        self.__event_io.begin(self.__filenames)
        self.uproot_iterator_header = self.__event_io.uproot_iterator_header
        self.uproot_iterator_data = self.__event_io.uproot_iterator_data
    
    def get_event_iterator(self):
        return self.__event_io.get_events

    def get_file_names(self):
        return self.__filenames

    def get_first_event(self, station_id):
        for event in self.__event_io.get_events():
            if station_id in event.get_station_ids():
                return event
        return None

    def get_n_events(self):
        return self.__event_io.get_n_events()

    def get_waveforms(self, station_id, channels):
        for filename in self.__filenames:
            file = uproot.open(filename)
            waveforms = file['waveforms']['radiant_data[24][2048]'].array(library='np')
            station_ids = file['waveforms']['station_number'].array(library='np')
            return waveforms[(station_ids == station_id), :, :][:, channels]

    def get_event_times(self, station_id):
        station_ids = np.array([], dtype=int)
        readout_times = np.array([], dtype=float)
        for filename in self.__filenames:
            file = uproot.open(filename)
            station_ids = np.append(station_ids, file['waveforms']['station_number'].array(library='np'))
            readout_times = np.append(readout_times, file['header']['readout_time'].array(library='np'))
        return readout_times[station_ids == station_id]

    def get_event_ids(self, station_id):
        station_ids = np.array([], dtype=int)
        event_ids = np.array([], dtype=float)
        for filename in self.__filenames:
            file = uproot.open(filename)
            station_ids = np.append(station_ids, file['waveforms']['station_number'].array(library='np'))
            event_ids = np.append(event_ids, file['waveforms']['event_number'].array(library='np'))
        return event_ids[station_ids == station_id]