import requests
import urllib


# The class fetches results from the Star Wars API
class Swapi:
    def __init__(self, base_url):
        self._base_url = base_url

    def search(self, resource, term=""):
        """
        The function will search data in a given resource 
        :param resource: the resource to search in (str)
        :param term: the search query - by default retrive all resource data (list of dict)
        """
        query =  '/?' + urllib.parse.urlencode({'search': term})
        url = self._base_url + resource + query
        results = []
        while url: # Iterating over each page
            res = Swapi.get_json_response(url)
            url = res['next']
            results += res['results']
        return results         

    def get_planets(self):
        """ 
        The function will get sorted results about all the planets in the website
        """
        # getting all planets is an alias for searching for all planets
        return self.search('planets')

    @staticmethod
    def get_json_response(endpoint):
        """
        Static method that parsing json data from the api
        :param endpoint: endpoint in the api (string)
        :return: the json response (dict)
        """
        print(endpoint)
        return requests.get(endpoint).json()
