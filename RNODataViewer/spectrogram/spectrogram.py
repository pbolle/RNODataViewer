import numpy as np
from RNODataViewer.base.app import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.subplots
import plotly.express
import RNODataViewer.base.data_provider
from NuRadioReco.utilities import units

layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div('Spectrogram', style={'flex': '1'}),
                html.Div([
                    html.Button([
                        html.Div('', className='icon-cw')
                    ], id='spectrogram-reload-button', className='btn btn-primary')
                ], style={'flex': 'none'})
            ], className='flexi-box')
        ], className='panel panel-heading'),
        html.Div([
            dcc.Graph(id='spectrogram-plot')
        ], className='panel panel-body')
    ], className='panel panel-default')
])

empty_message = {
    'xaxis': {'visible': False},
    'yaxis': {'visible': False},
    'annotations': [{
        'xref': 'paper',
        'yref': 'paper',
        'showarrow': False,
        'font': {'size': 28}
    }]
}


@app.callback(
    Output('spectrogram-plot', 'figure'),
    [Input('spectrogram-reload-button', 'n_clicks')],
    [State('station-id-dropdown', 'value'),
     State('channel-id-dropdown', 'value')]
)
def update_spectrogram_plot(n_clicks, station_id, channel_ids):
    if station_id is None:
        msg = {'layout': empty_message}
        msg['layout']['annotations'][0]['text'] = 'No Station selected'
        return msg
    if len(channel_ids) == 0:
        msg = {'layout': empty_message}
        msg['layout']['annotations'][0]['text'] = 'No Channels selected'
        return msg
    data_provider = RNODataViewer.base.data_provider.RNODataProvider()
    first_event = data_provider.get_first_event(station_id)
    if first_event is None:
        msg = {'layout': empty_message}
        msg['layout']['annotations'][0]['text'] = 'Station {} not found in events'.format(station_id)
        return msg
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
    subplot_titles = []
    for channel_id in channel_ids:
        subplot_titles.append('Channel {}'.format(channel_id))
    sort_args = np.argsort(gps_times)
    times = np.array(times)
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
                z=np.abs(spectra[i_channel, sort_args[::-1]].T) / units.mV,
                x=times[sort_args[::-1]],
                y0 = 0,
                dy = d_f / units.MHz,
                coloraxis='coloraxis',
                name='Ch.{}'.format(channel_id)
            ), 1, i_channel + 1
        )
    fig.update_layout(coloraxis_colorbar={'title': 'U [mV]'})
    return fig
