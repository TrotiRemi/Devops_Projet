from elasticsearch import Elasticsearch, helpers
import pandas as pd

ELASTICSEARCH_URL = "http://localhost:9200"  # Changez si Elasticsearch est ailleurs
INDEX_NAME = "athle_results"
df = pd.read_csv("all2.csv")
def Pandas_Elastic(df):
    """
    Synchronise les données d'un DataFrame pandas vers Elasticsearch.
    """
    # Connexion à Elasticsearch
    es = Elasticsearch(hosts=[ELASTICSEARCH_URL])

    # Vérification si l'index existe dans Elasticsearch, sinon création
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "competition_name": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                        },
                        "distance": {"type": "float"},
                        "Minute_Time": {"type": "float"},
                        "athlete": {"type": "text"},
                        "club": {"type": "text"},
                        "category": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                        },
                        "department": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                        },
                        "competition_date": {"type": "date", "format": "yyyy-MM-dd"},
                        "vitesse": {"type": "float"},
                        "type": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                        },
                        "type_course": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                        },
                        "location": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                        },
                        "ligue": {
                            "type": "text",
                            "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}
                        }
                    }
                }
            }
        )
        print(f"Index '{INDEX_NAME}' créé avec succès.")

    # Préparation des documents pour Elasticsearch
    actions = []
    for i, row in df.iterrows():
        actions.append({
            "_index": INDEX_NAME,
            "_id": i,  # Utilisation de l'index du DataFrame comme ID
            "_source": row.to_dict()  # Conversion de la ligne du DataFrame en dictionnaire
        })

    # Insertion des documents dans Elasticsearch
    try:
        helpers.bulk(es, actions)
        print(f"Synchronisation réussie : {len(actions)} documents insérés dans Elasticsearch.")
    except helpers.BulkIndexError as e:
        print(f"Erreur lors de l'insertion en masse dans Elasticsearch : {e.errors}")
        raise

Pandas_Elastic(df)
