# Parameters
K = 100
L = 10

# Question Answering module
# https://huggingface.co/ancs21/xlm-roberta-large-vi-qa
READER_MODEL = "ancs21/xlm-roberta-large-vi-qa"
# READER_MODEL = "ahotrod/albert_xxlargev1_squad2_512"
DEVICE = -1   # int for GPU, -1 for CPU
READER_MODE = "concat"

# Inference task model
INFERRER_MODEL = "symanto/xlm-roberta-base-snli-mnli-anli-xnli"     # Checked
# INFERRER_MODEL = "ynie/albert-xxlarge-v2-snli_mnli_fever_anli_R1_R2_R3-nli"   # Checked

# Database
DB_CONFIG = {
    "host": "localhost",
    "port": 15432,
    "user": "longnguyen",
    "password": "longnguyen",
    "database": "corpus"
}

DB_NAME = "mlqa_test"

DB_SENT_TABLE = f"{DB_NAME}_sent_articles"
DB_ARTICLE_TABLE = f"{DB_NAME}_articles"

# ElasticSearch
ES_CONFIG = {
    "host": "localhost",
    "port": 9200,
    "index": f"vi_{DB_NAME}",
}
ES_FIELDS = [
    # "title",
    "content",
]

# Configuration parameters
DB_SETTING = {
    "host": DB_CONFIG.get("host"),
    "port": DB_CONFIG.get("port"),
    "user": DB_CONFIG.get("user"),
    "pwd": DB_CONFIG.get("password"),
    "db_name": DB_CONFIG.get("database"),
    "db_sent_table": DB_SENT_TABLE,
}

ES_SETTING = {
    **ES_CONFIG,
    "K": K,
    "list_fields": ES_FIELDS,
}

READER_SETTING = {
    "model": READER_MODEL,
    "device": DEVICE,
    "mode": READER_MODE,
}

RERANKER_SETTING = {
    "host": "localhost",
    "port": 50051,
    "L": L,
}

INFERRER_SETTING = {
    "model": INFERRER_MODEL,
    "device": DEVICE,
}

RETRIEVER_SETTING = {
    "db_setting": DB_SETTING,
    "es_setting": ES_SETTING,
    "reranker_setting": RERANKER_SETTING,
    "reader_setting": READER_SETTING,
    "inferrer_setting": INFERRER_SETTING,
}
