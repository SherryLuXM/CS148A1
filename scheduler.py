"""Assignment 1 - Scheduling algorithms (Task 4)
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
This module contains the abstract Scheduler class, as well as the two
subclasses RandomScheduler and GreedyScheduler, which implement the two
scheduling algorithms described in the handout.
"""
from typing import List, Dict, Callable
from random import shuffle, choice
from container import PriorityQueue
from domain import Parcel, Truck


class Scheduler:
    """A scheduler, capable of deciding what parcels go onto which trucks, and
    what route each truck will take.
    This is an abstract class.  Only child classes should be instantiated.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks>, that is, decide
        which parcels will go on which trucks, as well as the route each truck
        will take.
        Mutate the Truck objects in <trucks> so that they store information
        about which parcel objects they will deliver and what route they will
        take.  Do *not* mutate the list <parcels>, or any of the parcel objects
        in that list.
        Return a list containing the parcels that did not get scheduled onto any
        truck, due to lack of capacity.
        If <verbose> is True, print step-by-step details regarding
        the scheduling algorithm as it runs.  This is *only* for debugging
        purposes for your benefit, so the content and format of this
        information is your choice; we will not test your code with <verbose>
        set to True.
        """
        raise NotImplementedError


class RandomScheduler(Scheduler):
    """
    The random algorithm will go through the parcels in random order.
    For each parcel, it will schedule it onto a randomly chosen truck
    (from among those trucks that have capacity to add that parcel).
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks> randomly

        >>> t1 = Truck(11, 10, 'Toronto')
        >>> t2 = Truck(12, 10, 'Toronto')
        >>> t3 = Truck(13, 10, 'Toronto')
        >>> p1 = Parcel(1, 5, 'Toronto', 'Ottawa')
        >>> p2 = Parcel(2, 15, 'Toronto', 'Calgary')
        >>> random_scheduling = RandomScheduler()
        >>> random_scheduling.schedule([p1, p2],[t1, t2, t3]) == [p2]
        True
        """
        unpacked = []
        shuffle(parcels)
        # ensure the for loop will go through parcels in random order
        for parcel in parcels:
            # generate a list of possible trucks;
            packable = []
            for truck in trucks:
                if truck.packable(parcel):
                    packable.append(truck)
            # if no trucks available for the parcel, record parcel to <unpacked>
            if not packable:
                unpacked.append(parcel)
            else:
                truck_select = choice(trucks)  # truck is randomly chosen
                truck_select.pack(parcel)
        return unpacked


class GreedyScheduler(Scheduler):
    """
    A scheduler that allocate parcels to trucks based on parcel order and truck
    choice.

    === Public Attributes ===
    - parcel_method: comparison function for ordering parcel for allocation
    - truck_order: the order of trucks to get parcel allocation
    """
    config: Dict[str, str]
    par_method: Callable[[Parcel, Parcel], bool]
    truck_order: str

    def __init__(self, config: Dict[str, str]) -> None:
        """initialize GreedyScheduler"""
        self.config = config
        pf = {'non-decreasing': {'volume': _pvnd, 'destination': _pdnd},
              'non-increasing': {'volume': _pvni, 'destination': _pdni}}
        self.par_method = pf[config['parcel_order']][config['parcel_priority']]
        self.truck_order = config['truck_order']

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks> by Parcel
        priority, parcel order, and truck order """
        unpacked = []
        ordered_parcels = self._order_parcels(parcels)
        while not ordered_parcels.is_empty():
            priority_parcel = ordered_parcels.remove()
            eligible_trucks = _eligible_trucks(trucks, priority_parcel)
            if not eligible_trucks:
                unpacked.append(priority_parcel)
            else:
                ordered_trucks = self._order_trucks(eligible_trucks)
                ordered_trucks.remove().pack(priority_parcel)
        return unpacked

    # ----- Helper methods for Parcels -----

    def _order_parcels(self, parcels: List[Parcel]) -> PriorityQueue:
        """Transform the <parcels> into a Queue based on parcel_order in either
        non-decreasing or non-increasing order."""
        ordered_parcels = PriorityQueue(self.par_method)
        for parcel in parcels:
            ordered_parcels.add(parcel)
        return ordered_parcels

    # ----- Helper methods for trucks -----

    def _order_trucks(self, trucks: List[Truck]) \
            -> PriorityQueue:
        """Order trucks in either non-decreasing or non-increasing
        order."""
        ordered_trucks = PriorityQueue(_truck_most_available_space)
        if self.truck_order == 'non-decreasing':
            ordered_trucks = PriorityQueue(_truck_least_available_space)
        for truck in trucks:
            ordered_trucks.add(truck)
        return ordered_trucks


def _eligible_trucks(trucks: List[Truck], parcel: Parcel) \
        -> List[Truck]:
    """Filter eligible trucks for <parcel> from <trucks>.
    An eligible truck must have enough unused space for <parcel>.
    If there are trucks with the same last stop as the parcel destination,
    then only these trucks will be eligible.
    """
    packable_trucks = []
    for truck in trucks:
        if truck.packable(parcel):
            packable_trucks.append(truck)
    # for trucks with last stops the same as parcel destination
    eligible = []
    for truck in packable_trucks:
        if truck.route[-1] == parcel.destination:
            eligible.append(truck)
    if packable_trucks and not eligible:
        eligible = packable_trucks
    return eligible


def _pvnd(p1: Parcel, p2: Parcel) -> bool:
    """verify if <p1> is smaller in volume than <p2>.
    pvnd: parcel volume non-decreasing

    >>> parcel_1 = Parcel(1, 2, 'Toronto', 'Ottawa')
    >>> parcel_2 = Parcel(2, 3, 'Toronto', 'Ottawa')
    >>> _pvnd(parcel_1, parcel_2)
    True
    """
    return p1.volume < p2.volume


def _pvni(p1: Parcel, p2: Parcel) -> bool:
    """Return if Parcel p1 is larger in volume than Parcel p2.
    pvni: parcel volume non-increasing

    >>> parcel_1 = Parcel(1, 3, 'Toronto', 'Ottawa')
    >>> parcel_2 = Parcel(2, 2, 'Toronto', 'Ottawa')
    >>> _pvni(parcel_1, parcel_2)
    True
    """
    return p1.volume > p2.volume


def _pdnd(p1: Parcel, p2: Parcel) -> bool:
    """Return if Parcel p1 is smaller alphabetically than Parcel p2.
    pdnd: parcel destination non-decreasing

    >>> parcel_1 = Parcel(1, 2, 'Toronto', 'Calgary')
    >>> parcel_2 = Parcel(2, 3, 'Toronto', 'Ottawa')
    >>> _pdnd(parcel_1, parcel_2)
    True
    """
    return p1.destination < p2.destination


def _pdni(p1: Parcel, p2: Parcel) -> bool:
    """Return if Parcel p1 is larger alphabetically than Parcel p2.
    pdni: parcel destination non-increasing

    >>> parcel_1 = Parcel(1, 2, 'Toronto', 'Calgary')
    >>> parcel_2 = Parcel(2, 3, 'Toronto', 'Ottawa')
    >>> _pdni(parcel_1, parcel_2)
    False
    """
    return p1.destination > p2.destination


def _truck_most_available_space(t1: Truck, t2: Truck) -> bool:
    """Return if Truck t1 has more available space than Truck t2
    >>> truck_1 = Truck(1000, 15, "Toronto")
    >>> truck_2 = Truck(1100, 10, 'Toronto')
    >>> _truck_most_available_space(truck_1, truck_2)
    True
    """
    return t1.volume_capacity - t1.stored > t2.volume_capacity - t2.stored


def _truck_least_available_space(t1: Truck, t2: Truck) -> bool:
    """Return if Truck t1 has less available space than Truck t2.
    >>> truck_1 = Truck(1000, 10, "Toronto")
    >>> truck_2 = Truck(1100, 15, 'Toronto')
    >>> _truck_least_available_space(truck_1, truck_2)
    True
    """
    return t1.volume_capacity - t1.stored < t2.volume_capacity - t2.stored


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['compare_algorithms'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', 'container', 'domain'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })
