class ExperiSearchError(Exception):
    pass

class QueryError(ExperiSearchError):

    def __init__(self, search_term, url, exception):
        self.msg = (
            "Issue when querying url: " + url + " with search term: " +
            search_term + "\nGot exception: " + str(exception)
        )
