from .app import create_app
import webbrowser, os

def start():
    
    # CURRENT WORKING DIRECTORY & SETTINGS FILE PATH
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    SETTINGS_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "core", "config", "webapp.json")
    
    # Creating the app
    app = create_app(config_file=SETTINGS_FILE_PATH)
    
    # Running
    app.run(
        app.config['NETWORK_SETTINGS']['IP_ADDRESS'],
        app.config['NETWORK_SETTINGS']['PORT_NUMBER'],
        debug=app.config['MODE_SETTINGS']['ENABLE_DEBUG'],
        use_reloader=app.config['MODE_SETTINGS']['ENABLE_RELOADER']
    )
    
if __name__ == '__main__':
    start()