import docker, json, os

from graboidrfc.core.modules.utils.metaclasses import Singleton
from graboidrfc.core.modules.utils.dynpath import get_dynamic_package_path

class DockerPG(metaclass=Singleton):

    # CURRENT WORKING DIRECTORY & FILE PATHS
    DYNAMIC_PACKAGE_PATH = get_dynamic_package_path()
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    
    # SETTINGS FILE PATHS
    SETTINGS_FILE_PATH = os.path.join(DYNAMIC_PACKAGE_PATH, "core", "config", "docker.json")

    def __init__(self):
        
        # Client from env
        self.client = docker.from_env()
        
        # Lettura delle impostazioni
        settings = __class__.__get_settings()
        
        # Mapping impostazioni a parametri d'istanza
        self.__remap_settings(settings)
        
        try:
            # Getting the container
            self.container = self.client.containers.get(self.container_name)
        except docker.errors.NotFound:
            # Creating the container
            self.container = self.__get_new_container()
    
    # PRIVATE METHODS
    
    def __remap_settings(self, settings):
        """Funzione che mappa le impostazioni a variabili d'istanza."""
        try:
        
            # Network Settings
            self.local_port = settings["NETWORK_SETTINGS"]["PORT_NUMBER"]
            self.local_address = settings["NETWORK_SETTINGS"]["IP_ADDRESS"]
            
            # Container Settings
            self.image = settings["CONTAINER_OPTIONS"]["IMAGE"]
            self.port = settings["CONTAINER_OPTIONS"]["INTERNAL_PORT_NUMBER"]
            self.container_name = settings["CONTAINER_OPTIONS"]["CONTAINER_NAME"]
            
            # Database Settings
            self.db_password = settings["DATABASE_SETTINGS"]["DB_PASSWORD"]
            self.db_user = settings["DATABASE_SETTINGS"]["DB_USER"]
            self.db_name = settings["DATABASE_SETTINGS"]["DB_NAME"]

        except Exception as e:
            raise ValueError(f"Impossibile leggere il file di impostazione \'{__class__.SETTINGS_FILE_PATH}\': {e}")
    
    @staticmethod
    def __get_settings(fp:str=None):
        """Funzione che legge e restutiusce le impostazioni in formato JSON."""
        
        # Ottenimento del percorso del file delle impostazioni
        FILE_PATH = fp if fp else __class__.SETTINGS_FILE_PATH
        
        # Controllo se il file delle impostazioni esiste
        if not os.path.isfile(FILE_PATH):
            raise FileNotFoundError(f"Il file di configurazione di docker non è stato trovato al seguente percorso: \'{FILE_PATH}\'.")

        # Lettura e restituzione delle impostazioni in formato JSON
        with open(FILE_PATH, mode="r", encoding='utf-8') as f:
            return json.load(f)
    
    def __get_new_container(self):
        """Crea e ritorna un nuovo container."""
        return self.client.containers.create(
            environment=[
                f"POSTGRES_USER={self.db_user}",
                f"POSTGRES_PASSWORD={self.db_password}",
                f"POSTGRES_DB={self.db_name}"],
            ports={f"{self.port}/tcp":(self.local_address, self.local_port)},
            name=self.container_name,
            image=self.image,
            detach=True
        )
    
    # API METHODS
    
    def is_docker_running(self) -> bool:
        """Verifica se Docker è in esecuzione."""
        try:
            self.client.ping()
            return True
        except docker.errors.APIError:
            return False
    
    def is_running(self) -> bool:
        """Verifica se il container è in esecuzione."""
        if self.container:
            return (self.container.status == 'running')
        return False
    
    def create(self):
        """Crea il container, se non esiste già."""
        if not self.container:
            self.container = self.__get_new_container()
    
    def recreate(self):
        """Cancella il container esistente e ne crea uno nuovo."""
        
        if self.container:
            self.container.stop()
            self.container.remove()
        
        self.container = self.__get_new_container()
    
    def start(self):
        """Avvia il container se non è in esecuzione."""
        if self.container and not self.is_running():
            self.container.start()
    
    def stop(self):
        """Ferma il container se è in esecuzione."""
        if self.container and self.is_running():
            self.container.stop()
    
    def delete(self):
        """Rimuove il container se esiste."""
        if self.container:
            self.container.stop()
            self.container.remove()
            self.container = None