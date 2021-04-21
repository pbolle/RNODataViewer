def get_error_message(message):
    return {'layout': {
        'xaxis': {'visible': False},
        'yaxis': {'visible': False},
        'annotations': [{
            'text': message,
            'xref': 'paper',
            'yref': 'paper',
            'showarrow': False,
            'font': {'size': 28}
        }]
    }}
