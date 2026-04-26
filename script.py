import requests
from notion_client import Client
from datetime import datetime
import os

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
DATABASE_ID = os.environ["DATABASE_ID"]

notion = Client(auth=NOTION_TOKEN)

def fetch_camara():
    url = "https://dadosabertos.camara.leg.br/api/v2/proposicoes?keywords=bitcoin"
    res = requests.get(url).json()

    projetos = []

    for item in res.get("dados", []):
        projetos.append({
            "nome": item["ementa"],
            "codigo": item["id"],
            "link": f"https://www.camara.leg.br/propostas-legislativas/{item['id']}",
            "fonte": "Câmara"
        })

    return projetos


def enviar(p):
    notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties={
            "Nome": {"title": [{"text": {"content": p["nome"]}}]},
            "País": {"select": {"name": "Brasil"}},
            "Código": {"rich_text": [{"text": {"content": str(p["codigo"])}}]},
            "Status": {"select": {"name": "Proposed"}},
            "Data de Atualização": {"date": {"start": datetime.now().isoformat()}},
            "Link Oficial": {"url": p["link"]},
            "Fonte": {"select": {"name": p["fonte"]}}
        }
    )


def main():
    projetos = fetch_camara()

    for p in projetos:
        enviar(p)


if __name__ == "__main__":
    main()
