from synonym_data_source_interface import ISynonymDataSource


class ISynonymizer:
    def set_synonym_data_source(self, data: ISynonymDataSource) -> None:
        """Dependency injection of the data source"""
        pass

    def get_synonyms(self, searchTerm: str) -> list[str]:
        """Get the synonyms from the data source. Calculate levenshtein distance and return top 3 results"""
        """Must be sorted on levenshtein distance (lowest first)"""
        """The result must be locally cached in memory for future requests"""
        pass

    def get_last_result(self) -> str:
        """Returns the last result returned by this instance"""
        pass

    def get_most_searched_term(self) -> str:
        """Returns the most searched term. Must be O(1)"""
        pass