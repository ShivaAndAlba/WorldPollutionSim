# Global Warming Model

A case study of [Cellular Atomata](https://en.wikipedia.org/wiki/Cellular_automaton) and object oriented design princepels. 

## Description

The idea came from a project in a course called "Biological Computation" in the Open University of Israel.
The simplest example of Cellular Automata is [Conwey's game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), where simple rules in a system create complex behaviors.

Here I applied the same principals to model global warming effect of pollution, its far from accurate or represents any real world model but it still repents how a 
small changes and simple rules can create big changes in a system.

examples:
1. initial state
[initial_state](./images/initial_state.png)
2. end state 
[end_state1](./images/end_state1.png)
3. diffrent end state
[end_state2](./images/end_state2.png)

In short each cell in a 2d grid has neighbors around him, at each iteration we look at a cell and the surrounding neighbors.
We calculate the surrounding neighbors effect, based on predefined factors and conditions, on the current cell and update current cell state.

Each cell is represented using [State design pattern](https://github.com/ShivaAndAlba/DesignPatterns/blob/main/Behavioral%20Patterns/State.md)(cheatsheet i made for myself).
Cells transition to next state is implemented using a queue, after full iteration over all cells, we transition all cell to next state and update gui accordingly.

### Getting Started

1. Install [NumPy](https://numpy.org/install/)
2. Clone repository:
```
git clone https://github.com/ShivaAndAlba/WorldPollutionSim.git
```
3. From WorldPollutionSim directory in cli:
```
python GWModel.py
```
4. Enjoy.

## Authors

* [ShivaAndAlba](https://github.com/ShivaAndAlba)
