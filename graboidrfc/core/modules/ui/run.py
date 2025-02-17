# Altri import
import webbrowser, os
from .app import create_app

# Import moduli di progetto
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

def start():
    
    # PACKAGE DYNAMIC FOLDER & SETTING FILE PATH
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    SETTINGS_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "config", "webapp.json")
    
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