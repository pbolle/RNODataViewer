import RNODataViewer.base.data_provider
from RNODataViewer.base.app import app
import dash_html_components as html
from dash.dependencies import Input, Output

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
    [Input('file-list-reload-button', 'n_clicks')]
)
def update_file_list(n_clicks):
    data_provider = RNODataViewer.base.data_provider.RNODataProvider()
    filenames = data_provider.get_file_names()
    if filenames is None:
        return ''
    children = []
    for filename in filenames:
        children.append(
            html.Div('{}'.format(filename))
        )
    return children
