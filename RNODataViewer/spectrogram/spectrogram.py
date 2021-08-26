import numpy as np
from RNODataViewer.base.app import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.subplots
import RNODataViewer.base.data_provider_nur
import RNODataViewer.base.error_message
import RNODataViewer.spectrogram.spectrogram_data
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


@app.callback(
    Output('spectrogram-plot', 'figure'),
    [Input('spectrogram-reload-button', 'n_clicks')],
    [State('station-id-dropdown', 'value'),
     State('channel-id-dropdown', 'value'),
     State('file-type-dropdown', 'value')]
)
def update_spectrogram_plot(n_clicks, station_id, channel_ids, file_type):
    if station_id is None:
        return RNODataViewer.base.error_message.get_error_message('No Station selected')
    if len(channel_ids) == 0:
        return RNODataViewer.base.error_message.get_error_message('No Channels selected')
    if file_type == 'nur':
        station_found, times, spectra, d_f = RNODataViewer.spectrogram.spectrogram_data.get_spectrogram_data_py(station_id, channel_ids)
    else:
        station_found, times, spectra, d_f = RNODataViewer.spectrogram.spectrogram_data.get_spectrogram_data_root(station_id, channel_ids)
    if not station_found:
        return RNODataViewer.base.error_message.get_error_message('Station {} not found in events'.format(station_id))
    subplot_titles = []
    for channel_id in channel_ids:
        subplot_titles.append('Channel {}'.format(channel_id))

    fig = plotly.subplots.make_subplots(
        cols=len(channel_ids),
        rows=1,
        subplot_titles=subplot_titles,
        x_title='Event',
        y_title='f [MHz]',
        shared_xaxes='all',
        shared_yaxes='all'
    )
    for i_channel, channel_id in enumerate(channel_ids):
        fig.add_trace(
            go.Heatmap(
                z=np.abs(spectra[i_channel].T) / units.mV,
                x=times,
                y0=0.0,
                dy=d_f / units.MHz,
                coloraxis='coloraxis',
                name='Ch.{}'.format(channel_id)
            ), 1, i_channel + 1
        )
    fig.update_layout(coloraxis_colorbar={'title': 'U [mV]'})
    fig.update_layout({"coloraxis_cmin": 0,
                       "coloraxis_cmax": 1e3})
    return fig
