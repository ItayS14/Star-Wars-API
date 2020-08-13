import requests


class Swapi:
    def __init__(self, base_url, resources = None):
        self._base_url = base_url
        self._resources = resources or Swapi.get_json_response(self._base_url)

    def search(self, resource, term=""):
        """
        The function will search data in a given resource 
        :param resource: the resource to search in (str)
        :param term: the search query - by default retrive all resource data
        :raise: InvalidResource - in case the resource was invalid
        """
        if resource not in self._resources:
            raise Swapi.InvalidResource
        
        results = []
        url = self._base_url + resource + '/' + f'?search={term}'
        while url:
            res = Swapi.get_json_response(url)
            url = res.get('next')
            results += res['results']
        return results         

    @staticmethod
    def get_json_response(endpoint):
        """
        Static method that parsing json data from the api
        :param endpoint: endpoint in the api (string)
        :return: the json response (dict)
        """
        return requests.get(endpoint).json()

    # Execption that is thrown in case the resource was invalid
    class InvalidResource(Exception):
        pass