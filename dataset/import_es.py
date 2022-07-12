import json
import logging
from os import path
from typing import Dict, List

import ipdb
from elasticsearch.client import Elasticsearch

DATA_DIR = "MLQA/Test/"
ES_INDEX = "vi_ahihi_2"
DATA_FILE = path.join(DATA_DIR, "test-context-vi-question-vi.json")

logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def import_squad_style(data: List[Dict]) -> None:
    """Import SquAD-style dataset into ElasticSearch index.

    Arguments format:
    {
        "title": <str>,
        "paragraphs": [
            {
                "context": <str>,
                "qas": [...],
            },
            ...
        ]
    }
    """
    # Importing
    ES = Elasticsearch(
        timeout=80,
        max_retries=3,
        retry_on_timeout=True,
    )
    counter = 0
    for dt in data:
        title = dt["title"]
        for para in dt["paragraphs"]:
            content = para["context"]
            doc = {
                "title": title,
                "content": content,
            }
            response = ES.index(
                index=ES_INDEX,
                id=counter,
                body=doc,
            )
            logging.info(
                "[+] Added (id: {id}): {title}".format(
                    id=counter,
                    title=title,
                )
            )
            counter += 1


if __name__ == "__main__":
    with open(DATA_FILE, encoding="ascii") as f:
        corpus = json.load(f)
        data = corpus["data"]
        import_squad_style(data)
