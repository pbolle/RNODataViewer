import NuRadioReco.utilities.metaclasses
import six
from NuRadioReco.modules.io.rno_g.readRNOGData import readRNOGData


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
