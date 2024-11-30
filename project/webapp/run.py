from app import create_app

import webbrowser

if __name__ == '__main__':
    
    # Istanziamento e Configurazione app
    app = create_app()
    
    # Apertura automatica della pagina
    # webbrowser.open(f"http://{app.config['NETWORK_SETTINGS']['IP_ADDRESS']}:{app.config['NETWORK_SETTINGS']['PORT_NUMBER']}")
    
    # Avvio del servizio
    app.run(
        app.config['NETWORK_SETTINGS']['IP_ADDRESS'],
        app.config['NETWORK_SETTINGS']['PORT_NUMBER'],
        debug=app.config['MODE_SETTINGS']['ENABLE_DEBUG']
    )