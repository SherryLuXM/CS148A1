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
from typing import List, Dict, Union
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
    The random algorithm will go through the parcels in random order. For each
    parcel, it will schedule it onto a randomly chosen truck (from among those
    trucks that have capacity to add that parcel). Because of this randomness,
    each time you run your random algorithm on a given problem, it may generate
    a different solution.
    """

    def __init__(self) -> None:
        """initialize RandomScheduler"""

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
        shuffle(parcels)  # ensure the for loop will go through
        # parcels in random order
        for parcel in parcels:
            # generate a list of possible trucks;
            packable = []
            for truck in trucks:
                if truck.packable(parcel):
                    packable.append(truck)
            if not packable:  # if no trucks available for this
                # parcel, record parcel to <unpacked>
                unpacked.append(parcel)
            else:
                truck_select = choice(trucks)  # truck is randomly chosen
                truck_select.pack(parcel)
        return unpacked


class GreedyScheduler(Scheduler):
    """
    The greedy algorithm tries to be more strategic. Like the random algorithm,
    it processes parcels one at a time, picking a truck for each, but it tries
    to pick the “best” truck it can for each parcel. Our greedy algorithm is
    quite short-sighted: it makes each choice without looking ahead to possible
    consequences of the choice (that’s why we call it “greedy”).
    The greedy algorithm has two configurable features: the order in which
    parcels are considered, and how a truck is chosen for each parcel. These
    are described below.
    Parcel order:
    There are four possible orders that the algorithm could use to process the
    parcels:
    - In order by parcel volume, either smallest to largest (non-decreasing) or
        largest to smallest (non-increasing).
    - In order by parcel destination, either smallest to largest
        (non-decreasing) or largest to smallest (non-increasing).
    Since destinations are strings, larger and smaller is determined by
    comparing strings (city names) alphabetically.
    Ties are broken using the order in which the parcels are read from our data
    file (see below).
    Truck choice:
    When the greedy algorithm processes a parcel, it must choose which truck to
    assign it to. The algorithm first does the following to compute the
    eligible trucks:
    It only considers trucks that have enough unused volume to add the parcel.
    Among these trucks, if there are any that already have the parcel’s
    destination at the end of their route, only those trucks are considered.
    Otherwise, all trucks that have enough unused volume are considered.
    Given the eligible trucks, the algorithm can be configured one of two ways
    to make a choice:
    - choose the eligible truck with the most available space, or
    - choose the eligible truck with the least available space
    Ties are broken using the order in which the trucks are read from our data
    file. If there are no eligible trucks, then the parcel is not scheduled
    onto any truck.
    Observations about the Greedy Algorithm:
    Since there are four options for parcel priority and two options for truck '
    choice, our greedy algorithm can be configured eight different ways in
    total.
    Notice that there is no randomness in the greedy algorithm; it is
    completely “deterministic”. This means that no matter how many times you
    run your greedy algorithm on a given problem, it will always generate the
    same solution.
    === Public Attributes ===
    parcel_priority: either ‘volume’ or ‘destination’
    parcel_order: either ‘non-decreasing’ (meaning we process parcels in order
                    from smallest to largest), or
                    ‘non-increasing’ (meaning we process parcels in order from
                    largest to smallest).
    truck_order: either ‘non-decreasing’ (meaning we choose the eligible truck
                    with the least available space, and as go through the
                    parcels we will choose trucks with greater available space),
                    or ‘non-increasing’ (meaning we choose the eligible truck
                    with the most available space, and as we go through the
                    parcels we will choose trucks with less available space).
    """
    config: Dict[str, str]
    parcel_priority: str
    parcel_order: str
    truck_order: str

    def __init__(self, config: Dict[str, str]) -> None:
        """initialize GreedyScheduler"""
        self.config = config
        self.parcel_priority = config['parcel_priority']
        self.parcel_order = config['parcel_order']
        self.truck_order = config['truck_order']

    def schedule(self, parcels: List[Parcel], trucks: List[Truck],
                 verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks> by Parcel
        priority, parcel order, and truck order """
        unpacked = []
        # ---- volume configuration ----
        if self.parcel_priority == 'volume':
            # Order parcels following configurations
            ordered_parcels = self._order_parcels_volume(parcels)
            # Loop over our ordered list of parcels until there are
            # none left.
            while not ordered_parcels.is_empty():
                # Create an ordered truck list and reorder it every
                # iteration so new data gets updated
                ordered_trucks = self._order_trucks(trucks)
                # Remove the top parcel of our list and store it in
                # a new variable
                priority_parcel = ordered_parcels.remove()
                # Create a list of trucks that our Parcel fits in,
                # stored in backwards order of priority, meaning
                # the first item is the highest priority.
                eligible_trucks = _list_packable(ordered_trucks,
                                                 priority_parcel)
                # If our Parcel doesn't fit in any truck, append it
                # to the unpacked list
                if not eligible_trucks:
                    unpacked.append(priority_parcel)
                else:
                    # Check if the destination of our Parcel matches
                    # with the last item in a truck route, if not, just
                    # pack the parcel into the top truck.
                    priority_truck = _check_same_locations(eligible_trucks,
                                                           priority_parcel)
                    priority_truck.pack(priority_parcel)

        # ---- destination configuration ----
        if self.parcel_priority == 'destination':
            ordered_parcels = self._order_parcels_destination(parcels)
            while not ordered_parcels.is_empty():
                ordered_trucks = self._order_trucks(trucks)
                priority_parcel = ordered_parcels.remove()
                eligible_trucks = _list_packable(ordered_trucks,
                                                 priority_parcel)
                if not eligible_trucks:
                    unpacked.append(priority_parcel)
                else:
                    priority_truck = _check_same_locations(eligible_trucks,
                                                           priority_parcel)
                    priority_truck.pack(priority_parcel)
        return unpacked

    # ----- Helper methods for Parcels -----

    def _order_parcels_volume(self, parcels: List[Parcel]) \
            -> Union[PriorityQueue, None]:
        """Order the parcels based on volume configuration in either
        non-decreasing or non-increasing order."""
        if self.parcel_order == 'non-decreasing':
            ordered_parcels = PriorityQueue(_parcel_volume_non_decreasing)
            for parcel in parcels:
                ordered_parcels.add(parcel)
            return ordered_parcels
        if self.parcel_order == 'non-increasing':
            ordered_parcels = PriorityQueue(_parcel_volume_non_increasing)
            for parcel in parcels:
                ordered_parcels.add(parcel)
            return ordered_parcels
        return None

    def _order_parcels_destination(self, parcels: List[Parcel]) \
            -> Union[PriorityQueue, None]:
        """Order the parcels based on destination configuration in
        either non-decreasing or non-increasing order."""
        if self.parcel_order == 'non-decreasing':
            ordered_parcels = PriorityQueue(_parcel_destination_non_decreasing)
            for parcel in parcels:
                ordered_parcels.add(parcel)
            return ordered_parcels
        if self.parcel_order == 'non-increasing':
            ordered_parcels = PriorityQueue(_parcel_destination_non_increasing)
            for parcel in parcels:
                ordered_parcels.add(parcel)
            return ordered_parcels
        return None

    # ----- Helper methods for trucks -----

    def _order_trucks(self, trucks: List[Truck]) \
            -> Union[PriorityQueue, None]:
        """Order trucks in either non-decreasing or non-increasing
        order."""
        if self.truck_order == 'non-decreasing':
            ordered_trucks = PriorityQueue(_truck_least_available_space)
            for truck in trucks:
                ordered_trucks.add(truck)
            return ordered_trucks
        if self.truck_order == 'non-increasing':
            ordered_trucks = PriorityQueue(_truck_most_available_space)
            for truck in trucks:
                ordered_trucks.add(truck)
            return ordered_trucks
        return None


def _check_same_locations(trucks: List[Truck], parcel: Parcel) -> List[Truck]:
    """Filter trucks from <trucks> that share parcel's destination.
    
    add a doctest below for having one elible truck, and for having none
    """
    eligible = []
    for truck in trucks:
        if truck.route[-1] == parcel.destination:
            eligible.append(truck)
    return eligible


def _list_packable(trucks: PriorityQueue, parcel: Parcel) \
        -> List[Truck]:
    """Return a list of all packable trucks with respect to one Parcel."""
    eligible_trucks = []
    while not trucks.is_empty():
        priority_truck = trucks.remove()
        if priority_truck.packable(parcel):
            eligible_trucks.append(priority_truck)
    return eligible_trucks


def _parcel_volume_non_decreasing(p1: Parcel, p2: Parcel) -> bool:
    """Return if Parcel p1 is smaller in volume than Parcel p2.
    >>> parcel_1 = Parcel(1, 2, 'Toronto', 'Ottawa')
    >>> parcel_2 = Parcel(2, 3, 'Toronto', 'Ottawa')
    >>> _parcel_volume_non_decreasing(parcel_1, parcel_2)
    True
    """
    return p1.volume < p2.volume


def _parcel_volume_non_increasing(p1: Parcel, p2: Parcel) -> bool:
    """Return if Parcel p1 is larger in volume than Parcel p2.
    >>> parcel_1 = Parcel(1, 3, 'Toronto', 'Ottawa')
    >>> parcel_2 = Parcel(2, 2, 'Toronto', 'Ottawa')
    >>> _parcel_volume_non_increasing(parcel_1, parcel_2)
    True
    """
    return p1.volume > p2.volume


def _parcel_destination_non_decreasing(p1: Parcel, p2: Parcel) -> bool:
    """Return if Parcel p1 is smaller alphabetically than Parcel p2.
    >>> parcel_1 = Parcel(1, 2, 'Toronto', 'Calgary')
    >>> parcel_2 = Parcel(2, 3, 'Toronto', 'Ottawa')
    >>> _parcel_destination_non_decreasing(parcel_1, parcel_2)
    True
    """
    return p1.destination < p2.destination


def _parcel_destination_non_increasing(p1: Parcel, p2: Parcel) -> bool:
    """Return if Parcel p1 is larger alphabetically than Parcel p2.
    >>> parcel_1 = Parcel(1, 2, 'Toronto', 'Calgary')
    >>> parcel_2 = Parcel(2, 3, 'Toronto', 'Ottawa')
    >>> _parcel_destination_non_decreasing(parcel_1, parcel_2)
    True
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
