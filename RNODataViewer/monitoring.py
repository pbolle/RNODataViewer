#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import webbrowser
from RNODataViewer.base.app import app,server
app.config.suppress_callback_exceptions = True

import RNODataViewer.base.data_provider_root
import RNODataViewer.base.data_provider_nur
from file_list.run_stats import RunStats

from tabs import rnog_overview
from tabs import run_viewer
from tabs import event_viewer

import logging
from file_list.run_stats import RUN_TABLE #RunStats, DATA_DIR
import astropy.time
import pandas as pd
import sys, os
  
argparser = argparse.ArgumentParser(description="View RNO Data Set")
argparser.add_argument('--open-window', const=True, default=False, action='store_const',
                         help="Open the event display in a new browser tab on startup")
argparser.add_argument('--port', default=8080, help="Specify the port the event display will run on")
#argparser.add_argument('--monitoring', action="store_true", help="if set, run as monitoring instance, <file_location> should be top level directory where data (i.e. the stationXX directories) sit")
parsed_args = argparser.parse_args()
  
logging.info("starting online monitoring")

#rs = RunStats(DATA_DIR)
run_table = RUN_TABLE #rs.get_table()
filenames_root = run_table.filenames_root
filenames_nur = []
  
RNODataViewer.base.data_provider_root.RNODataProviderRoot().set_filenames(filenames_root)
RNODataViewer.base.data_provider_nur.RNODataProvider().set_filenames(filenames_nur)


app.layout = html.Div([
    html.Div([
        html.Img(src='./assets/rnog_logo_monogram_BlackTransparant.png', style={"float": "left", "width": "100px"}),
        html.H1('RNO-G Data Monitor')]),
    dcc.Tabs(
            [
                dcc.Tab(label= 'Overview', value= 'overview_tab'),
                dcc.Tab(label= 'Run Browser', value= 'runbrowser_tab'),
                dcc.Tab(label= 'Event Browser', value= 'eventbrowser_tab')
            ],
            value='overview_tab',
            id='tabs-example'
        ),
    html.Div(id='tabs-content-example')
    #dcc.Tabs([
    #    dcc.Tab(label= 'Overview', children=index_app_layout),
    #    dcc.Tab(label= 'Run Browser', children=run_viewer.run_viewer_layout),
    #    dcc.Tab(label= 'Event Browser', children=event_viewer.event_viewer_layout)
    #])
])

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'overview_tab':
        return rnog_overview.overview_layout
    elif tab == 'runbrowser_tab':
        return run_viewer.run_viewer_layout
    elif tab == 'eventbrowser_tab':
        return event_viewer.event_viewer_layout


if __name__ == '__main__':
    if int(dash.__version__.split('.')[0]) <= 1:
        if int(dash.__version__.split('.')[1]) < 0:
            print('WARNING: Dash version 0.39.0 or newer is required, you are running version {}.   Please update.'.format(dash.__version__))
    port = parsed_args.port
    if parsed_args.open_window:
        webbrowser.open_new("http://localhost:{}".format(port))
    app.run_server(debug=False, port=port)
