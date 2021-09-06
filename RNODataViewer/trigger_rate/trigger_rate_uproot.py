import numpy as np
import itertools
#from NuRadioReco.eventbrowser.app import app
from RNODataViewer.base.app import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.subplots
import RNODataViewer.base.data_provider_root
import RNODataViewer.base.error_message
from NuRadioReco.utilities import units
from astropy.time import Time, TimeDelta
from NuRadioReco.framework.base_trace import BaseTrace
layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div('Event rate', style={'flex': '1'}),
                html.Div([
                    html.Button([
                        html.Div('', className='icon-cw')
                    ], id='triggeruproot-reload-button', className='btn btn-primary')
                ], style={'flex': 'none'})
            ], className='flexi-box')
        ], className='panel panel-heading'),
        html.Div([
            dcc.Graph(id='triggeruproot-plot')
        ], className='panel panel-body')
    ], className='panel panel-default')
])

@app.callback(
    Output('triggeruproot-plot', 'figure'),
    [Input('triggeruproot-reload-button', 'n_clicks')],
    [State('station-id-dropdown', 'value')]
)
def update_triggeruproot_plot(n_clicks, station_ids):
    BINWIDTH_SEC = 10*60
    if station_ids is None:
        return RNODataViewer.base.error_message.get_error_message('No Station selected')
    data_provider = RNODataViewer.base.data_provider_root.RNODataProviderRoot()
    
    #station_ids_found = []
    #for station_id in station_ids:
    #    first_event = data_provider.get_first_event(station_id)
    #    if first_event is not None:
    #        station_ids_found.append(station_id)
    #if len(station_ids_found)==0:
    #    return RNODataViewer.base.error_message.get_error_message('Stations {} not found in events'.format(list(station_ids)))
    plots = []
    subplot_titles = []


    # get the needed data:
    station_numbers = np.array([],dtype=int)
    trigger_times = np.array([])

    trigger_masks = {
            'rf_trigger' : np.array([],dtype=bool),
            'force_trigger': np.array([],dtype=bool),
            'pps_trigger': np.array([],dtype=bool),
            'ext_trigger': np.array([],dtype=bool),
            'radiant_trigger': np.array([],dtype=bool),
            'lt_trigger': np.array([],dtype=bool)
            }
    data_provider.set_iterators()
    for headers in data_provider.uproot_iterator_header:
        station_numbers = np.append(station_numbers, np.array(headers['station_number']))
        trigger_times = np.append(trigger_times, np.array(headers['readout_time']))
        for trigger_key in trigger_masks:
            trigger_masks[trigger_key] = np.append(trigger_masks[trigger_key], np.array(headers['trigger_info.'+trigger_key]))
    trigger_masks['total'] = np.ones_like(station_numbers, dtype=bool)

    for station_id in station_ids:        
        mask_station = station_numbers == station_id

        bins = np.arange(min(trigger_times), max(trigger_times)+BINWIDTH_SEC, BINWIDTH_SEC)
        bins_fits = Time(bins, format="unix", scale="utc").fits

        subplot_titles.append('Station {}'.format(station_id))
        bincenters = Time((bins[1:]+bins[:-1])/2., format="unix", scale="utc").fits

        for key in trigger_masks:# ["total"]: #trigger_masks
            contents, b = np.histogram(trigger_times[trigger_masks[key]&mask_station], bins)
            point_labels = None #contents
            if key=="total":
                visible = True
            else:
                visible='legendonly'
            plots.append(go.Scatter(
                x = bincenters,
                y = contents/(BINWIDTH_SEC),
                mode='lines+markers',
                name='Station: {}, Trigger: {}'.format(station_id, key),
                visible=visible,
                text=point_labels
            ))
    fig = go.Figure(plots)
    fig.update_layout(
          xaxis={'title': 'date'},
          yaxis={'title': 'Rate [Hz]'}
      )
    fig.update_yaxes(rangemode='tozero')
    return fig
