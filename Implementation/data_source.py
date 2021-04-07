from synonym import Synonym
from synonym_data_source_interface import ISynonymDataSource

class DataSource(ISynonymDataSource):
    def get_synonyms(self, searchTerm: str) -> list[Synonym]:
        """TODO"""
        pass
