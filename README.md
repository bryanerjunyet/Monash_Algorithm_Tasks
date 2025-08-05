# Monash Algorithm Tasks
## Assignment 1 - Locomotion Commotion
This module is a program for driver to determine the best driving route to intercept your friend who 
is onboard a circle train line, where the interception happens at a train station at the same time
with the least cost and earliest time.

**Algorithm & Data Structure**
- Dijsktra Search
- Multiverse Methodology
- MinHeap

**Classes Usage**
City    : A city graph with the concept of multiverse.
Location: A location in the city, which can be a regular location or a train station.
Road    : A road between two locations.
MinHeap : A MinHeap for efficient selection of the minimum cost location.

## Assignment 2
### TASK 1 - A Crowded Campus
This module section is a program for campus to allocate students to classes based on the physical class 
capacities and availability as well as student's preferred time. A Flow-Network-based approach is implemented
to model the allocation process to achieve the best proposed allocation of classes to students, where a minimum
satisfaction number of students obtain one of their top 5 preferred time slot, each student is allocated to 
exactly one class and each class meets its minimum and maximum capacity. 

**Algorithm & Data Structure**
- Network Flow
- Ford Fulkerson
- Breath-First Search

**Classes Usage**
AllocationFlow    : A flow edge in the AllocationNetwork represents a possible assignment to a decision point.
AllocationPoint   : A node in the AllocationNetwork represents a decision point in the allocation process.
AllocationNetwork : A manager class for AllocationNetwork construction and flow processing.

### TASK 2 - Typo
This module is a program for user to identify input words that have exactly 
one character substitution (Levenshtein distance of one) from the words in a
given dictionary. A Trie-based solution is implemented to efficiently store all 
dictionary words and optimise search process efficient lookup time by the Trie data structure.

**Algorithm & Data Structure**
- Trie-based Pruning

**Classes Usage**
TrieNode    : A single Trie node that contains a complete word and character links.
Bad_AI      : A Trie for efficient searching of words with one character substitution from the given dictionary. 
