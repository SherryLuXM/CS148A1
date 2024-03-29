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
    """Lets client code store and look up the distance betweeen any two cities.
    === Public Attributes ===
    === Private Attributes ===
    _distances: records of distances from one city to another city in dict form.
    === Representation Invariants ===
    The distance between cities must not be negative.
    If the distance from city A to city B is recorded, the distance from city B
    to city A must be available.
    === Sample Usage ===
    >>> d = DistanceMap()
    >>> d.add_distance('Toronto', 'Montreal', 10)
    >>> d.distance('Toronto', 'Montreal')
    10
    >>> d.distance('Toronto', 'Ottawa')
    -1
    """
    _distances: Dict[str, Dict[str, int]]

    def __init__(self) -> None:
        """Create a distance record."""
        self._distances = {}

    def add_distance(self, city_a: str, city_b: str, distance1: int,
                     distance2: int = -1) -> None:
        """Add <distance1> and <distance2> for <city_a> and <city_b> to
        <self._distances>.

        >>> d = DistanceMap()
        >>> d.add_distance('Edmonton', 'Toronto', 40)
        >>> d.distance('Edmonton', 'Toronto')
        40
        >>> d.distance('Toronto', 'Edmonton')
        40
        >>> d.add_distance('Toronto', 'Edmonton', 45)
        >>> d.distance('Edmonton', 'Toronto')
        40
        >>> d.distance('Toronto', 'Edmonton')
        45
        """
        if distance2 == -1:  # check if <distance2> is not passed
            distance2 = distance1
        # check if <self._distances> already has values for <city_a>
        if city_a in self._distances:
            self._distances[city_a][city_b] = distance1
        else:
            self._distances[city_a] = {city_b: distance1}
        # record <distance2> to self._distances
        if city_b in self._distances:
            # check if the distance from <city_b> to <city_a> is already stored
            # in <self._distances>
            if city_a not in self._distances[city_b]:
                self._distances[city_b][city_a] = distance2
        else:
            self._distances[city_b] = {city_a: distance2}

    def distance(self, city_a: str, city_b: str) -> int:
        """Return the distance from <city_a> to <city_b> stored in _distances.
        Return -1 if those cities haven't been stored.

        >>> d = DistanceMap()
        >>> d.add_distance('Edmonton', 'Toronto', 40)
        >>> d.distance('Edmonton', 'Toronto')
        40
        >>> d.distance('Toronto', 'Edmonton')
        40
        >>> d.distance('Toronto', 'Vancouver')
        -1
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
