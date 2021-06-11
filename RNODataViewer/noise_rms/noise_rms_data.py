import RNODataViewer.base.data_provider_nur
import RNODataViewer.base.data_provider_root
from NuRadioReco.framework.parameters import channelParameters as chp
import numpy as np


def get_noise_rms_data_nur(station_id, channel_ids):
    data_provider = RNODataViewer.base.data_provider_nur.RNODataProvider(channels=channel_ids)
    first_event = data_provider.get_first_event(station_id)
    if first_event is None:
        return False, None, None, None
    noise_rms = np.zeros((len(channel_ids), data_provider.get_n_events()))
    times = []
    point_labels = []
    for i_event, event in enumerate(data_provider.get_event_iterator()()):
        point_labels.append('Event {}, {}'.format(event.get_run_number(), event.get_id()))
        if station_id in event.get_station_ids():
            station = event.get_station(station_id)
            times.append(station.get_station_time().fits)
            for i_channel, channel_id in enumerate(channel_ids):
                noise_rms[i_channel, i_event] = station.get_channel(channel_id).get_parameter(chp.noise_rms)
    return True, times, noise_rms, point_labels


def get_noise_rms_data_root(station_id, channel_ids):
    data_provider = RNODataViewer.base.data_provider_root.RNODataProviderRoot(channels=channel_ids)
    times = data_provider.get_event_times(station_id)
    waveforms = data_provider.get_waveforms(station_id, channel_ids).astype(float)
    waveforms -= np.mean(waveforms, axis=2, keepdims=True)
    noise_rms = np.sqrt(np.mean(waveforms**2, axis=2))
    event_ids = data_provider.get_event_ids(station_id)
    return True, times, noise_rms.T, event_ids
