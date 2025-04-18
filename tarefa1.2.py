# Importa as bibliotecas necessárias para manipulação e visualização dos dados
import json
import os
from datetime import datetime

# Define o caminho para o ficheiro JSON onde os artigos foram armazenados
ficheiro_json = "artigos/artigos_guardian.json"

# Verifica se o ficheiro existe
if os.path.exists(ficheiro_json):
    with open(ficheiro_json, "r", encoding="utf-8") as file:
        dados = json.load(file)
    print("Total de registos carregados:", len(dados))
else:
    print("Ficheiro", ficheiro_json, "não encontrado.")

    # Exibe os primeiros 5 registos, mostrando os campos principais
numero_registos = 5
print(f"Exibindo os primeiros {numero_registos} registos:")

for i, registo in enumerate(dados[:numero_registos]):
    print(f"\n--- Registo {i+1} ---")
    print("ID:", registo.get("id"))
    print("Título:", registo.get("webTitle"))
    print("URL:", registo.get("webUrl"))
    print("Headline:", registo.get("headline"))
    print("TrailText:", registo.get("trailText"))
    print("Timestamp:", registo.get("timestamp"))
    # Exibe uma prévia do campo "body" (caso exista)
    corpo = registo.get("body", "")
    if corpo:
        print("Corpo (primeiros 200 caracteres):", corpo[:200], "...")
