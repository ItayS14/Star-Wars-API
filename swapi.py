import requests

class Swapi:
    def __init__(self, base_url, resources = None):
        self._base_url = base_url

    def search(self, resource, term=""):
        """
        The function will search data in a given resource 
        :param resource: the resource to search in (str)
        :param term: the search query - by default retrive all resource data (list of dict)
        """
        results = []
        url = self._base_url + resource + '/?search=' + term
        while url:
            res = Swapi.get_json_response(url)
            url = res['next']
            results += res['results']
        return results         

    def get_planets(self, field, dec):
        """ 
        The function will get sorted results about all the planets in the website
        :param field: The field to sort by (string)
        :param dec: if true sorting in descending order otherwise ascending order (bool)
        """
        data = self.search('planets')
        #return sorted(data, key=lambda x: x[field], reverse=dec)
        return data
        
    @staticmethod
    def get_json_response(endpoint):
        """
        Static method that parsing json data from the api
        :param endpoint: endpoint in the api (string)
        :return: the json response (dict)
        """
        return requests.get(endpoint).json()
