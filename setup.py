from setuptools import setup, find_packages
import json, os, re

def get_current_file_path():
    return os.path.dirname(os.path.abspath(__file__))

def get_requires(req_file: str = None):
    
    req_file = req_file or "requirements.txt"
    req_file_path = os.path.join(get_current_file_path(), req_file)
    
    if not os.path.exists(req_file_path):
        raise FileNotFoundError(f"File delle dipendenze non trovato al seguende percorso: \'{req_file_path}\'.")
    
    try:
        with open(req_file_path, mode="r", encoding='utf-8') as fd:
            return [ dip for line in fd.readlines() if (dip := line.strip()) and not dip.startswith('#') ]
        
    except Exception as e:
        raise Exception(f"Errore durante la lettura del file delle dipendenze al seguente percorso: \'{req_file_path}\': {e}")

def prepare_manifest(package_folder: str, manifest_file: str = None):
    
    manifest_file = manifest_file or "MANIFEST.in"
    manifest_file_path = os.path.join(get_current_file_path(), manifest_file)
    include_string = f"recursive-include {package_folder} *"
    
    try:
        if os.path.exists(manifest_file_path):
            with open(manifest_file_path, mode="r", encoding='utf-8') as fd:
                if include_string in fd.read(): return
        
        with open(manifest_file_path, mode="w", encoding='utf-8') as fd:
            fd.write(include_string)
    
    except Exception as e:
        raise Exception(f"Errore durante la creazione del manifest al seguente percorso: \'{manifest_file_path}\': {e}")

def load_config_file(config_file: str = None) -> dict:

    config_file = config_file or "setup.json"
    config_file_path = os.path.join(get_current_file_path(), config_file)
    
    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"File di configurazione non trovato al seguende percorso: \'{config_file_path}\'.")
    
    try:
        with open(config_file_path, mode="r", encoding='utf-8') as fd:
            return json.load(fd)
            
    except Exception as e:
        raise Exception(f"Errore durante la lettura del file delle impostazioni al seguente percorso: \'{config_file_path}\': {e}")

def prepare_config_file(config: dict) -> tuple[dict, str]:

    try:
        metadata = config["metadata"]
        dependencies = config["dependencies"]
        
        return ({
            
            "name": metadata["name"],
            "version": metadata["version"],
            "python_requires": metadata["python_version"],
            "packages": find_packages(include=[
                metadata['package_folder'],
                f"{metadata['package_folder']}.*"
            ]),
            "install_requires": get_requires(dependencies['requirements_file']),
            "entry_points": { "console_scripts": [
                f"{metadata['console_script']}={metadata['package_folder']}.{metadata['script']}:{metadata['function']}"
            ]},
            #"author": metadata['author'],
            #"author_email": metadata['author_email'],
            "url": metadata['url'],
            "license": metadata['license'],
            "include_package_data": metadata['include_package_data'],
            "classifiers": metadata['classifiers']
            
        }, metadata["package_folder"])
        
    except (KeyError, Exception) as e:
        raise KeyError(f"Chiave mancante nel file di configurazione: {e}")

def get_configs(config_file: str = None) -> tuple[dict, str]:
    config = load_config_file(config_file)
    return prepare_config_file(config)

if __name__ == '__main__':
    
    config_file = "setup.json"
    
    configs, package = get_configs(config_file)
    
    prepare_manifest(package)

    setup(**configs)