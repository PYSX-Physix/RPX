# RPX Game Engine Documentation

## Overview
This RPX Game Engine is built using PyGlet, a Python library for creating games and multimedia applications. The game engine features various scenes, character interactions, and immersive environments.

## Project Structure
```
rpg-game
├── src
│   ├── main.py                # Entry point of the game
│   ├── assets                 # Directory for game assets
│   │   ├── characters         # Character sprites and animations
│   │   ├── environments       # Background images and environment assets
│   │   └── sounds             # Sound effects and music files
│   ├── scenes                 # Game scenes
│   │   ├── menu.py            # Main menu scene
│   │   ├── game.py            # Main gameplay scene
│   │   ├── game_over.py       # Game over scene
|   |   └── settings.py        # Settings scene
│   └── utils                  # Utility functions
│       └── helpers.py         # Helper functions for asset management
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── .gitignore                 # Git ignore file
```

## Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd RPX
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python src/main.py
   ```

## Gameplay Details
- Navigate through the main menu to start the game or exit.
- Control your character in the game scene, interact with enemies, and explore various environments.
- Upon losing, you will be directed to the game over scene where you can choose to restart or exit.

## Credits
- Developed using PyGlet.
- Special thanks to the open-source community for their contributions.