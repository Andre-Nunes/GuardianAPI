from elasticsearch import Elasticsearch
import json
import os

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def indexar_artigos(indice, ficheiro_json):
    """
    Conecta ao Elasticsearch, cria o índice (caso não exista) e indexa os artigos do ficheiro JSON.
    """
    es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "*6n_RqIr=GpVhiz3*Nzh"),
    verify_certs=False  # útil para ignorar certificados autoassinados
)
    
    # Cria o índice com mapeamento, caso ele não exista
    if not es.indices.exists(index=indice):
        mapping = {
            "mappings": {
                "properties": {
                    "id": {"type": "keyword"},
                    "webTitle": {"type": "text"},
                    "webUrl": {"type": "text"},
                    "headline": {"type": "text"},
                    "trailText": {"type": "text"},
                    "body": {"type": "text"},
                    "timestamp": {"type": "date"}
                }
            }
        }
        es.indices.create(index=indice, body=mapping)
        print(f"Índice '{indice}' criado.")
    else:
        print(f"Índice '{indice}' já existe.")
    
    # Verifica se o ficheiro JSON existe e carrega os dados
    if os.path.exists(ficheiro_json):
        with open(ficheiro_json, "r", encoding="utf-8") as file:
            dados = json.load(file)
        print("Total de registos carregados:", len(dados))
    else:
        print("Ficheiro", ficheiro_json, "não encontrado.")
        return
    
    # Indexa cada artigo no Elasticsearch usando o campo 'id' do artigo
    for artigo in dados:
        es.index(index=indice, id=artigo.get("id"), body=artigo)
    print("Indexação concluída.")

def executar_query(indice, query_body):
    from elasticsearch import Elasticsearch

    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=("elastic", "*6n_RqIr=GpVhiz3*Nzh"),
        verify_certs=False
    )

    resultados = es.search(index=indice, body=query_body)
    return resultados

if __name__ == "__main__":
    # Configurações
    INDEX_NAME = "artigos_guardian"
    JSON_FILE = "artigos/artigos_guardian.json"

    # Indexação dos dados
    indexar_artigos(INDEX_NAME, JSON_FILE)

    # Exemplo de Query 1: Buscar artigos cujo campo "body" contenha a palavra "technology"
    query1 = {
        "query": {
            "match": {
                "body": "technology"
            }
        }
    }
    
    resultados1 = executar_query(INDEX_NAME, query1)
    print("\nResultados da Query 1:")
    for hit in resultados1['hits']['hits']:
        print(f"ID: {hit['_id']} - Título: {hit['_source']['webTitle']} - Score: {hit['_score']}")