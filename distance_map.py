"""Assignment 1 - Distance map (Task 1)

CSC148, Winter 2021

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

All of the files in this directory and all subdirectories are:
Copyright (c) 2021 Diane Horton, Ian Berlott-Atwell, Jonathan Calver,
Sophia Huynh, Myriam Majedi, and Jaisie Sin.

===== Module Description =====

This module contains the class DistanceMap, which is used to store
and look up distances between cities. This class does not read distances
from the map file. (All reading from files is done in module experiment.)
Instead, it provides public methods that can be called to store and look up
distances.
"""
from typing import Dict


class DistanceMap:
    """Lets client code store and look up the distance betweeen any two
    cities.
    === Attributes ===
    _distances: A dictionary that keeps track of the distance between two
        cities, each key item is a string with one city name, and its value is a dictionary which takes another city
        as destination and an integer which is the distance between them. Keep in mind the distance from city A to city
        B could be different than the distance from city B to city A!
    === Representation Invariants ===
    - The distance between cities must not be negative.
    === Sample Usage ===
    >>> d = DistanceMap()
    >>> d.add_distance('Toronto', 'Montreal', 10)
    >>> d.distance('Toronto', 'Montreal')
    10
    >>> d.add_distance('Toronto', 'Ottawa')
    >>> d.distance('Toronto', 'Ottawa')
    -1
    """
    _distances: Dict[str, Dict[str, int]]

    def __init__(self) -> None:
        """Create an empty dictionary which will serve as the distance
        storage."""
        self._distances = {}

    def add_distance(self, city_a: str, city_b: str, distance: int = -1) -> None:
        """Add the distance from <city_a> to <city_b> to our private dictionary.
        If no distance parameter is passed, add -1 as the distance.

        >>> d = DistanceMap()
        >>> d.add_distance('Edmonton', 'Toronto', 40)
        >>> d.add_distance('Toronto', 'Calgary', 45)
        >>> d.distance('Edmonton', 'Toronto')
        40
        >>> d.distance('Toronto', 'Calgary')
        45
        >>> d.add_distance('Toronto', 'Ottawa')
        >>> d.distance('Toronto', 'Ottawa')
        -1
        """
        try:
            self._distances[city_a][city_b] = distance
        except KeyError:
            self._distances[city_a] = {}
            self._distances[city_a][city_b] = distance

    def distance(self, city_a: str, city_b: str) -> int:
        """Return the distance from <city_a> to <city_b> stored in _distances.
        Return -1 if those cities haven't been stored.
        """
        try:
            return self._distances[city_a][city_b]
        except KeyError:
            return -1


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
