import RNODataViewer.base.data_provider_nur
import RNODataViewer.base.data_provider_root
from RNODataViewer.base.app import app
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

layout = html.Div([
    html.Div([
        html.Div([
            html.Div('File Names', style={'flex': '1'}),
            html.Div([
                html.Button([
                    html.Div('', className='icon-cw')
                ], id='file-list-reload-button', className='btn btn-primary')
            ], style={'flex': 'none'})
        ], className='flexi-box')
    ], className='panel panel-heading'),
    html.Div([
        html.Div('', id='file-list-display')
    ], className='panel panel-body', style={'max-height': '200px', 'overflow': 'scroll'})
], className='panel panel-default')


@app.callback(
    Output('file-list-display', 'children'),
    [Input('file-list-reload-button', 'n_clicks')],
    [State('file-type-dropdown', 'value')]
)
def update_file_list(n_clicks, file_type):
    if file_type == 'root':
        data_provider = RNODataViewer.base.data_provider_root.RNODataProviderRoot()
    else:
        data_provider = RNODataViewer.base.data_provider_nur.RNODataProvider()
    filenames = data_provider.get_file_names()
    if filenames is None:
        return ''
    children = []
    for filename in filenames:
        children.append(
            html.Div('{}'.format(filename))
        )
    return children
