import os, json
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, NUMERIC, STORED, KEYWORD, DATETIME

with open("corpus.json", mode="r", encoding='utf-8') as f:
    doc = json.load(f)

if not os.path.exists("index_dir"):
    os.mkdir("index_dir")

schema = Schema(
    number = ID(stored=True, unique=True),
    files = STORED,
    title = TEXT(stored=True),
    authors = TEXT(stored=True),
    date = STORED,
    more_info = STORED,
    status = TEXT(stored=True),
    abstract = TEXT(stored=True),
    keywords = KEYWORD(commas=True),
    content = TEXT
)

ix = index.create_in("index_dir", schema)
writer = ix.writer()

for d in doc:
    writer.add_document(
        number = d["Number"],
        files = d["Files"],
        title = d["Title"],
        authors = d["Authors"],
        date = d["Date"],
        more_info = d["More Info"],
        status = d["Status"],
        abstract = d["Abstract"],
        keywords = d["Keywords"],
        content = d["Content"]
    )

writer.commit()