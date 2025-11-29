# Kingdom Clone - Functionality Roadmap

## 1. Core Engine & Visuals
- [ ] **Game Loop**: Main loop handling events, update, draw.
- [ ] **State Manager**: Handle transitions (Menu -> Game -> Cave -> Win/Loss).
- [ ] **Asset Generator**: Procedural pixel-art generation (drawing rects to surfaces) to mimic the aesthetic without external files.
- [ ] **Camera**: Smooth scrolling centered on player, clamped to world bounds.
- [ ] **Input Handling**: WASD/Arrows, Shift to Run, Down/S to Interact/Drop Coin.

## 2. World Generation
- [ ] **Biomes**:
    - **Plains**: Spawns Rabbits.
    - **Forest**: Spawns Deer, Treasure Chests.
- [ ] **Terrain**: Flat ground with parallax backgrounds (Sky, Mountains, Trees, Near Trees).
- [ ] **Day/Night Cycle**: Visual darkening, Moon phases (Blood Moon logic).
- [ ] **Interactables**: Spots for Buildings, Portals, Chests.

## 3. Player & Mounts
- [ ] **Player Controller**: Movement, Interaction.
- [ ] **Inventory**:
    - **Coin Pouch**: Visual overflow.
    - **Gem Pouch**: For unlocking mounts.
- [ ] **Mount System**:
    - **Default Horse**: Balanced stats.
    - **Stag**: Fast in forest, slow elsewhere.
    - **Warhorse**: High stamina, fast gallop, boosts nearby units (optional buff).
    - **Bear**: Attacks Greed? (Maybe too complex, stick to stats first).
- [ ] **Health/Loss**:
    - Hit 1: Drop Coin (if available).
    - Hit 2 (No coins): Drop Crown.
    - Crown Stolen: Game Over.

## 4. Economy & Items
- [ ] **Coin Physics**: Coins bounce, roll, and settle.
- [ ] **Gems**: Rare currency found in forest chests.
- [ ] **Income**:
    - Archers hunting (Rabbits/Deer).
    - Farmers farming.
    - Interest from Banker (optional).

## 5. Units & Jobs
- [ ] **Recruitment**: Vagrants (in camps) -> Peasants (1 coin).
- [ ] **Job System**: Peasants pick up tools to change class.
- [ ] **Archers**:
    - Weapon: Bow.
    - Day: Hunt.
    - Night: Defend behind walls.
- [ ] **Builders**:
    - Weapon: Hammer.
    - Tasks: Build/Upgrade Walls, Chop Trees, Push Boat, Push Bomb.
- [ ] **Farmers**:
    - Weapon: Scythe.
    - Task: Farm crops at Farm buildings (Day only).

## 6. Buildings
- [ ] **Campfire (Base)**:
    - Tier 1-N: Unlocks Banker, Knights, Bomb Shop.
- [ ] **Walls**: Wood -> Stone -> Iron. Blocks Greed.
- [ ] **Towers**: Wood -> Stone. protect Archers.
- [ ] **Farms**: Generates coins.
- [ ] **Boat Construction**:
    - Phase 1: Wreckage.
    - Phase 2: Adding parts (2 coins per plank).
    - Phase 3: Completed -> Push to Water.
    - Phase 4: Board & Leave (Victory A).
- [ ] **Bomb Shop**:
    - Unlocks at high-tier Campfire.
    - Buy Bomb -> Builders push to Cliff Portal.

## 7. Enemies (The Greed)
- [ ] **Greedling**: Basic unit. Steals coins/tools.
- [ ] **Masked Greed**: Armored, takes more hits.
- [ ] **Floater**: Flying, steals units (top of tower).
- [ ] **Spawning**:
    - Small Portal (Lighthouse side).
    - Big Portal (Cliff side).
    - Waves increase nightly.

## 8. The Cave (Cliff Portal)
- [ ] **Entry**: Escort Bomb to portal -> Pay to enter.
- [ ] **Interior**: Separate scene.
- [ ] **Gameplay**: Defend Bomb until it reaches the Heart.
- [ ] **Detonation**: Pay to ignite -> Run to exit -> Explosion -> Victory B.

## 9. UI & Feedback
- [ ] **Coin Count**: Visual or numeric.
- [ ] **Day Counter**: Roman numerals?
- [ ] **Win Screen**: Statistics (Days survived, Greed killed).
