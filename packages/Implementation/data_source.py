from ..Entities.synonym import Synonym
from ..Interfaces.synonym_data_source_interface import ISynonymDataSource
import requests
import json

class DataSource(ISynonymDataSource):
    def get_synonyms(self, searchTerm: str) -> list[Synonym]:
        response = requests.get("https://api.datamuse.com/words?rel_syn=" + searchTerm)
        if (response.ok):
            return response.json()
        else:
            return []
        pass
