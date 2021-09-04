from NuRadioReco.eventbrowser.app import app
#from RNODataViewer.base.app import app
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
                        {'label': 'waveforms', 'value': 'combined'},
                        {'label': 'headers', 'value': 'headers'}
                    ],
                    value='combined'
                )
            ], className='option-select')
        ], className='option-set'),
    html.Div([
        html.Div('Station ID', className='option-label'),
        html.Div([
            dcc.Dropdown(
                id='station-id-dropdown',
                options=station_entries,
                value=[11,21,22],
                multi=True
            )
        ], className='option-select')
    ], className='option-set')#,
    #html.Div([
    #    html.Div('Channel IDs', className='option-label'),
    #    html.Div([
    #        dcc.Dropdown(
    #            id='channel-id-dropdown',
    #            options=channel_entries,
    #            value=[],
    #            multi=True
    #        )
    #    ], className='option-select')
    #], className='option-set')
], className='input-group')

layout_run_browser = html.Div([
      html.Div([
              html.Div('File Type', className='option-label'),
              html.Div([
                  dcc.Dropdown(
                      id='file-type-dropdown',
                      options=[
                          {'label': 'ROOT', 'value': 'combined'},
                          {'label': 'headers', 'value': 'headers'}
                      #    {'label': '.nur', 'value': 'nur'}
                      ],
                      value='combined'
                  )
              ], className='option-select')
          ], className='option-set', style={'width': '20%', 'display': 'inline-block'}),
      html.Div([
          html.Div('Station ID', className='option-label'),
          html.Div([
              dcc.Dropdown(
                  id='station-id-dropdown',
                  options=station_entries,
                  value=22,
                  multi=False
              )
          ], className='option-select')
      ], className='option-set', style={'width': '20%', 'display': 'inline-block'}),
      html.Div([
          html.Div('Channel IDs', className='option-label'),
          html.Div([
              dcc.Dropdown(
                  id='channel-id-dropdown',
                  options=channel_entries,
                  value=[1],
                  multi=True
              )
          ], className='option-select')
          ], className='option-set', style={'width': '58%','display': 'inline-block'})
  ], className='input-group', style={'width': '100%','display': 'inline-block'})
