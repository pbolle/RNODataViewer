import numpy as np
import NuRadioReco.framework.event
import NuRadioReco.framework.station
import NuRadioReco.framework.channel
import NuRadioReco.modules.io.eventWriter
from NuRadioReco.utilities import units
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '--n_events',
    type=int,
    default=1000,
    help='Number of events to create'
)
parser.add_argument(
    '--filename',
    type=str,
    default='dummy_file.nur',
    help='Name of the output file'
)
parser.add_argument(
    '--station_id',
    type=int,
    default=11,
    help='ID of the station'
)
parser.add_argument(
    '--n_samples',
    type=int,
    default=512,
    help='Number of samples per channel trace'
)
parser.add_argument(
    '--events_per_file',
    type=int,
    default=100,
    help='Number of events to be written into the same file'
)
args = parser.parse_args()

event_writer = NuRadioReco.modules.io.eventWriter.eventWriter()
event_writer.begin(args.filename, events_per_file=args.events_per_file)

for i in range(args.n_events):
    event = NuRadioReco.framework.event.Event(0, i)
    station = NuRadioReco.framework.station.Station(args.station_id)
    for i_channel in range(10):
        channel = NuRadioReco.framework.channel.Channel(i_channel)
        channel.set_trace(np.random.normal(0, 1.e-3, args.n_samples), 1.5 * units.GHz)
        station.add_channel(channel)
    event.set_station(station)
    event_writer.run(event)