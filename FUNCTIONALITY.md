# Kingdom: Classic Clone - Functionality List

## 1. Core Engine
- [x] **Game Loop**: Standard Pygame loop (Events, Update, Draw).
- [x] **Settings**: Screen resolution (retro aspect ratio), frame rate (60 FPS), colors (palette).
- [x] **Camera**: Horizontal scrolling following the player.
- [x] **Input**: Keyboard support (Arrow keys/WASD for movement, Down/S to drop coin/interact, Shift to run).

## 2. World & Environment
- [x] **Level Generation**: Flat terrain with boundaries.
- [x] **Parallax Background**: Multiple layers (Sky, Far trees, Near trees) moving at different speeds.
- [x] **Ground**: Water reflection effect (simple mirroring/color shift).
- [x] **Day/Night Cycle**: Visual change (Sky color), Logic change (Peaceful vs Danger).

## 3. Player (Monarch)
- [x] **Movement**: Horse riding physics (acceleration, friction).
- [x] **States**: Idle, Walk, Gallop (stamina limited).
- [x] **Inventory**: Coin pouch (visual representation of fullness).
- [x] **Actions**: Drop coin (triggers physics).
- [x] **Crown**: Visual on head. If hit by Greed, crown drops. If Greed takes crown, Game Over.

## 4. Economy
- [x] **Coin Entity**: Physics-based entity (gravity, bounce).
- [x] **Sources**: Chests (one-time), Archers hunting (rabbits/deer), Farms.
- [x] **Sinks**: Recruiting, Building, Upgrading, Paying Greed (to save life).

## 5. Units (NPCs)
- [x] **Vagrants**: Spawn in camps. Wander. Recruit with 1 coin -> Peasant.
- [x] **Peasants**: Seek tools to become specialized units.
- [x] **Archers**:
    - Buy Bow (2 coins).
    - Day: Hunt wildlife for coins.
    - Night: Retreat to walls, shoot at Greed.
- [x] **Builders**:
    - Buy Hammer (3 coins).
    - Build/Upgrade structures.
    - Operate catapults (optional/advanced).
- [ ] **Knights** (Win Condition Requirement):
    - Upgraded from Castle. Lead attack on Portals. (Simplified: Archers attack portals).

## 6. Buildings
- [x] **Town Center (Campfire)**:
    - Tier 0: Campfire (Recruitment center).
    - Upgrades: Tent -> Wooden Fort -> Stone Castle.
    - Spawns Banker/Merchant (optional).
- [x] **Walls**:
    - Build on mound slots. Block Enemies. Health pool.
- [x] **Towers**:
    - Build on rock slots. Safe spot for Archers.
- [x] **Farms**:
    - Build on stream slots. Peasant farmers generate gold.
- [x] **Tool Shops**:
    - Archery Range (Spawns Bows).
    - Workshop (Spawns Hammers).

## 7. Enemies (The Greed)
- [x] **Spawning**: Spawn from Portals at night. Wave size increases over days.
- [x] **Greedling**: Basic enemy. Runs at player/units.
    - Action: Hit unit -> unit drops tool/coin.
    - Action: Pick up coin/tool -> Run back to portal.
    - Action: Attack Walls.
- [x] **Portals**:
    - Located at far ends of map.
    - Spawn enemies.
    - Vulnerable to attack (Win Condition).

## 8. Game Logic
- [x] **Win Condition**: Destroy all Portals (or at least one side to "escape" in New Lands, but Classic is usually destroy portals/survive). Let's aim for Destroy Portals.
- [x] **Lose Condition**: Crown is stolen by Greed and enters a Portal.

## 9. Visuals (Pixel Art Style)
- [x] **Procedural Assets**: Use `pygame.Surface` and `draw.rect` to create blocky, low-res sprites.
- [x] **Animations**: Simple frame-based animation or bobbing effects.
