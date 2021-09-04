#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from tabs import run_viewer
from tabs import event_viewer
from tabs import rnog_overview
from tabs.rnog_overview import *
from tabs.event_viewer import *
from tabs.run_viewer import *

#from RNODataViewer.base.app import app
from NuRadioReco.eventbrowser.app import app
app.config.suppress_callback_exceptions = True

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
            value='tab-1-example',
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
    port = 8087 # is used by the EventBrowser also...
    webbrowser.open_new("http://localhost:{}".format(port))
    app.run_server(debug=True, port=port)
