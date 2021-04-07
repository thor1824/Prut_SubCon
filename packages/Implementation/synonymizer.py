from ..Entities.synonym import Synonym
from ..Interfaces.synonymizer_interface import ISynonymizer
from ..Interfaces.synonym_data_source_interface import ISynonymDataSource


def __levenshtein_distance__(s: str, t: str) -> int:
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

class synonymizer(ISynonymizer):
    searchedTerms = dict()
    mostSearchedTerm: str = None
    __data_source: ISynonymDataSource = None
    """request_dict = dict()"""
    __request_dict = {'Wood': [Synonym('wooden', 1), Synonym('woods', 1), Synonym('woodwind', 1)]}

    def set_synonym_data_source(self, data: ISynonymDataSource) -> None:
        """Dependency injection of the data source"""
        self.__data_source = data

    def get_synonyms(self, search_term: str) -> list[str]:
        self.addToSearchedTerms(search_term)
        try:
            result = self.__request_dict[search_term]
            return result
        except:
            if self.__data_source is None:
                raise Exception('Not yet initialized properly')

            result2 = self.__data_source.get_synonyms(search_term)
        result2.sort(key=lambda x: __levenshtein_distance__(search_term, x.word))
        if len(result2) == 3:
            return result2

        
        """Get the synonyms from the data source. Calculate levenshtein distance and return top 3 results"""
        """Must be sorted on levenshtein distance (lowest first)"""
        """The result must be locally cached in memory for future requests"""
        pass

    def get_last_result(self) -> str:
        """Returns the last result returned by this instance"""
        pass

    def get_most_searched_term(self) -> str:
        """Returns the most searched term. Must be O(1)"""
        return self.mostSearchedTerm
        pass

    def __cache_result(self, search_key: str, result: list[Synonym]):
        self.__request_dict[search_key] = result

    def addToSearchedTerms(self, search_key: str):
        i = self.searchedTerms.get(search_key)
        if self.mostSearchedTerm == None:
            self.mostSearchedTerm = search_key

        if i != None:
            self.searchedTerms[search_key] += 1
            i += 1

        else:
            self.searchedTerms[search_key] = 1
            i = 1

        if self.searchedTerms[self.mostSearchedTerm] < i:
            self.mostSearchedTerm = search_key

