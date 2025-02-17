import pg8000, os, json

from alive_progress import alive_bar
from alive_progress.animations import bar_factory
_bar = bar_factory("▁▂▃▅▆▇", tip="", background=" ", borders=("|","|"))


class MyPostgres:
     
    # CURRENT WORKING DIRECTORY & FILE PATHS
    CURRENT_FILE_PATH = os.path.dirname(os.path.realpath(__file__))
    CURRENT_WORKING_DIRECTORY = os.path.abspath(os.getcwd())
    
    # INDEX & DATASET DIRECTORY PATHS
    DATASET_FILE_PATH = os.path.join(CURRENT_WORKING_DIRECTORY, "project", "searchengine", "dataset", "dataset.json")
    
    @staticmethod
    def __cursor():
        conn = pg8000.connect(
            database="graboid_rfc",
            user="postgres",
            password="postgres",
            host="127.0.0.1",
            port=55432
        )
        return conn.cursor()
    
    @staticmethod
    def _initialize_table():
        cursor = __class__.__cursor()
        cursor.execute(
            'DROP TABLE IF EXISTS dataset;\
            CREATE TABLE dataset (\
                id integer PRIMARY KEY,\
                files text[],\
                title text,\
                authors text[],\
                date date,\
                more_info text,\
                status text,\
                abstract text,\
                keywords text[],\
                content text\
             );\
             COMMIT;'
        )
    
    @staticmethod
    def __sanitize(s):
        s = s.replace('\\','\\\\')
        s = s.replace("'","\\'")
        s = s.replace('"','\\"')
        return s
    
    @staticmethod
    def __array_to_string(arr):
        return "ARRAY[E'" + "',E'".join(map(lambda x: __class__.__sanitize(x), arr)) + "']"
    

    # @staticmethod
    # def _populate_table():
        
    #     cursor = __class__.__cursor()
        
    #     with open(__class__.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
    #         documents = json.load(f)

    #     with alive_bar(len(documents), title=f"Popolamento del database di PostgreSQL", spinner="waves", bar=_bar) as b:
    #         for doc in documents:
    #             b()
    #             id    = doc["Number"]
    #             files     = __class__.__array_to_string(doc["Files"])
    #             title     = __class__.__sanitize(doc["Title"])
    #             authors   = __class__.__array_to_string(doc["Authors"])
    #             date      = doc["Date"]
    #             more_info = __class__.__sanitize(doc["More Info"])
    #             status    = doc["Status"]
    #             abstract  = __class__.__sanitize(doc["Abstract"])
    #             keywords  = __class__.__array_to_string(doc["Keywords"])
    #             content   = __class__.__sanitize(doc["Content"])

    #             query = f"INSERT INTO dataset (id, files, title, authors, date, more_info, status, abstract, keywords, content)\
    #                     VALUES ('{id}', {files}, E'{title}', {authors}, to_date('{date}', 'YYYY-MM'), E'{more_info}', '{status}', E'{abstract}',  {keywords}, E'{content}');"
                
    #             cursor.execute(query)
    #     cursor.execute("COMMIT;")

    @staticmethod
    def _populate_table(block_size: int = 1):
        """Popola la tabella con il dataset."""
        cursor = __class__.__cursor()
        
        with open(__class__.DATASET_FILE_PATH, mode="r", encoding='utf-8') as f:
            documents = json.load(f)
        
        insert_query = """
            INSERT INTO dataset (id, files, title, authors, date, more_info, status, abstract, keywords, content)
            VALUES ('{}', {}, E'{}', {}, to_date('{}', 'YYYY-MM'), E'{}', '{}', E'{}',  {}, E'{}');
        """
        
        try:
            
            with alive_bar(len(documents), title="Popolamento del database di PostgreSQL", spinner="waves", bar=_bar) as bar:

                for idx, doc in enumerate(documents, start=1):
                    
                    bar() # Progressing the bar
                    
                    id_ = doc["Number"]
                    files = __class__.__array_to_string(doc["Files"])
                    title = __class__.__sanitize(doc["Title"])
                    authors = __class__.__array_to_string(doc["Authors"])
                    date = doc["Date"]
                    more_info = __class__.__sanitize(doc["More Info"])
                    status = doc["Status"]
                    abstract = __class__.__sanitize(doc["Abstract"])
                    keywords = __class__.__array_to_string(doc["Keywords"])
                    content = __class__.__sanitize(doc["Content"])

                    cursor.execute(insert_query.format(
                        id_, files, title, authors, date, more_info, status, abstract, keywords, content
                    ))

                    if idx % block_size == 0: # default is 1000
                        cursor.execute('COMMIT;')

                cursor.execute("COMMIT;")
                print("Popolamento del database completato.")
                
        except Exception as e:
            #self.conn.rollback()
            print(f"Errore durante il popolamento del database: {e}")
            raise

    @staticmethod
    def create_indexes():
        cursor = __class__.__cursor()
        query = "CREATE INDEX content_idx ON dataset USING GIN (to_tsvector('english', content)); COMMIT;"
        cursor.execute(query)

    @staticmethod
    def test_index():
        cursor = __class__.__cursor()
        query = "SELECT id, ts_rank_cd(to_tsvector(content), query) AS rank FROM dataset, to_tsquery('QUIC & Protocol') query WHERE query @@ to_tsvector(content) ORDER BY rank DESC LIMIT 10;"
        results = cursor.execute(query)
        print(results.fetchall())

if __name__ == "__main__":
    my = MyPostgres()
    my._initialize_table()
    my._populate_table()
    my.create_indexes()
    #my.test_index()






    # def _populate_table(self, block_size: int = 1):
    #     """Popola la tabella con il dataset."""
    #     cursor = self._get_cursor()
    #     documents = __class__.__get_documents()
        
    #     insert_query = """
    #         INSERT INTO dataset (id, files, title, authors, date, more_info, status, abstract, keywords, content)
    #         VALUES (%s, %s, E'%s', %s, to_date('%s', 'YYYY-MM'), E'%s', '%s', E'%s', %s, E'%s');
    #     """
        
    #     try:
            
    #         with alive_bar(len(documents), title="Popolamento del database di PostgreSQL", spinner="waves", bar=_bar) as bar:
    #             insert_values = []
                
    #             for idx, doc in enumerate(documents, start=1):
                    
    #                 bar() # Progressing the bar
                    
    #                 id_ = doc["Number"]
    #                 files = __class__.__array_to_string(doc["Files"])
    #                 title = __class__.__sanitize(doc["Title"])
    #                 authors = __class__.__array_to_string(doc["Authors"])
    #                 date = doc["Date"]
    #                 more_info = __class__.__sanitize(doc["More Info"])
    #                 status = doc["Status"]
    #                 abstract = __class__.__sanitize(doc["Abstract"])
    #                 keywords = __class__.__array_to_string(doc["Keywords"])
    #                 content = __class__.__sanitize(doc["Content"])
                    
    #                 print(insert_query.replace("%s", "{}").format(
    #                     id_, files, title, authors, date, more_info, status, abstract, keywords, content
    #                 ))
                    
    #                 insert_values.append((
    #                     id_, files, title, authors, date, more_info, status, abstract, keywords, content
    #                 ))

    #                 if len(insert_values) >= block_size: # default is 1000
    #                     cursor.executemany(insert_query, insert_values)
    #                     insert_values = []
                
    #             if insert_values:
    #                 cursor.executemany(insert_query, insert_values)
    #                 insert_values = []

    #             self.conn.commit()
    #             print("Popolamento del database completato.")
                
    #     except Exception as e:
    #         self.conn.rollback()
    #         print(f"Errore durante il popolamento del database: {e}")
    #         raise








