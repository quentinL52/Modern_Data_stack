import io
import pandas as pd
import requests
import re
from tqdm import tqdm
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def api_helloworld_stage(periode="h", local="ile de france", keyword="data", contrat="Stage"):
    results = []

    params = {
        "k": keyword,
        "k_autocomplete": "",
        "l": local,
        "l_autocomplete": "",
        "sort": "relevance",
        "c": contrat,
        "cod": "all",
        "ray": 20,
        "d": periode
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        "Referer": "www.hellowork.com"
    }

    response = requests.get("https://www.hellowork.com/searchoffers/getsearchfacets", params=params, headers=headers)
    response_json = response.json()

    if "Results" in response_json and response_json["Results"]:
        for result in tqdm(response_json["Results"]):
            publication_date = result["PublishDate"]
            match = re.search(r'(\d{4}-\d{2}-\d{2})', publication_date)
            formatted_date = match.group(0) if match else publication_date
            lien = result["UrlOffre"]
            lien_origine = f'https://www.hellowork.com{lien}'
            localisations = result.get("Localisations", [])
            ville = localisations[3]["Label"] if len(localisations) > 3 else "N/A"
            result_dict = {
                "entreprise": result["CompanyName"],
                "publication": formatted_date,
                "poste": result["OfferTitle"],
                "contrat": result["ContractType"],
                "profil": result["Profile"],
                "description": result["Description"],
                "ville": ville,
                "lien": lien_origine,
                "source": result["ResponseUrl"]
            }
            results.append(result_dict)

    df = pd.DataFrame(results)
    df.reset_index(drop=True, inplace=True)
    return df

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    df = api_helloworld_stage(
        periode="h",  # h pour aujourd'hui
        local="ile de france",
        keyword="data",
        contrat="Stage"
    )
    return df


@test
def test_output(output, *args) -> None:
    """
    Test de la sortie du bloc
    """
    assert output is not None, 'La sortie est non définie'
    assert isinstance(output, pd.DataFrame), 'La sortie doit être un DataFrame'
    assert len(output.columns) > 0, 'Le DataFrame ne doit pas être vide'