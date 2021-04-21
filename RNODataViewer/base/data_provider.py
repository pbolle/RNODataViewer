import NuRadioReco.modules.io.NuRadioRecoio
import NuRadioReco.utilities.metaclasses
import six

@six.add_metaclass(NuRadioReco.utilities.metaclasses.Singleton)
class RNODataProvider():
    def __init__(self):
        self.__filenames = None
        self.__event_io = None

    def set_filenames(self, filenames):
        self.__filenames = filenames
        self.__event_io = NuRadioReco.modules.io.NuRadioRecoio.NuRadioRecoio(filenames)

    def get_event_iterator(self):
        return self.__event_io.get_events

    def get_file_names(self):
        return self.__filenames