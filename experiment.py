"""Assignment 1 - Running experiments (Task 5)

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

This module contains class SchedulingExperiment.  It can create an experiment
with input data and an algorithm configuration specified in a dictionary, then
run the experiment, generate statistics as the result of the experiment, and
(optionally) report the statistics.

This module is responsible for all the reading of data from the data files.
"""
from typing import List, Dict, Union
import json
from scheduler import RandomScheduler, GreedyScheduler, Scheduler
from domain import Parcel, Truck, Fleet
from distance_map import DistanceMap


class SchedulingExperiment:
    """An experiment in scheduling parcels for delivery.

    To complete an experiment involves four stages:

    1. Read in all data from necessary files, and create corresponding objects.
    2. Run a scheduling algorithm to assign parcels to trucks.
    3. Compute statistics showing how good the assignment of parcels to trucks
       is.
    4. Report the statistics from the experiment.

    === Public Attributes ===
    verbose:
      If <verbose> is True, print step-by-step details regarding the scheduling
      algorithm as it runs.
    scheduler:
      The scheduler to use in this experiment.
    parcels:
      The parcels to schedule in this experiment.
    fleet:
      The trucks that parcels are scheduled to in this experiment.
    dmap:
      The distances between cities in this experiment.

    === Private Attributes ===
    _stats:
      A dictionary of statistics. <_stats>'s value is undefined until
      <self>._compute_stats is called, at which point it contains keys and
      values as specified in Step 6 of Assignment 1.
    _unscheduled:
      A list of parcels. <_unscheduled>'s value is undefined until <self>.run
      is called, at which point it contains the list of parcels that could
      not be scheduled in the experiment.

    === Representation Invariants ===
    - <fleet> contains at least one truck
    - <dmap> contains all of the distances required to compute the length of
      any possible route for the trucks in <fleet> delivering the packages in
      <parcels>.
    """
    verbose: bool
    scheduler: Scheduler
    parcels: List[Parcel]
    fleet: Fleet
    dmap: DistanceMap
    _stats: Dict[str, Union[int, float]]
    _unscheduled: List[Parcel]

    def __init__(self, config: Dict[str, Union[str, bool]]) -> None:
        """Initialize a new experiment with the configuration specified in
        <config>.

        Precondition: <config> contains keys and values as specified
        in Assignment 1.
        """
        self.verbose = config['verbose']
        if config['algorithm'] == 'random':
            self.scheduler = RandomScheduler()
        else:
            self.scheduler = GreedyScheduler(config)
        self.parcels = read_parcels(config['parcel_file'])
        self.fleet = read_trucks(config['truck_file'],
                                 config['depot_location'])
        self.dmap = read_distance_map(config['map_file'])

        self._stats = {}
        self._unscheduled = []

    def run(self, report: bool = False) -> Dict[str, Union[int, float]]:
        """Run the experiment and return statistics on the outcome.

        If <report> is True, print a report on the statistics from this
        experiment.  Either way, return the statistics in a dictionary.

        If <self.verbose> is True, print step-by-step details
        regarding the scheduling algorithm as it runs.
        """
        trks = self.fleet.trucks
        vbose = self.verbose
        self._unscheduled = self.scheduler.schedule(self.parcels, trks, vbose)
        self._compute_stats()
        if report:
            self._print_report()
        return self._stats

    def _compute_stats(self) -> None:
        """Compute the statistics for this experiment, and store in
        <self>.stats.
        - fleet: the number of trucks in the fleet.
        - unused_trucks: the number of empty trucks.
        - avg_distance: among the used trucks, the average distance they will
        have to travel to follow their scheduled route.
        - avg_fullness: among the used trucks, their average fullness. The
        fullness of a truck is the percentage of its volume that is taken by
        parcels.
        - unused_space: among the used trucks, their total unused space. The
        unused space of a truck is the amount (not percentage) of its volume
        that is not taken by parcels.
        - unscheduled: the number of unscheduled parcels (parcels that did not
        fit onto any truck).
        Precondition: _run has already been called.
        """
        flt = self.fleet
        self._stats = {
            'fleet': flt.num_trucks(),
            'unused_trucks': flt.num_trucks() - flt.num_nonempty_trucks(),
            'avg_distance': flt.average_distance_travelled(self.dmap),
            'avg_fullness': flt.average_fullness(),
            'unused_space': flt.total_unused_space(),
            'unscheduled': len(self._unscheduled)
        }

    def _print_report(self) -> None:
        """Report on the statistics for this experiment.
        Precondition: _compute_stats has already been called.
        """
        stat = self._stats
        info = f'Experiment Statistics: '\
               f'{stat["fleet"]} truck(s) in the fleet' \
               f'{stat["unused_trucks"]} unused truck(s)' \
               f'Truck(s) travel {stat["avg_distance"]} unit(s) on average.' \
               f'Average fullness of used truck(s) is {stat["avg_fullness"]}%' \
               f'Total unused space on used trucks are {stat["unused_space"]}' \
               f'Undelivered parcels: {stat["unscheduled"]}'
        print(info)


# ----- Helper functions -----


def read_parcels(parcel_file: str) -> List[Parcel]:
    """Read parcel data from <parcel_file> and return.
    Parcel file format: <parcel_id>, <source>, <destination>, <parcel_volume>
    Precondition: <parcel_file> is the path to a file containing parcel data in
                  the form specified in Assignment 1.
    """
    plist = []
    # read and add the parcels to the list.
    with open(parcel_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            pid = int(tokens[0].strip())
            source = tokens[1].strip()
            destination = tokens[2].strip()
            volume = int(tokens[3].strip())
            plist.append(Parcel(pid, volume, source, destination))
    return plist


def read_distance_map(distance_map_file: str) -> DistanceMap:
    """Read distance data from <distance_map_file> and return a DistanceMap
    that records it.
    Map file format: <city1>, <city2>, <distance1> [, <distance2> ]
    === Preconditions ===
    <distance_map_file> is the path to a file containing distance data in the
    form specified in Assignment 1.
    """
    dmap = DistanceMap()
    with open(distance_map_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            c1 = tokens[0].strip()
            c2 = tokens[1].strip()
            distance1 = int(tokens[2].strip())
            distance2 = int(tokens[3].strip()) if len(tokens) == 4 \
                else distance1
            dmap.add_distance(c1, c2, distance1, distance2)
    return dmap


def read_trucks(truck_file: str, depot_location: str) -> Fleet:
    """Read truck data from <truck_file> and return a Fleet containing these
    trucks, with each truck starting at the <depot_location>.
    Truck file format: <truck_id>, <truck_volume>
    === Preconditions ===
    <truck_file> is a path to a file containing truck data in the form specified
     in Assignment 1.
    Truck IDs may occur in any order and need not be consecutive, but no truck
    ID occurs more than once in the file.
    """
    flt = Fleet()
    with open(truck_file, 'r') as file:
        for line in file:
            tokens = line.strip().split(',')
            tid = int(tokens[0])
            capacity = int(tokens[1])
            flt.add_truck(Truck(tid, capacity, depot_location))
    return flt


def simple_check(config_file: str) -> None:
    """Configure and run a single experiment on the scheduling problem
    defined in <config_file>.
    Precondition: <config_file> is a json file with keys and values
    as in the dictionary format defined in Assignment 1.
    """
    # Read an experiment configuration from a file and build a dictionary
    with open(config_file, 'r') as file:
        configuration = json.load(file)
    # Create and run an experiment with that configuration.
    experiment = SchedulingExperiment(configuration)
    experiment.run(report=True)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['read_parcels', 'read_distance_map', 'read_trucks',
                       '_print_report', 'simple_check'],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'json', 'scheduler', 'domain',
                                   'distance_map'],
        'disable': ['E1136'],
        'max-attributes': 15,
    })

    # ------------------------------------------------------------------------
    # The following code can be used as a quick and simple check to see if your
    # experiment can run without errors.
    # ------------------------------------------------------------------------
    simple_check('data/demo.json')
