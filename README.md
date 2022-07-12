# Scalable fact-checking and question answering system
# Table of contents
[Idea](#idea)
- [Retriever](#retriever)
- [Reader and Inferrer](#reader-and-inferrer)

[Manual](#manual)
- [Install dependencies](#1-install-dependencies)
- [Setup indices](#2-setup-indices)
    - [ElasticSearch](#21-elasticsearch-index)
    - [MySQL database](#22-mysql-database)
- [Import data to indices](#3-import-data-to-indices)
- [Deploy](#4-deploy)
    - [Backend](#backend)
    - [Encoder](#encoder)
    - [Frontend](#frontend)
- [Preprocess](#preprocess)

[Note](#note)

# Idea
Our main contribution is a scalable fact-checking system which provides two main features:
- **Question answering**
- **Fact checking**

Our system is a combination of multiple components ranging from NLI, QA, IR in NLP:
- **Retriever**: retrieve a set of most relevant data related to the content that the user requests
- **Reader**: search and extract answer for the question from the user, given the relevant data from the Retriever
- **Inferrer**: classify each data (evidence) in the set of most relevant data from the Retriever given the user's claim

## Retriever
![Information retrieval procedure](/images/IR.png)

## Reader and Inferrer
![Fact checking and Question answering procedures](/images/FEVER-QA.png)

## Data preprocessing
![Data preprocessing](/images/Preprocess.png)

# Manual
Instruction to reproduce the experiment step-by-step for the testset of the [MLQA dataset](https://github.com/facebookresearch/MLQA)

**Python**: 3.7.5

## 1. Install dependencies
```bash
pip install -r requirements.txt
```

also, install missing packets for FAISS library:
```bash
sudo apt-get install libopenblas-dev
sudo apt-get install libomp-dev
```

## 2. Setup indices
### 2.1. ElasticSearch index
Clone: 
```bash
git clone https://github.com/icesonata/docker-es-cococ-tokenizer.git
```

Deploy:
``` bash
docker-compose up -d
```
*Note: this may require `sudo` privilege.

Create index with `title` and `content` fields via API :

(for `cURL`, move to the *Alternative* below the payload)

Send to `localhost:9200/vi_mlqa_test` with `PUT` method and the payload below.

```json
{
  "settings": {
    "index": {
        "number_of_shards" : 1,
        "number_of_replicas" : 1,        
      "analysis": {
        "analyzer": {
          "my_analyzer": {
            "tokenizer": "vi_tokenizer",
            "char_filter":  [ "html_strip" ],
            "filter": [
              "icu_folding"
            ]
          }
        }
      }
    }
  },
  "mappings": {
    "properties" : {
      "title" : {
          "type" : "text",
          "analyzer": "my_analyzer"
      },
      "content" : {
          "type" : "text",
          "analyzer" : "my_analyzer"
      }
    }
  }
}
```
*Alternatively, using `cURL`:
```bash
curl -XPUT "http://localhost:9200/vi_mlqa_test" -H 'Content-Type: application/json' -d'{"settings": {"index":{"number_of_shards":1,"number_of_replicas":1,"analysis":{"analyzer":{"my_analyzer":{"tokenizer":"vi_tokenizer","char_filter":["html_strip"],"filter":["icu_folding"]}}}}},"mappings":{"properties":{"title" :{"type":"text","analyzer":"my_analyzer"},"content":{"type":"text","analyzer":"my_analyzer"}}}}'
```

**Misc**

Check the existing indices:
```bash
curl -XGET localhost:9200/_cat/indices
```

Count the number of documents in an index:
```bash
curl -XGET localhost:9200/vi_mlqa_test/_count
```

### 2.2. MySQL database
Setup MySQL with password=`root` and host port=`15432`
```bash
docker run --name db_index -e MYSQL_ROOT_PASSWORD=root -p 15432:3306 -d mysql:latest
```

Get into to the MySQL container:
```bash
docker exec -it db_index /bin/bash
```
*Note: this step may require `sudo` privilege.

Get into MySQL server in the container:
```bash
mysql -uroot -p
```
*Note: enter password=`root` when the server requires authentication.

Create a database, named `corpus`:
```sql
CREATE corpus;
USE corpus;
```

Create a new user:
```sql
CREATE USER 'longnguyen'@'%' IDENTIFIED BY 'longnguyen';
```

Grant the user with privilege enough for access on the `corpus` database from SQLAlchemy:
```sql
GRANT ALL PRIVILEGES ON test_db.* to 'longnguyen'@'%';
```

Create document table:
```sql
CREATE TABLE mlqa_test_articles(id int not null auto_increment, title text, content longtext, publish_date varchar(50), primary key(id)) character set utf8mb4 collate utf8mb4_general_ci;
```

Create sentence table:
```sql
CREATE TABLE mlqa_test_sent_articles(id int not null auto_increment, sentence text, doc_id int, primary key(id), foreign key(doc_id) references mlqa_test_articles(id) on delete cascade) character set utf8mb4 collate utf8mb4_unicode_ci;
```

**Misc**

Check tables:
```sql
SHOW tables;
DESCRIBE mlqa_test_articles;
DESCRIBE mlqa_test_sent_articles;
```

Count number of entries in the tables:
```sql
SELECT COUNT(*) FROM mlqa_test_articles;
SELECT COUNT(*) FROM mlqa_test_sent_articles;
```

## 3. Import data to indices
Move to `dataset/` directory.
```bash
cd dataset/
```

**ElasticSearch**
```bash
python import_es.py
```

**MySQL**
```bash
python import_db.py
```

## 4. Deploy
For deployment, make sure ElasticSearch and MySQL are working.

This step requires 3 separate shells:
- Backend 
- Encoder
- Frontend

### Backend
Move to `backend/` directory to deploy server on the `0.0.0.0` with port `8888` by running the command below:
```bash
python manage.py runserver 0.0.0.0:8888
```

### Encoder
Move to `encoder/` directory and change `ROOT_DIR` to an absolute path to the directory of the project, e.g.,
```python
ROOT_DIR = "/home/username/FactCheck-QA/"
```

Then, run the command below:
```bash
python encoder_server.py
```

*Note: change serving address of the Encoder via `serve()` function of the `encoder/encoder_server.py`

### Frontend
**NodeJS**: >= 16.0

*Note: use [nvm](https://github.com/nvm-sh/nvm) for switching to newer nodeJS version.

Move to `frontend/` directory and run the command below once to install the dependencies:
```bash
npm install
```

Then, everytime frontend needs to be deployed, just run the command below:
```bash
npm run dev
```

*Note: frontend interacts with backend via API. You can change backend address in `frontend/src/@core/utils/api/api.js`

# Preprocess
Look into `dataset/[Research]_Sentence_processing_for_SquAD_format_dataset.ipynb`

or you can reuse the available resources of the MLQA dataset we provide.

# Note
There are some note for this project:
- There is a indexing mismatch between the indices that mentioned in the comments, for example:
    - **MySQL**: 1-index
    - **ElasticSearch**: 0-index
    - **FAISS**: 0-index
- How to change language models which are downloaded from [HuggingFace](https://huggingface.co): there are two files to be concerned
    - `backend/apps/search/components/config.py`:
        - `READER_MODEL`: question-answering model
        - `INFERRER_MODEL`: natural language inference model, text-classification following NLI model, or zero-shot classification model. Note that different models have different output style, hence we must config our `backend/apps/search/components/inferrer.py` to comply with the output format.
    - `encoder/encoder_server.py`:
        - `EMBEDDING_MODEL`: embedding model released by [SBERT](https://huggingface.co/sentence-transformers)
        - `FEATURE_SIZE`: dimension of the output that the embedding model produces
- We use *IndexFlatL2* combined with *IndexIDMap* of FAISS for semantic search
- Remember to alter the address and port of different services in the `config.py` file. Also, `K` indicates number of documents retrieved in the full-text search conducted by ElasticSearch, while `L` indicating number of sentences to retrieved from `K` documents by semantic search. In other words, in information retrieval step, `K`->`L` documents are retrieved.
- Reader offers two modes: `concat` and `ensemble`, which can be set in the `config.py`:
    - `concat`: concatenates *L* retrieved data into a *context* and, with the question, put it to the language model
    - `ensemble`: each data in *L* retrieved data will be treated as a *context* and the final step is filter out an answer with highest confidence score provided by the language model. *Note*: this mode usually produces less accurate results.
- By default, the project runs only on CPU. Therefore, considering switching `device` to 0 or `gpu`, etc. for better productivity with GPU if available.

Authors:
- [Long Nguyen-Hoang](https://github.com/icesonata)
- [Nhan Trinh-Huynh-Trong](https://github.com/18521184)
