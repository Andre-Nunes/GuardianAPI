#guardian_scraper
import requests
import json
import os
import logging
from datetime import datetime

# API Key via variável de ambiente
API_KEY = os.environ.get("GUARDIAN_API_KEY")
print("API_KEY carregada:", bool(API_KEY))

# Caminhos
os.makedirs("logs", exist_ok=True)
os.makedirs("artigos", exist_ok=True)
FICHEIRO_JSON = "artigos/artigos_guardian.json"
FICHEIRO_LOG = "logs/guardian.log"

# Logging
logging.basicConfig(
    filename=FICHEIRO_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def recolher_guardian(max_paginas=20):
    url = "https://content.guardianapis.com/search"
    artigos_total = []

    # Carregar artigos existentes se houver
    artigos_existentes = {}
    if os.path.exists(FICHEIRO_JSON):
        with open(FICHEIRO_JSON, "r", encoding="utf-8") as f:
            try:
                dados_existentes = json.load(f)
                artigos_existentes = {art["id"]: art for art in dados_existentes}
            except json.JSONDecodeError:
                logging.warning("Ficheiro JSON existente estava vazio ou inválido.")

    novos_artigos = 0

    for pagina in range(1, max_paginas + 1):
        params = {
            "api-key": API_KEY,
            "page-size": 50,
            "page": pagina,
            "order-by": "newest",
            "show-fields": "headline,trailText,body",
            "q": "technology OR science"
        }

        try:
            r = requests.get(url, params=params)
            dados = r.json()

            resultados = dados.get("response", {}).get("results")
            if not resultados:
                break

            for res in resultados:
                artigo_id = res["id"]
                if artigo_id not in artigos_existentes:
                    artigo = {
                        "id": artigo_id,
                        "webTitle": res["webTitle"],
                        "webUrl": res["webUrl"],
                        "headline": res["fields"].get("headline"),
                        "trailText": res["fields"].get("trailText"),
                        "body": res["fields"].get("body"),
                        "timestamp": datetime.now().isoformat()
                    }
                    artigos_existentes[artigo_id] = artigo
                    novos_artigos += 1

        except Exception as e:
            logging.error(f"Erro na página {pagina}: {str(e)}")
            break

    # Guardar todos os artigos (existentes + novos) no mesmo ficheiro
    with open(FICHEIRO_JSON, "w", encoding="utf-8") as f:
        json.dump(list(artigos_existentes.values()), f, ensure_ascii=False, indent=2)

    logging.info(f"{novos_artigos} novos artigos adicionados. Total atual: {len(artigos_existentes)}")

recolher_guardian()
