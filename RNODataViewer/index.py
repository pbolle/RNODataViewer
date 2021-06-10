
import dash_html_components as html
import dash
import argparse
import glob
from RNODataViewer.base.app import app
import RNODataViewer.base.data_provider_root
import RNODataViewer.base.data_provider_nur
import RNODataViewer.file_list.file_list
import RNODataViewer.station_selection.station_selection
import RNODataViewer.spectrogram.spectrogram
import RNODataViewer.noise_rms.noise_rms
import RNODataViewer.spectrogram.spectrogram_uproot
import RNODataViewer.trigger_rate.trigger_rate_uproot
argparser = argparse.ArgumentParser(description="View RNO Data Set")
argparser.add_argument('file_location', type=str, help="Path of folder")
parsed_args = argparser.parse_args()
filenames_root = glob.glob('{}/*.root'.format(parsed_args.file_location))
RNODataViewer.base.data_provider_root.RNODataProviderRoot().set_filenames(filenames_root)
filenames_nur = glob.glob('{}/*.nur'.format(parsed_args.file_location))
RNODataViewer.base.data_provider_nur.RNODataProvider().set_filenames(filenames_nur)


app.title = 'RNO Data Browser'
app.layout = html.Div([
    RNODataViewer.station_selection.station_selection.layout,
    html.Div([
        html.Div([
            html.Div([
                RNODataViewer.file_list.file_list.layout
            ], className='blocki-box')
        ], className='flexi-element-1'),
        html.Div([
            RNODataViewer.noise_rms.noise_rms.layout
        ], className='flexi-element-4')

    ], className='flexi-box'),
    html.Div([
        html.Div([
            RNODataViewer.spectrogram.spectrogram.layout
        ], className='flexi-element-1')
    ], className='flexi-box'),
    html.Div([
        html.Div([
            RNODataViewer.spectrogram.spectrogram_uproot.layout
        ], className='flexi-element-1')
    ], className='flexi-box'),
    html.Div([
        html.Div([
            RNODataViewer.trigger_rate.trigger_rate_uproot.layout
        ], className='flexi-element-1')
    ], className='flexi-box')
])

if __name__ == '__main__':
    if int(dash.__version__.split('.')[0]) <= 1:
        if int(dash.__version__.split('.')[1]) < 0:
            print('WARNING: Dash version 0.39.0 or newer is required, you are running version {}. Please update.'.format(dash.__version__))
    app.run_server(debug=True, port=8080)
