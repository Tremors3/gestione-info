import lucene

from org.apache.lucene.store import RAMDirectory
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField

# Inizializza la macchina virtuale Java (JVM)
#lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Creazione di un documento
doc = Document()
doc.add(Field("title", "Lucene Introduction", TextField.TYPE_STORED))

# Creazione di un indice in memoria
directory = RAMDirectory()
writer_config = IndexWriterConfig(StandardAnalyzer())
writer = IndexWriter(directory, writer_config)

# Aggiungere il documento all'indice
writer.addDocument(doc)
writer.commit()

# Chiudere il writer
writer.close()
