# Kingdom: Classic Clone

A 2D side-scrolling strategy/management game built with Python and Pygame, inspired by *Kingdom: Classic*.

## Features
- **Exploration**: Ride your horse across a procedurally rendered land.
- **Economy**: Collect coins, manage your pouch, and invest in your kingdom.
- **Recruitment**: Turn wandering vagrants into loyal subjects.
- **Building**: Construct walls to defend and shops to equip your people.
- **Defense**: Survive nightly waves of Greed that try to steal your crown.
- **Victory**: Destroy the portals to secure your land.

## Installation

1. Ensure you have Python 3 installed.
2. Install the required dependencies:
   ```bash
   pip install pygame
   ```

## How to Run

Execute the main script:
```bash
python3 main.py
```

## Controls

- **Movement**: `Arrow Keys` or `WASD` (Left/Right)
- **Run**: Hold `Shift` while moving.
- **Interact / Drop Coin**: `Down Arrow` or `S`
    - Stand near a beggar to recruit them (1 coin).
    - Stand near a building slot to build/upgrade (variable cost).
    - Stand near a shop to buy a tool (variable cost).
    - Drop a coin on the ground for storage or distraction.

## Gameplay Guide

1. **Start**: You begin with a few coins.
2. **Recruit**: Find Vagrants in camps and drop a coin to turn them into Peasants.
3. **Equip**:
    - Build a **Bow Shop** to turn Peasants into **Archers** (they hunt for coins by day, defend by night).
    - Build a **Hammer Shop** to turn Peasants into **Builders** (they build and repair structures).
4. **Build**:
    - **Campfire**: Upgrade to a Town Center.
    - **Mounds**: Build Walls to hold back the Greed.
5. **Survive**: At night, the Greed will attack. If they hit you, you lose coins. If you have no coins, you lose your Crown.
6. **Win**: Destroy the Portals at the ends of the map.
7. **Lose**: If your Crown is stolen, the kingdom falls.

## Credits
Built as a clone for educational/demonstration purposes. Original game concept by Noio and Licorice.
