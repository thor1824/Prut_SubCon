from ..Entities.synonym import Synonym
from ..Interfaces.synonymizer_interface import ISynonymizer
from ..Interfaces.synonym_data_source_interface import ISynonymDataSource


def __levenshtein_distance__(s: str, t: str) -> int:
    """Calculates the levenshtein distance of two words"""

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
    __data_source: ISynonymDataSource = None
    __request_dict = dict()

    def set_synonym_data_source(self, data: ISynonymDataSource) -> None:
        """Dependency injection of the data source"""
        self.__data_source = data

    def get_synonyms(self, search_term: str) -> list[str]:
        """Get the synonyms from the data source. Calculate levenshtein distance and return top 3 results"""
        try:
            # tries to get cached result
            cache_result = self.__request_dict[search_term]
            return cache_result
        except:
            # caches if search term is not present in the dictionary
            # i.e no result cached by given thr search term
            if self.__data_source is None:
                raise Exception('Not yet initialized properly')

            api_results = self.__data_source.get_synonyms(search_term)

        # Sorts the api_result by the levenshtein distance
        api_results.sort(key=lambda x: __levenshtein_distance__(search_term, x.word))

        top_result = list()
        n_of_results = 3

        # checks if it is possible to return a list of top three,
        # if not the set n_of_results is set to the length og the array
        if len(api_results) < 3:
            n_of_results = len(api_results)

        for i in range(n_of_results):
            top_result.append(api_results[i].word)

        # caches the result of the search term
        self.__cache_result(search_term, top_result)
        return top_result

    def get_last_result(self) -> str:
        """Returns the last result returned by this instance"""
        pass

    def get_most_searched_term(self) -> str:
        """Returns the most searched term. Must be O(1)"""
        pass

    def __cache_result(self, search_key: str, result: list[Synonym]):
        self.__request_dict[search_key] = result
