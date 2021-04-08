import functools

from ..Interfaces.synonym_data_source_interface import ISynonymDataSource
from ..Interfaces.synonymizer_interface import ISynonymizer


def _levenshtein_distance(s: str, t: str) -> int:
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


class Synonymizer(ISynonymizer):
    _searched_terms = dict()
    _most_searched_term: str = None
    _last_result: str = None
    _data_source: ISynonymDataSource = None

    def set_synonym_data_source(self, data: ISynonymDataSource) -> None:
        """
        Dependency injection of the data source
        """

        self._data_source = data

    def get_synonyms(self, search_term: str) -> list[str]:
        """
        Gets the synonyms from the data source. Calculate levenshtein distance and return top 3 results
        """

        self._last_result = search_term
        top_result = self._get_top_n_synonym(search_term, 3)
        self._add_to_searched_terms(search_term)
        return top_result

    def get_last_result(self) -> str:
        """
        Returns the last searched term
        """

        return self._last_result

    def get_most_searched_term(self) -> str:
        """
        Returns the most searched term.
        """

        return self._most_searched_term

    def _add_to_searched_terms(self, search_key: str):
        """
        Adds the search_key to the __searched_terms dict and sets its "occurrence" to 1, if it already exist the
        occurrence wil be counter one up. if the n_occurrence is higher than the current __most_searched_term then it
        __most_searched_term wil be set as search_key's value
        """

        n_occurrence = self._searched_terms.get(search_key)
        if self._most_searched_term is None:
            self._most_searched_term = search_key

        if n_occurrence is not None:
            n_occurrence += 1
            self._searched_terms[search_key] += n_occurrence
        else:
            n_occurrence = 1
            self._searched_terms[search_key] = n_occurrence

        if self._searched_terms[self._most_searched_term] < n_occurrence:
            self._most_searched_term = search_key

    @functools.lru_cache(maxsize=100)
    def _get_top_n_synonym(self, search_term: str, n_results) -> list[str]:
        """
        Fetches all synonyms from the __data_source sorts them by the levenshtein distance in ascending order and
        return top n of that result (n_results).

        If two or more synonyms has the same levenshtein distance then those wil be sorted alphabetically in ascending Order

        Throws an Exception if  the __data_source is not set.
        """
        if self._data_source is None:
            raise Exception('Not yet initialized properly')

        api_results = self._data_source.get_synonyms(search_term)

        # Sorts the api_result first by the levenshtein distance then in alphabetical order, both in ascending order
        api_results.sort(key=lambda x: (_levenshtein_distance(search_term, x.word), x.word))

        top_result = list()
        n_of_results = n_results

        # checks if it is possible to return a list of top three,
        # if not the set n_of_results is set to the length og the array
        if len(api_results) < n_results:
            n_of_results = len(api_results)

        for i in range(n_of_results):
            top_result.append(api_results[i].word)

        return top_result
