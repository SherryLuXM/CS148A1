<div id="top"></div>


<h3 align="center"> Parcel Delivery Scheduling Algorithm in Python</h3>
  <p align="center">
  Computer science project completed in 2021
  </p>
</div>


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#File-guide">File guide</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#system-structure">System structure</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


## About The Project

This project showcases through knowledge with class design and implementation in Python, capacity to understand and work with complex code, and use of quenes, unit-testing, and Abstract Data Type. 

My team builds a system to schedule and optimize parcel delivery based on constraints like truck availability, parcel sizes, depot location, parcel destinations, to schedule the most efficient routes. A random delivery-scheduling algorithm was first implemented as a baseline, then we develop a greedy optimization algorithm that gives much better results.

Specifically, the project requires understanding of composition and inheritance, and implementation of classes and subclasses with attributes, representation invariants, preconditions, methods, and appropriate interface and data structure. We work with existing data to build the most reasonable and functional sets of classes and methods, which support an algorithm that can produce a definite and optimized solution for the parcel delivery problem.

### Built With
Python

### File Guide
* a1_starter_tests.py: contains unit tests;
* experiment.py: contains class SchedulingExperiment;
* distance_map.py: contains class DistanceMap that allows clients to look up or store distance between two cities;
* domain.py: contains classes Parcel, Truck, and Fleet;
* container.py: contains class Container and a child class PriorityQueue;
* scheduler.py: contains an abstract class Scheduler and two subclasses RandomScheduler and GreedyScheduler;
* explore.py: compares all algorithms;
* generator.py: creates random truck and parcel data and writes them to file;
* A1 Handout.pdf: assignment requirements and instructions;
* LICENSE: MIT License for the project.


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

The code can be referenced for implementing classes, subclasses, and methods in Python, for writing algorithms that generate data or unit tests, or compute optimized solutions, and for doing algorithm comparison. 

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- System structure -->
## System structure
Class, subclass, and notable functions
- SchedulingExperiment
- DistanceMap
- Parcel
- Truck
    - packable()
    - pack()
    - fullness()
    - distance()
- Fleet
    - add_truck()
    - num_trucks()
    - num_nonempty_trucks()
    - parcel_allocations()
    - total_unused_space()
    - \_total_fullness()
    - average_fullness()
    - total_distance_travelled()
    - average_distance_travelled()
- Container
  - PriorityQueue
- Scheduler
  - RandomScheduler
  - GreedyScheduler

<p align="right">(<a href="#top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Sherry Xiaoman Lu - sherry.luxiaoman@gmail.com
[![LinkedIn][linkedin-shield]][linkedin-url]

Project Link: [https://github.com/SherryLuXM/CS148A1.git](https://github.com/SherryLuXM/CS148A1.git)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* This is the first assignment from CSC148H1 S 20211: Introduction to Computer Science, taken during the Winter 2020-2021 semester, at the St.George Campus, at University of Toronto, taught by Professor Diane Horton. The experiment.py, explore.py, and generator.py are mostly if not all written by the course staffs, while they provided frameworks and guidances for coding the other files. 

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/sherry-l-633854132/
