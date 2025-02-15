from .app import create_app

import webbrowser

def start():
    
    app = create_app()
    
    app.run(
        app.config['NETWORK_SETTINGS']['IP_ADDRESS'],
        app.config['NETWORK_SETTINGS']['PORT_NUMBER'],
        debug=app.config['MODE_SETTINGS']['ENABLE_DEBUG'],
        use_reloader=app.config['MODE_SETTINGS']['ENABLE_RELOADER']
    )
    
if __name__ == '__main__':
    start()