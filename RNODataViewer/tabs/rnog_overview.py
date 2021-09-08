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
from file_list.run_stats import RUN_TABLE #RunStats, DATA_DIR
import astropy.time
import pandas as pd


run_table = RUN_TABLE #rs.get_table()
print(len(run_table))

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


