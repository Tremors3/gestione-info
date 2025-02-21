import docker

class PostgresDB:
    CONTAINER_NAME = "graboid_rfc"

    @staticmethod
    def start():
        client = docker.from_env()
        
        try: 
            container = client.containers.get(__class__.CONTAINER_NAME)
        except docker.errors.NotFound:
            container = client.containers.run(
                environment=[
                    "POSTGRES_USER=postgres",
                    "POSTGRES_PASSWORD=postgres",
                    "POSTGRES_DB=graboid_rfc"],
                ports={"5432/tcp":('127.0.0.1', 55432)},
                name=__class__.CONTAINER_NAME,
                image='postgres',
                detach=True
            )
        else:
            container.start()
    
    @staticmethod
    def stop():
        client = docker.from_env()
        try:
            container = client.containers.get(__class__.CONTAINER_NAME)
        except:
            print("Container non trovato.")
        else:
            container.stop()

    @staticmethod
    def delete():
        client = docker.from_env()
        try:
            container = client.containers.get(__class__.CONTAINER_NAME)
        except:
            print("Container non trovato.")
        else:
            container.remove()

if __name__ == "__main__":
    cont = PostgresDB()
    cont.stop()
    cont.delete()
    cont.start()
