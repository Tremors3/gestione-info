import docker

from core.modules.utils.metaclasses import Singleton

class DockerPG(metaclass=Singleton):

    def __init__(self,
            container_name:str="graboid_rfc", 
            db_user:str="postgres", 
            db_password:str="postgres", 
            db_name:str="graboid_rfc", 
            local_port:int=55432):
        
        # Client from env
        self.client = docker.from_env()
        
        # Container parameters
        self.container_name = container_name
        self.db_password = db_password
        self.local_port = local_port
        self.db_user = db_user
        self.db_name = db_name
        
        # Container variables
        self.image = 'postgres'
        self.local_address = '127.0.0.1'
        self.port = 5432
        
        try:
            # Getting the container
            self.container = self.client.containers.get(self.container_name)
        except docker.errors.NotFound:
            # Creating the container
            self.container = self.__get_new_container()
    
    # PRIVATE METHODS
    
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