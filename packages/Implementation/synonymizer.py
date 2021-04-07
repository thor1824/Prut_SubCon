from ..Interfaces.synonymizer_interface import ISynonymizer
from ..Interfaces.synonym_data_source_interface import ISynonymDataSource

class synonymizer(ISynonymizer):
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

    def __levenshtein_distance__(self, s, t):
        # Initialize matrix of zeros
        rows = len(s) + 1
        cols = len(t) + 1
        distance = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(1, rows):
            for j in range(1, cols):
                distance[i][0] = i
                distance[0][j] = j

        for col in range(1, cols):
            for row in range(1, rows):
                if s[row - 1] == t[col - 1]:
                    cost = 0
                else:
                    cost = 1

                distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
                                         distance[row][col - 1] + 1,  # Cost of insertions
                                         distance[row - 1][col - 1] + cost)  # Cost of substitutions
        return distance[row][col]