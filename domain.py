"""Assignment 1 - Domain classes (Task 2)

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

This module contains the classes required to represent the entities
in the simulation: Parcel, Truck and Fleet.
"""
from typing import List, Dict
from distance_map import DistanceMap


class Parcel:
    """Create a parcel. Each parcel has a unique ID, volume (measured
    in cc), and a source and destination.

    === Public Attributes ===
    id_: a parcel's unique ID
    volume: how much space a parcel takes up in cubic centimetres
    source: name of the city it came from
    destination: name of the city its being delivered to

    === Representation Invariants ===
    - volume > 0
    - destination is not the depot
    === Sample Usage ===
    >>> p = Parcel(1, 10, 'Toronto', 'Calgary')
    >>> p.id_ == 1
    True
    >>> p.source == 'Toronto'
    True
    >>> p.destination == 'Calgary'
    True
    """
    id_: int
    volume: int
    source: str
    destination: str

    def __init__(self, id_: int, volume: int, source: str, destination: str) \
            -> None:
        """Create an instance of a parcel."""

        self.id_ = id_
        self.volume = volume
        self.source = source
        self.destination = destination


class Truck:
    """Create an instance of a truck. Each truck has a unique ID,
    volume capacity, and a Route.

    === Public Attributes ===
    id_: a truck's ID number
    volume_capacity: the maximum amount of volume a truck can carry.
    depot: a Truck's initial position.
    stored: how much volume is stored onto the Truck.
    route: an ordered List of city names that a truck is supposed to go through.
    parcels: the parcels allocated for the truck to deliver.
    === Representation Invariants ===
    - 0 <= stored <= volume_capacity
    - volume_capacity > 0
    - route[0] == depot

    === Sample Usage ===
    >>> t = Truck(1200, 10, 'Toronto')
    >>> t.id_ == 1200
    True
    >>> t.volume_capacity == 10
    True
    >>> p1 = Parcel(1, 2, 'Toronto', 'Ottawa')
    >>> p2 = Parcel(2, 3, 'Toronto', 'Ottawa')
    >>> t.pack(p1)
    True
    >>> t.pack(p2)
    True
    >>> t.fullness()
    50.0
    """
    id_: int
    volume_capacity: int
    depot: str
    stored: int
    route: List[str]
    parcels: List[Parcel]

    def __init__(self, id_: int, volume_capacity: int, depot: str) -> None:
        """Create a Truck. A Truck will always initially be empty and will
        always start at the depot."""

        self.id_ = id_
        self.volume_capacity = volume_capacity
        self.depot = depot
        self.stored = 0
        self.route = [self.depot]
        self.parcels = []

    def packable(self, parcel: Parcel) -> bool:
        """
        return True if it is possible to pack <parcel> onto the truck.
        >>> t = Truck(1000, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Ottawa')
        >>> p2 = Parcel(2, 6, 'Toronto', 'Calgary')
        >>> t.packable(p1)
        True
        >>> t.packable(p2)
        True
        >>> t.pack(p1)
        True
        >>> t.pack(p2)
        False
        >>> t.route[-1]
        'Ottawa'
        >>> t.fullness()
        50.0
        """
        return parcel.volume + self.stored <= self.volume_capacity

    def pack(self, parcel: Parcel) -> bool:
        """Pack the Truck with a Parcel, return True if it has been
        successfully packed. Return False if stored exceeds
        volume_capacity.
        Add the parcel's destination to the end of the Truck's route unless the
        LAST item is equal to the destination.
        >>> t = Truck(1000, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Ottawa')
        >>> p2 = Parcel(2, 6, 'Toronto', 'Calgary')
        >>> t.pack(p1)
        True
        >>> t.pack(p2)
        False
        >>> t.route[-1]
        'Ottawa'
        >>> t.fullness()
        50.0
        """
        # First, check if there's enough space to fit the parcel.
        if self.packable(parcel):
            # Add the parcel to the Truck.
            self.stored += parcel.volume
            self.parcels.append(parcel)
            # Don't modify route if the last item is the same as the
            # parcel's destination.
            if self.route[-1] != parcel.destination:
                self.route.append(parcel.destination)
            return True
        # At this point we know the parcel doesn't fit.
        return False

    def fullness(self) -> float:
        """Return the percentage of a Truck's fullness.
        >>> t = Truck(1000, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Ottawa')
        >>> p2 = Parcel(1, 5, 'Toronto', 'Calgary')
        >>> t.pack(p1)
        True
        >>> t.pack(p2)
        True
        >>> t.fullness()
        100.0
        """
        return (100 * self.stored) / self.volume_capacity

    def distance(self, dmap: DistanceMap) -> int:
        """calculate the distance travelled by this truck, with data from <dmap>

        >>> t = Truck(1333, 10, 'Toronto')
        >>> p = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t.pack(p)
        True
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> t.distance(m)
        18
        """
        i = 0
        d_total = 0
        while i < len(self.route) - 1:
            dist = dmap.distance(self.route[i], self.route[i + 1])
            if dist > 0:
                d_total += dmap.distance(self.route[i], self.route[i + 1])
            i += 1
        # the truck needs to return to depot at the end of route
        final = dmap.distance(self.route[i], self.depot)
        if self.route[i] != self.depot and final > 0:
            d_total += final
        return d_total


class Fleet:
    """ A fleet of trucks for making deliveries.
    ===== Public Attributes =====
    trucks:
      List of all Truck objects in this fleet.
    """
    trucks: List[Truck]

    def __init__(self) -> None:
        """Create a Fleet with no trucks.

        >>> f = Fleet()
        >>> f.num_trucks()
        0
        """
        self.trucks = []

    def add_truck(self, truck: Truck) -> None:
        """Add <truck> to this fleet.

        Precondition: No truck with the same ID as <truck> has already been
        added to this Fleet.
        >>> f = Fleet()
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> f.add_truck(t)
        >>> f.num_trucks()
        1
        """
        self.trucks.append(truck)

    # We will not test the format of the string that you return -- it is up
    # to you.
    def __str__(self) -> str:
        """Produce a string representation of this fleet

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> print(f)
        Information of all trucks in the fleet:
        ID: 1423; Depot: Toronto; Storage: 0/10; Route: ['Toronto']
        Total: 1 truck(s)
        """
        info = 'Information of all trucks in the fleet:'
        for truck in self.trucks:
            info = info + '\n' + f'ID: {truck.id_}; Depot: {truck.depot}; ' \
                                 f'Storage: {truck.stored}/' \
                                 f'{truck.volume_capacity}; ' \
                                 f'Route: {truck.route}'

        info += f'\nTotal: {self.num_trucks()} truck(s)'
        return info

    def num_trucks(self) -> int:
        """Return the number of trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> f.num_trucks()
        1
        """
        return len(self.trucks)

    def num_nonempty_trucks(self) -> int:
        """Return the number of non-empty trucks in this fleet.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t1)
        >>> p1 = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> p2 = Parcel(2, 4, 'Toronto', 'Montreal')
        >>> t1.pack(p2)
        True
        >>> t1.fullness()
        90.0
        >>> t2 = Truck(5912, 20, 'Toronto')
        >>> f.add_truck(t2)
        >>> p3 = Parcel(3, 2, 'New York', 'Windsor')
        >>> t2.pack(p3)
        True
        >>> t2.fullness()
        10.0
        >>> t3 = Truck(1111, 50, 'Toronto')
        >>> f.add_truck(t3)
        >>> f.num_nonempty_trucks()
        2
        """
        count = 0
        for truck in self.trucks:
            if truck.stored != 0:
                count += 1
        return count

    def parcel_allocations(self) -> Dict[int, List[int]]:
        """Return a dictionary in which each key is the ID of a truck in this
        fleet and its value is a list of the IDs of the parcels packed onto it,
        in the order in which they were packed.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(27, 5, 'Toronto', 'Hamilton')
        >>> p2 = Parcel(12, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t1.pack(p2)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p3 = Parcel(28, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p3)
        True
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.parcel_allocations() == {1423: [27, 12], 1333: [28]}
        True
        """
        allocations = {}
        for truck in self.trucks:
            allocations[truck.id_] = []
            for parcel in truck.parcels:
                allocations[truck.id_].append(parcel.id_)
        return allocations

    def total_unused_space(self) -> int:
        """Return the total unused space, summed over all non-empty trucks in
        the fleet.
        If there are no non-empty trucks in the fleet, return 0.

        >>> f = Fleet()
        >>> f.total_unused_space()
        0
        >>> t = Truck(1423, 1000, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.total_unused_space()
        995
        """
        unused_space = 0
        for truck in self.trucks:
            stored = truck.stored
            if stored != 0:
                unused_space += (truck.volume_capacity - stored)
        return unused_space

    def _total_fullness(self) -> float:
        """Return the sum of truck.fullness() for each non-empty truck in the
        fleet. If there are no non-empty trucks, return 0.

        >>> f = Fleet()
        >>> f._total_fullness() == 0.0
        True
        >>> t = Truck(1423, 10, 'Toronto')
        >>> f.add_truck(t)
        >>> f._total_fullness() == 0.0
        True
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f._total_fullness()
        50.0
        """
        flt_fullness = 0
        for truck in self.trucks:
            flt_fullness += truck.fullness()
        return flt_fullness

    def average_fullness(self) -> float:
        """Return the average percent fullness of all non-empty trucks in the
        fleet.

        Precondition: At least one truck is non-empty.

        >>> f = Fleet()
        >>> t = Truck(1423, 10, 'Toronto')
        >>> p = Parcel(1, 5, 'Buffalo', 'Hamilton')
        >>> t.pack(p)
        True
        >>> f.add_truck(t)
        >>> f.average_fullness()
        50.0
        """
        return self._total_fullness() / self.num_nonempty_trucks()

    def total_distance_travelled(self, dmap: DistanceMap) -> int:
        """Return the total distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.

        Precondition: <dmap> contains all distances required to compute the
                      average distance travelled.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.total_distance_travelled(m)
        36
        """
        total_d = 0
        for truck in self.trucks:
            dist = truck.distance(dmap)
            if dist > 0:
                total_d += dist
        return total_d

    def average_distance_travelled(self, dmap: DistanceMap) -> float:
        """Return the average distance travelled by the trucks in this fleet,
        according to the distances in <dmap>.
        Include in the average only trucks that have actually travelled some
        non-zero distance.

        === Preconditions ===
        - <dmap> contains all distances required to compute the average
          distance travelled.
        - At least one truck has travelled a non-zero distance.

        >>> f = Fleet()
        >>> t1 = Truck(1423, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Hamilton')
        >>> t1.pack(p1)
        True
        >>> t2 = Truck(1333, 10, 'Toronto')
        >>> p2 = Parcel(2, 5, 'Toronto', 'Hamilton')
        >>> t2.pack(p2)
        True
        >>> m = DistanceMap()
        >>> m.add_distance('Toronto', 'Hamilton', 9)
        >>> f.add_truck(t1)
        >>> f.add_truck(t2)
        >>> f.average_distance_travelled(m)
        18.0
        """
        total = self.total_distance_travelled(dmap)
        if total == 0:
            return 0
        count = 0
        for truck in self.trucks:
            # Only add trucks that have travelled a non-zero distance.
            if truck.distance(dmap) > 0:
                count += 1
        return total / count


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
    import doctest
    doctest.testmod()
