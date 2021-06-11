import RNODataViewer.base.data_provider_root
import RNODataViewer.base.data_provider_nur
import numpy as np
import astropy.time
from NuRadioReco.utilities import units
import NuRadioReco.framework.base_trace


def get_spectrogram_data_py(station_id, channel_ids):
    data_provider = RNODataViewer.base.data_provider_nur.RNODataProvider(channels=channel_ids)
    first_event = data_provider.get_first_event(station_id)
    if first_event is None:
        return False, None, None, None
    channel = first_event.get_station(station_id).get_channel(channel_ids[0])
    spectra = np.empty((len(channel_ids), data_provider.get_n_events(), channel.get_number_of_samples() // 2 + 1))
    times = []
    gps_times = np.zeros(data_provider.get_n_events())
    d_f = channel.get_frequencies()[2] - channel.get_frequencies()[1]
    for i_event, event in enumerate(data_provider.get_event_iterator()()):
        if station_id in event.get_station_ids():
            station = event.get_station(station_id)
            times.append(station.get_station_time().fits)
            gps_times[i_event] = station.get_station_time().gps
            for i_channel, channel_id in enumerate(channel_ids):
                spectra[i_channel, i_event] = np.abs(station.get_channel(channel_id).get_frequency_spectrum())
    sort_args = np.argsort(gps_times)
    times = np.array(times)
    return True, times[sort_args[::-1]], spectra[:, sort_args[::-1]], d_f


def get_spectrogram_data_root(station_id, channel_ids):
    data_provider = RNODataViewer.base.data_provider_root.RNODataProviderRoot(channels=channel_ids)
    first_event = data_provider.get_first_event(station_id)
    if first_event is None:
        return False, None, None, None
    channel = first_event.get_station(station_id).get_channel(channel_ids[0])
    spectra = {}  # np.empty((len(channel_ids), data_provider.get_n_events(), channel.get_number_of_samples() // 2 + 1))
    gps_times = []
    d_f = channel.get_frequencies()[2] - channel.get_frequencies()[1]
    data_provider.set_iterators()

    for headers, events in zip(data_provider.uproot_iterator_header, data_provider.uproot_iterator_data):
        mask_station = events['station_number'] == station_id
        gps_times.append(headers['readout_time'][mask_station])
        for i_channel, channel_id in enumerate(channel_ids):
            if i_channel not in spectra:
                spectra[i_channel] = []
            traces = np.array(events['radiant_data[24][2048]'][:, channel_id, :])[mask_station]

            def convert(data):
                tr = NuRadioReco.framework.base_trace.BaseTrace()
                tr.set_trace((data - np.mean(data)) * units.mV, sampling_rate=1. / (0.5 * units.ns))
                return np.abs(tr.get_frequency_spectrum())

            spec = np.apply_along_axis(convert, 1, np.array(traces))
            spectra[i_channel].append(spec)

    gps_times = np.concatenate(gps_times)
    for it in spectra:
        spectra[it] = np.concatenate(spectra[it])
    subplot_titles = []
    for channel_id in channel_ids:
        subplot_titles.append('Channel {}'.format(channel_id))
    sort_args = np.argsort(gps_times)
    times = astropy.time.Time(gps_times, format="unix", scale="utc").fits
    return True, times, spectra, d_f
