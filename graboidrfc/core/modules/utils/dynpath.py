import pkg_resources, os

def get_dynamic_package_path(distname: str = None, default: str = "graboidrfc"):
    """Funzione che restituisce il percorso del pacchetto dinamicamente."""
    
    # Imposta il nome del pacchetto
    distname = distname if distname else default
    
    try:
        # Verifica se il pacchetto è installato tramite setuptools
        pkg_resources.get_distribution(distname)
        
        # Ottieni il percorso del pacchetto installato, compatibile con il venv
        current_file_path = os.path.join(os.path.dirname(pkg_resources.resource_filename(distname, "")), distname)

    except pkg_resources.DistributionNotFound:
        
        # Se il pacchetto non è trovato, usa la directory di lavoro corrente
        current_file_path = os.path.abspath(os.getcwd())
    
    return current_file_path