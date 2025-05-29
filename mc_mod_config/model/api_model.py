import requests
from mc_mod_config.util import MetaSingleton

class ApiModel(metaclass=MetaSingleton):
    def __init__(self):
        self.api_path = "https://api.modrinth.com/v2/"

    def search_mod(self, query: str, index: str = 'relevance', offset: int = 0, limit: int = 10) -> dict:
        response = requests.get(f"{self.api_path}/search", {
            "query": query,
            "index": index,
            "offset": offset,
            "limit": limit,
            "facets": """[["project_type:mod"]]"""
        })
        if response.status_code == 400:
            raise ValueError(f"{response.json()['error']}: {response.json()['description']}")
        return response.json()

def get_api_model() -> ApiModel:
    return ApiModel()