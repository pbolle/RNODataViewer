import dash_html_components as html
import os
import dash
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
#from RNODataViewer.base.app import app
from NuRadioReco.eventbrowser.app import app
import webbrowser
import RNODataViewer.base.data_provider_root
import RNODataViewer.base.data_provider_nur
import RNODataViewer.file_list.file_list
import RNODataViewer.station_selection.station_selection
import RNODataViewer.spectrogram.spectrogram
import RNODataViewer.noise_rms.noise_rms
#import RNODataViewer.trigger_rate.trigger_rate_uproot
from file_list.run_stats import DATA_DIR, RunStats
import numpy as np

data_provider_run = RNODataViewer.base.data_provider_root.RNODataProviderRoot()


##app.title = 'RNO Data Browser'
run_viewer_layout = html.Div([
    html.Div([
        RNODataViewer.station_selection.station_selection.layout_run_browser,
        html.Div([
            html.Div('Selected runs', className='option-label'),
            dcc.Dropdown(id='file-name-dropdown',
                options=[],
                value=[],
                multi=True,
                className='custom-dropdown')]),
        html.Div([
            html.Button('open file', id='btn-open-file', className='btn btn-default')
            ], className='input-group-btn'),
            ], className='input-group', style={"width":"50%"}),
    html.Div([
        html.Div([
            RNODataViewer.noise_rms.noise_rms.layout
        ], className='flexi-element-4')

    ], className='flexi-box'),
    html.Div([
        html.Div([
            RNODataViewer.spectrogram.spectrogram.layout
        ], className='flexi-element-1')
    ], className='flexi-box')
])

@app.callback(Output('file-name-dropdown', 'options'),
              [Input('station-id-dropdown', 'value')])
def set_filename_dropdown(stations , folder=DATA_DIR):
        print("here")
        rs = RunStats(folder)
        run_table = rs.get_table()
        station_mask = np.array([np.isin(s, stations) for s in run_table.station], dtype=bool)
        run_table = run_table[station_mask]
        filtered_names = list(run_table.filenames_root)
        data_provider_run.set_filenames(filtered_names[:10])
        rrr =  [{'label': "Station {}, Run {}".format(row.station, row.run), 'value': row.filenames_root} for index, row in run_table.iterrows()]

        return rrr
#    #return [{'label': ll.split('/')[-1], 'value': ll} for ll in sorted(glob.glob(os.path.join(folder, '*.root*')))]
#      #else:
#    #    return [{'label': ll.split('/')[-1], 'value': ll} for ll in sorted(glob.glob(os.path.join(folder, '*.nur*')))]
