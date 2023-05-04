"""
Caches JSON to a flat file 

For example, when you need to cache an API response for (n) period, 
but saving to a database is just too extra. 
"""
import os
import time
import json 

class CacheJSON:
    """A class to cache a JSON API response to a flat file. 

    ...

    Attributes
    ----------
    length : int
        The length of the cache in seconds
        default: 3600 (1 hour)
    file : str
        A file name to save the JSON data to
        default: cache.json
    file_path : str
        The path to the file
        default: os.path.join(os.getcwd(), file)
    data : json
        The JSON data to save to the file

    Methods
    -------
    save()
        Saves the JSON data to the file
    load()
        Loads the JSON data from the file
    is_expired()
        Checks if the cache is expired
    is_valid()
        Checks if the cache is valid
    get()
        Gets the JSON data from the cache
    set()
        Sets the JSON data to the cache
    """
    length = 3600
    data = None
    file = 'cache.json'
    file_path = os.path.join(os.getcwd(), file)

    def __init__(self, file: str = None, data: json = None, file_path: str = None) -> None:
        """Initialize the class with the data, file name, and file path

        Parameters
        ----------
        file : str
            Optional, the file name to save the JSON data to
        data : json
            The JSON data to save to the file
        file_path : str
            Optional, the path to the file

        """
        if data:
            self.data = data

        if file: 
            self.file = file

        if file_path:
            self.file_path = file_path

    def save(self) -> None:
        """Saves the JSON data to the file"""
        with open(self.file_path, 'w', encoding='utf-8') as handle:
            json.dump(self.data, handle)

    def load(self) -> json:
        """Loads the JSON data from the file"""
        with open(self.file_path, 'r', encoding='utf-8') as handle:
            return json.load(handle)
    
    def is_expired(self) -> bool:
        """Checks if the cache is expired

        Parameters
        ----------
        length : int
            The length of the cache in seconds

        Returns
        -------
        bool
            True if the cache is expired, False otherwise

        """
        if self.is_valid():
            return os.path.getmtime(self.file_path) + self.length < time.time()
        else:
            return True
    
    def is_valid(self) -> bool:
        """Checks if the cache is valid

        Returns
        -------
        bool
            True if the cache is valid, False otherwise

        """
        return os.path.exists(self.file_path)

    def get(self) -> json:
        """Gets the JSON data from the cache

        Returns
        -------
        json
            The JSON data from the cache

        """
        if self.is_valid():
            return self.load()
        else:
            return None

    def set(self, data: json) -> None:
        """Sets the JSON data to the cache

        Parameters
        ----------
        data : json
            The JSON data to save to the file

        """
        self.data = data
        self.save()
    
    def __str__(self) -> str:
        """Returns the JSON data as a string

        Returns
        -------
        str
            The JSON data as a string

        """
        return str(self.data)

if __name__ == '__main__':
    #Example usage
    import requests

    url = 'https://dummyjson.com/products'

    cache = CacheJSON()
    if cache.is_expired():
        print('Cache is expired')
        r = requests.get(url)
        data = r.json()
        cache.set(data)
    else:
        print('Cache is valid')
        data = cache.get()

    print(data)
  
          
