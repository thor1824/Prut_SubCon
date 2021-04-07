from ..Entities.synonym import Synonym


class ISynonymDataSource:
    def get_synonyms(self, searchTerm: str) -> list[Synonym]:
        """Returns all synonyms based on the searchterm """
        pass
