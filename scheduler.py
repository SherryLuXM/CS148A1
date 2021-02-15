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
from typing import List, Dict, Union, Callable
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
    The random algorithm will go through the parcels in random order. For each parcel, it will schedule it onto a
    randomly chosen truck (from among those trucks that have capacity to add that parcel). Because of this randomness,
    each time you run your random algorithm on a given problem, it may generate a different solution.
    """

    def schedule(self, parcels: List[Parcel], trucks: List[Truck], verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks> randomly"""
        pass


class GreedyScheduler(Scheduler):
    """
    The greedy algorithm tries to be more strategic. Like the random algorithm, it processes parcels one at a time,
    picking a truck for each, but it tries to pick the “best” truck it can for each parcel. Our greedy algorithm is
    quite short-sighted: it makes each choice without looking ahead to possible consequences of the choice (that’s why
    we call it “greedy”).

    The greedy algorithm has two configurable features: the order in which parcels are considered, and how a truck is
    chosen for each parcel. These are described below.

    Parcel order
    There are four possible orders that the algorithm could use to process the parcels:
    In order by parcel volume, either smallest to largest (non-decreasing) or largest to smallest (non-increasing).
    In order by parcel destination, either smallest to largest (non-decreasing) or largest to smallest (non-increasing).
    Since destinations are strings, larger and smaller is determined by comparing strings (city names) alphabetically.
    Ties are broken using the order in which the parcels are read from our data file (see below).

    Truck choice
    When the greedy algorithm processes a parcel, it must choose which truck to assign it to. The algorithm first does
    the following to compute the eligible trucks:

    It only considers trucks that have enough unused volume to add the parcel.
    Among these trucks, if there are any that already have the parcel’s destination at the end of their route, only
    those trucks are considered. Otherwise, all trucks that have enough unused volume are considered.
    Given the eligible trucks, the algorithm can be configured one of two ways to make a choice:

    choose the eligible truck with the most available space, or
    choose the eligible truck with the least available space
    Ties are broken using the order in which the trucks are read from our data file. If there are no eligible trucks,
    then the parcel is not scheduled onto any truck.

    Observations about the Greedy Algorithm
    Since there are four options for parcel priority and two options for truck choice, our greedy algorithm can be
    configured eight different ways in total.

    Notice that there is no randomness in the greedy algorithm; it is completely “deterministic”. This means that no
    matter how many times you run your greedy algorithm on a given problem, it will always generate the same solution.
    === Public Attributes ===
    parcel_priority: either ‘volume’ or ‘destination’
    parcel_order: either ‘non-decreasing’ (meaning we process parcels in order from smallest to largest), or
                    ‘non-increasing’ (meaning we process parcels in order from largest to smallest).
    truck_order: either ‘non-decreasing’ (meaning we choose the eligible truck with the least available space, and as
    go through the parcels we will choose trucks with greater available space), or ‘non-increasing’ (meaning we choose
    the eligible truck with the most available space, and as we go through the parcels we will choose trucks with less
    available space).
    """
    parcel_priority: str
    parcel_order: str
    truck_order: str

    def __init__(self, parcel_priority: str, parcel_order: str, truck_order: str) -> None:
        """initialize GreedyScheduler"""
        self.parcel_priority = parcel_priority
        self.parcel_order = parcel_order
        self.truck_order = truck_order


    def schedule(self, parcels: List[Parcel], trucks: List[Truck], verbose: bool = False) -> List[Parcel]:
        """Schedule the given <parcels> onto the given <trucks> by Parcel priority, parcel order, and truck order"""
        pass


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
