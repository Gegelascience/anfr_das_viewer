"""module encapsulant la gestion du dataset de l'anfr"""
import requests


class AnfrConnector:
    """class encapsulant les appels à l'api anfr"""

    def __init__(self):
        self.__endpoint_resource = "/records/2.0/search/resource_id="
        self.__endpoint_search = "/datasets/2.0/search/include_drafts=false&include_private=false"
        self.__endpoint_dataset = "/datasets/2.0/DATASETID/id="
        self.__base_url = "https://data.anfr.fr/api"

    def search_dataset_by_name(self, name: str):
        """recherche un dataset par son nom"""
        response = requests.get(self.__base_url + self.__endpoint_search)
        if response.status_code == 200:
            if response.json().get("success"):
                data_response: dict = response.json().get("result")
                for res in data_response.get("results"):
                    if res.get("name") == name:
                        return res
                return None
            print(response.json().get("error"))
            return None
        print(response.status_code)
        return None

    def get_dataset_by_id(self, dataset_id: str):
        """recherche un dataset par son id"""
        response = requests.get(self.__base_url + self.__endpoint_dataset + dataset_id)
        if response.status_code == 200:
            if response.json().get("success"):
                return response.json().get("result")

            print(response.json().get("error"))
            return None
        print(response.status_code)
        return None

    def get_resource_data(self, resource_id: str):
        """récupère une ressource par son id"""
        response = requests.get(self.__base_url + self.__endpoint_resource + resource_id)
        if response.status_code == 200:
            if response.json().get("success"):
                return response.json().get("result")

            print(response.json().get("error"))
            return None

        print(response.status_code)
        return None
