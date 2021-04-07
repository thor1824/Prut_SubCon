from ..Entities.synonym import Synonym
from ..Interfaces.synonym_data_source_interface import ISynonymDataSource
import requests
import json


class DataSource(ISynonymDataSource):
    def get_synonyms(self, searchTerm: str) -> list[Synonym]:
        """response = requests.get("https://api.datamuse.com/words?rel_syn=" + searchTerm)
        if (response.ok):
            synonyms = []
            data = response.json()

            for d in data:
                synonym = Synonym(d["word"], d["score"])
                synonyms.append(synonym)
            
            return synonyms
        else:
            return []
        pass"""
        return [Synonym('wooden', 1), Synonym('woods', 1), Synonym('woodwind', 1)]
