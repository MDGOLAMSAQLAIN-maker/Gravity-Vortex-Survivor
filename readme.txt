# Gravity Vortex Survivor

## Overview
Gravity Vortex Survivor is a 2D space survival game built using Python and Pygame. Players control a spaceship navigating through space, avoiding gravitational hazards, collecting energy cores, and surviving as long as possible.

## Features
- **Realistic Gravity Mechanics**: The ship experiences gravitational pull from planets and must counteract it with thrust.
- **Physics-based Movement**: Ship movement follows inertia, rotation, and thrust mechanics.
- **Dynamic Environment**: Planets exert gravitational force, and objects like fuel pods and energy cores appear randomly.
- **HUD Display**: Shows fuel levels, score, and ship status.
- **Game Over Conditions**: Collision with planets or depletion of fuel ends the game.
- **Screen Wrapping**: The ship can move beyond screen edges and reappear on the opposite side.
- **Randomized Elements**: Energy cores, obstacles, and power-ups spawn dynamically to keep gameplay engaging.

## Installation
### Prerequisites
Ensure you have Python installed on your system.
```sh
python --version
```
If not installed, download and install Python from [Python.org](https://www.python.org/).

### Install Dependencies
This game requires Pygame. Install it using pip:
```sh
pip install pygame
```

## How to Play
1. Run the game script:
```sh
python gravity_vortex_survivor.py
```
2. Use the arrow keys to control the spaceship:
   - **Up Arrow**: Thrust forward
   - **Left/Right Arrows**: Rotate the ship
3. Avoid crashing into planets and obstacles.
4. Collect energy cores to increase score.
5. Monitor fuel levels; running out of fuel ends the game.

## Future Enhancements
- Implementing AI-controlled obstacles.
- Adding multiplayer functionality.
- Enhancing graphics with better sprites and effects.
- Introducing new power-ups and abilities.

## Contributing
Feel free to fork the project and submit pull requests. Contributions are always welcome!

## License
This project is licensed under the MIT License.