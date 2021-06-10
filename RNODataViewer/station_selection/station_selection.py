from RNODataViewer.base.app import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from RNODataViewer.station_selection.station_list import station_entries, channel_entries


layout = html.Div([
    html.Div([
            html.Div('File Type', className='option-label'),
            html.Div([
                dcc.Dropdown(
                    id='file-type-dropdown',
                    options=[
                        {'label': 'ROOT', 'value': 'root'},
                        {'label': '.nur', 'value': 'nur'}
                    ],
                    value='root'
                )
            ], className='option-select')
        ], className='option-set'),
    html.Div([
        html.Div('Station ID', className='option-label'),
        html.Div([
            dcc.Dropdown(
                id='station-id-dropdown',
                options=station_entries,
                value=None,
                multi=False
            )
        ], className='option-select')
    ], className='option-set'),
    html.Div([
        html.Div('Channel IDs', className='option-label'),
        html.Div([
            dcc.Dropdown(
                id='channel-id-dropdown',
                options=channel_entries,
                value=[],
                multi=True
            )
        ], className='option-select')
    ], className='option-set')
], className='input-group')
