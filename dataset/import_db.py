import json
from os import path
from typing import Dict, List

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# specify database configurations
config = {
    'host': 'localhost',
    'port': 15432,
    'user': 'longnguyen',
    'password': 'longnguyen',
    'database': 'corpus'
}
db_user = config.get('user')
db_pwd = config.get('password')
db_host = config.get('host')
db_port = config.get('port')
db_name = config.get('database')

# specify connection string
connection_str = f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"

# connect to database
engine = create_engine(connection_str)
# connection = engine.connect()
db = scoped_session(sessionmaker(bind=engine))

DB_NAME = "mlqa_test"
SENT_TABLE = f"{DB_NAME}_sent_articles_ahihi"
ARTICLE_TABLE = f"{DB_NAME}_articles_ahihi"

DATA_DIR = "MLQA/Test/"
DOCS_FILE = path.join(DATA_DIR, "docs.json")
DOC_SENT_MAP_FILE = path.join(DATA_DIR, "doc_range_map.json")
DATA_FILE = path.join(DATA_DIR, "test-context-vi-question-vi.json")


def import_docs(
    docs: List[str],
    doc_sent_map: Dict[str, Dict[str, int]]
) -> None:
    """Import documents to database."""
    for doc_id in doc_sent_map.keys():
        start = doc_sent_map[doc_id]["start"]
        end = doc_sent_map[doc_id]["end"]
        for idx in range(start, end+1):
            db.execute(
                f"""
                    INSERT INTO {SENT_TABLE} (sentence, doc_id)
                    VALUES (
                        :sentence, 
                        :doc_id
                    )
                """,
                {
                    "sentence": docs[idx],
                    # document's ID in MySQL is 1-index while doc_id is 0-index
                    # so we must increment it to comply with MySQL standard
                    "doc_id": int(doc_id)+1,
                },
            )
        print(f"Done for doc #{doc_id}")
    db.commit()
    print("Success!")


def import_dataset() -> None:
    """Import SquAD-format dataset."""
    with open(DATA_FILE, encoding="ascii") as f:
        corpus = json.load(f)
        data = corpus["data"]

        for dt in data:
            title = dt["title"]
            for para in dt["paragraphs"]:
                content = para["context"]
                db.execute(
                    f"""
                        INSERT INTO {ARTICLE_TABLE} (title, content)
                        VALUES (
                            :title,
                            :content
                        )
                    """,
                    {
                        "title": title,
                        "content": content,
                    }
                )
        db.commit()
    print("Success!")


if __name__ == "__main__":
    # Import articles into article table
    import_dataset()
    print("Done with document table.")

    # Import for sentence table
    with open(DOCS_FILE) as file_docs:
        docs = json.load(file_docs)
        with open(DOC_SENT_MAP_FILE) as file_map:
            doc_sent_map = json.load(file_map)
            import_docs(docs, doc_sent_map)
    print("Done with sentence table.")
