import numpy as np
import itertools
from RNODataViewer.base.app import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.subplots
import RNODataViewer.base.data_provider
import RNODataViewer.base.error_message
from NuRadioReco.utilities import units
from astropy.time import Time
from NuRadioReco.framework.base_trace import BaseTrace
layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div('SpectrogramUproot', style={'flex': '1'}),
                html.Div([
                    html.Button([
                        html.Div('', className='icon-cw')
                    ], id='spectrogramuproot-reload-button', className='btn btn-primary')
                ], style={'flex': 'none'})
            ], className='flexi-box')
        ], className='panel panel-heading'),
        html.Div([
            dcc.Graph(id='spectrogramuproot-plot')
        ], className='panel panel-body')
    ], className='panel panel-default')
])

@app.callback(
    Output('spectrogramuproot-plot', 'figure'),
    [Input('spectrogramuproot-reload-button', 'n_clicks')],
    [State('station-id-dropdown', 'value'),
     State('channel-id-dropdown', 'value')]
)
def update_spectrogramuproot_plot(n_clicks, station_id, channel_ids):
    if station_id is None:
        return RNODataViewer.base.error_message.get_error_message('No Station selected')
    if len(channel_ids) == 0:
        return RNODataViewer.base.error_message.get_error_message('No Channels selected')
    data_provider = RNODataViewer.base.data_provider.RNODataProvider(channels=channel_ids)
    data_provider.set_iterators()
    first_event = data_provider.get_first_event(station_id)
    if first_event is None:
        return RNODataViewer.base.error_message.get_error_message('Station {} not found in events'.format(station_id))
    channel = first_event.get_station(station_id).get_channel(channel_ids[0])
    spectra = {}#np.empty((len(channel_ids), data_provider.get_n_events(), channel.get_number_of_samples() // 2 + 1))
    times = []
    gps_times = []
    d_f = channel.get_frequencies()[2] - channel.get_frequencies()[1]
    data_provider.set_iterators()

    for headers, events in zip(data_provider.uproot_iterator_header, data_provider.uproot_iterator_data):
        print(events['event_number'])
        mask_station = events['station_number'] == station_id
        print(len(mask_station))
        gps_times.append(headers['readout_time'][mask_station])
        for i_channel, channel_id in enumerate(channel_ids):
            if i_channel not in spectra:
                spectra[i_channel] = []
            traces = np.array(events['radiant_data[24][2048]'][:,channel_id,:])[mask_station]
            print(np.shape(traces))
            def convert(data):
                tr = BaseTrace()
                tr.set_trace((data-np.mean(data))*units.mV, sampling_rate=1./(0.5*units.ns))
                return np.abs(tr.get_frequency_spectrum())
            spec = np.apply_along_axis(convert, 1, np.array(traces))
            spectra[i_channel].append(spec)
    
    gps_times = np.concatenate(gps_times)
    for it in spectra:
        spectra[it]= np.concatenate(spectra[it])
    subplot_titles = []
    for channel_id in channel_ids:
        subplot_titles.append('Channel {}'.format(channel_id))
    sort_args = np.argsort(gps_times)
    times = Time(gps_times, format="unix", scale="utc").fits
    fig = plotly.subplots.make_subplots(
        cols=len(channel_ids),
        rows=1,
        subplot_titles=subplot_titles,
        x_title='Time',
        y_title='f [MHz]',
        shared_xaxes='all',
        shared_yaxes='all'
    )
    for i_channel, channel_id in enumerate(channel_ids):
        fig.add_trace(
            go.Heatmap(
                z=np.abs(np.array(spectra[i_channel]).T) / units.mV,
                x=times,#[sort_args[::-1]],
                y0 = 0,
                dy = d_f / units.MHz,
                coloraxis='coloraxis',
                name='Ch.{}'.format(channel_id)
            ), 1, i_channel + 1
        )
    fig.update_layout(coloraxis_colorbar={'title': 'U [mV]'})
    return fig
