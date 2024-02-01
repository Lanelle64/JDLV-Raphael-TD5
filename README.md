# JDLV-Raphael-TD5
[Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life), also known as Conway's Life, is a cellular automaton invented by the British mathematician John Horton Conway. It is a playerless game that takes place on a two-dimensional grid composed of cells. Each cell can be in one of two states: alive or dead.

The rules of the game are simple:

- **Survival**: A live cell with 2 or 3 live neighbors survives to the next generation. Otherwise, it dies due to isolation or overcrowding.

- **Birth**: A dead cell surrounded exactly by 3 live cells becomes alive in the next generation.

The game evolves according to these rules in each generation, creating complex and fascinating configurations. Players can observe the game's evolution from a given initial configuration or create their own configurations to see how they develop.

Conway's Game of Life is interesting due to its simplicity and the complexity that can emerge from it. It is often used as an example of a deterministic dynamical system, where simple rules lead to complex and unpredictable behaviors.

## Features:
Multiple populations can be created for the same Game of Life, competing for their territory!

Customizable parameters such as board size, number and size of populations, etc.

## Setup/Troubleshoot
Simply clone this GitHub repository and run JDLV.py! To run it, open the file in VS Code or execute it from the terminal with:
`python3 {path_to_file}\JDLV.py`

Install the required dependencies:
```
pip install numpy
```
```
pip install colorama
```

## Possible Additions and Improvements
- Add a visual interface, such as a GUI
- Improve the presentation by displaying an ASCII title and formatting questions
- Clear the console at each generation for better 'animation'
- Add colors for different populations
- Introduce new features!

## Authors
Raphael Michon - Base Project    
Emma K - Documentation, Translation    
Seb Moine - Enhancement, bug fix    
*Add your name here with your contribution*

## License
This project is licensed under the MIT License - see the [License file](LICENSE) for details
