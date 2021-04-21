
import dash_html_components as html
import dash
import argparse
import glob
from RNODataViewer.base.app import app
import RNODataViewer.base.data_provider
import RNODataViewer.file_list.file_list

argparser = argparse.ArgumentParser(description="View RNO Data Set")
argparser.add_argument('file_location', type=str, help="Path of folder")
parsed_args = argparser.parse_args()
filenames = glob.glob('{}/*.nur'.format(parsed_args.file_location))
RNODataViewer.base.data_provider.RNODataProvider().set_filenames(filenames)


app.title = 'RNO Data Browser'
app.layout = html.Div([
    RNODataViewer.file_list.file_list.layout
])

if __name__ == '__main__':
    if int(dash.__version__.split('.')[0]) <= 1:
        if int(dash.__version__.split('.')[1]) < 0:
            print('WARNING: Dash version 0.39.0 or newer is required, you are running version {}. Please update.'.format(dash.__version__))
    app.run_server(debug=False, port=8080)
