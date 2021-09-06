import dash_html_components as html
import dash_core_components as dcc
import dash_table
import os
import dash
import argparse
import glob
import numpy as np
import random
import logging
from RNODataViewer.base.app import app
import webbrowser
import RNODataViewer.base.data_provider_root
import RNODataViewer.base.data_provider_nur
import RNODataViewer.file_list.file_list
import RNODataViewer.station_selection.station_selection
import RNODataViewer.trigger_rate.trigger_rate_uproot
from file_list.run_stats import RunStats
import astropy.time
import pandas as pd


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description="View RNO Data Set")
    argparser.add_argument('file_location', type=str, help="Path of folder", default="/Users/shallmann/Desktop/rnog_field_data")
    argparser.add_argument('--monitoring', action="store_true", help="if set, run as monitoring instance, <file_location> should be top level directory where data (i.e. the stationXX directories) sit")
    parsed_args = argparser.parse_args()

else:
    class PA:
        def __init__(self):
            self.file_location = "/Users/shallmann/Desktop/rnog_field_data"
            self.monitoring = True
    parsed_args = PA()
logging.info("starting online monitoring")


# get the input files
if not parsed_args.monitoring:
    filenames_root = glob.glob('{}/*.root'.format(parsed_args.file_location))
    filenames_root.sort()
    filenames_nur = glob.glob('{}/*.nur'.format(parsed_args.file_location))
    filenames_nur.sort()
    # overwrite in case no directory, but a file was provided explicitly...
    if os.path.isfile(parsed_args.file_location):
        if parsed_args.file_location.endswith(".root"):
            filenames_root = [parsed_args.file_location]
        if parsed_args.file_location.endswith(".nur"):
            filenames_nur = [parsed_args.file_location]
else:
    rs = RunStats(parsed_args.file_location)
    run_table = rs.get_table()
    filenames_root = run_table.filenames_root
    filenames_nur = []

RNODataViewer.base.data_provider_root.RNODataProviderRoot().set_filenames(filenames_root)
RNODataViewer.base.data_provider_nur.RNODataProvider().set_filenames(filenames_nur)

def get_slider_marks(ymin=2021, ymax=None, months = np.arange(1,13)):
    if ymax==None:
        ymax=astropy.time.Time.now().ymdhms[0]
    slider_marks = {}
    for y in range(ymin,ymax+1):
        for m in months:
            for d in range(32):
                try:
                    slider_marks[int(astropy.time.Time("{}-{}-{}".format(str(y).zfill(4), str(m).zfill(2), str(d).zfill(2)), format="iso").mjd)] = ""
                except:
                    continue
            for d in [1,15]:
                slider_marks[int(astropy.time.Time("{}-{}-{}".format(str(y).zfill(4), str(m).zfill(2), str(d).zfill(2)), format="iso").mjd)] = "{}-{}-{}".format(str(y).zfill(4), str(m).zfill(2), str(d).zfill(2))
    return slider_marks
slider_marks = get_slider_marks()

overview_layout = html.Div([
    RNODataViewer.station_selection.station_selection.layout,
    html.Div([html.Div('Time selector', style={'flex': '1'}),
                  dcc.RangeSlider(
                      id='time-selector',
                      min=min(run_table["mjd_first_event"]),
                      max=astropy.time.Time.now().mjd+1,
                      marks = slider_marks,
                      value=[astropy.time.Time.now().mjd - 1,
                          astropy.time.Time.now().mjd,
                      ],
                      step=0.01,
                      included=True
                  ),
                  ],style={'marginTop':"1%", "margin":"1%"}),
    html.Div([
        html.Div(id='output-container-range-slider', style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': "1%", 'marginRight': "1%"}),
        html.Div([
                RNODataViewer.file_list.file_list.layout
            ], style={'width': '55%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginLeft': "1%", 'marginRight': "1%"})]),

    html.Div([
        html.Div([
            RNODataViewer.trigger_rate.trigger_rate_uproot.layout
        ], className='flexi-element-1')
    ], className='flexi-box')
])



@app.callback(
    dash.dependencies.Output('output-container-range-slider', 'children'),
    [dash.dependencies.Input('time-selector', 'value'),
     dash.dependencies.Input('station-id-dropdown', 'value')])
def update_output(value, station_ids=[11,21,22]):
    t_start = value[0]
    t_end = value[1]
    print(len(run_table))
    selected = run_table[(np.array(run_table["mjd_first_event"])>t_start) & (np.array(run_table["mjd_last_event"])<t_end)]
    print(len(selected))
    RNODataViewer.base.data_provider_root.RNODataProviderRoot().set_filenames(selected.filenames_root)
    ###print(len(RNODataViewer.base.data_provider_root.RNODataProviderRoot().get_event_times_hdr(11)))
    return_strings = []
    for station in station_ids:
        runs_for_station = selected[selected.station==station].run
        if len(runs_for_station) == 0:
            runrange = [np.nan, np.nan]
        else:
            runrange = [min(runs_for_station), max(runs_for_station)]
        return_strings.append('{} - {}'.format(str(runrange[0]).rjust(6),str(runrange[1]).rjust(6)))
        #return_strings.append('Station {}: Run range: {} -- {}<br>'.format(str(station).rjust(3), str(runrange[0]).rjust(6),str(runrange[1]).rjust(6)))
    print(return_strings)
    retdata = pd.DataFrame({"Station": station_ids, "Selected Runs": return_strings})
    #return "".join(return_strings)
    return  dash_table.DataTable(
                            id='ddoutput-container-range-slider',
                            data=retdata.to_dict("records"),
                            columns=[{'id': x, 'name': x} for x in retdata.columns]
                )

if __name__ == '__main__':
    if int(dash.__version__.split('.')[0]) <= 1:
        if int(dash.__version__.split('.')[1]) < 0:
            print('WARNING: Dash version 0.39.0 or newer is required, you are running version {}. Please update.'.format(dash.__version__))
    port = 8087 #8080 is used by the EventBrowser also...
    webbrowser.open_new("http://localhost:{}".format(port))
    
    app.title = 'RNO Data Browser'
    app.run_server(debug=True, port=port)
