# Kingdom: Classic Clone - Functionality List

## 1. Core Engine
- [ ] **Game Loop**: Standard Pygame loop (Events, Update, Draw).
- [ ] **Settings**: Screen resolution (retro aspect ratio), frame rate (60 FPS), colors (palette).
- [ ] **Camera**: Horizontal scrolling following the player.
- [ ] **Input**: Keyboard support (Arrow keys/WASD for movement, Down/S to drop coin/interact, Shift to run).

## 2. World & Environment
- [ ] **Level Generation**: Flat terrain with boundaries.
- [ ] **Parallax Background**: Multiple layers (Sky, Far trees, Near trees) moving at different speeds.
- [ ] **Ground**: Water reflection effect (simple mirroring/color shift).
- [ ] **Day/Night Cycle**: Visual change (Sky color), Logic change (Peaceful vs Danger).

## 3. Player (Monarch)
- [ ] **Movement**: Horse riding physics (acceleration, friction).
- [ ] **States**: Idle, Walk, Gallop (stamina limited).
- [ ] **Inventory**: Coin pouch (visual representation of fullness).
- [ ] **Actions**: Drop coin (triggers physics).
- [ ] **Crown**: Visual on head. If hit by Greed, crown drops. If Greed takes crown, Game Over.

## 4. Economy
- [ ] **Coin Entity**: Physics-based entity (gravity, bounce).
- [ ] **Sources**: Chests (one-time), Archers hunting (rabbits/deer), Farms.
- [ ] **Sinks**: Recruiting, Building, Upgrading, Paying Greed (to save life).

## 5. Units (NPCs)
- [ ] **Vagrants**: Spawn in camps. Wander. Recruit with 1 coin -> Peasant.
- [ ] **Peasants**: Seek tools to become specialized units.
- [ ] **Archers**:
    - Buy Bow (2 coins).
    - Day: Hunt wildlife for coins.
    - Night: Retreat to walls, shoot at Greed.
- [ ] **Builders**:
    - Buy Hammer (3 coins).
    - Build/Upgrade structures.
    - Operate catapults (optional/advanced).
- [ ] **Knights** (Win Condition Requirement):
    - Upgraded from Castle. Lead attack on Portals.

## 6. Buildings
- [ ] **Town Center (Campfire)**:
    - Tier 0: Campfire (Recruitment center).
    - Upgrades: Tent -> Wooden Fort -> Stone Castle.
    - Spawns Banker/Merchant (optional).
- [ ] **Walls**:
    - Build on mound slots. Block Enemies. Health pool.
- [ ] **Towers**:
    - Build on rock slots. Safe spot for Archers.
- [ ] **Farms**:
    - Build on stream slots. Peasant farmers generate gold.
- [ ] **Tool Shops**:
    - Archery Range (Spawns Bows).
    - Workshop (Spawns Hammers).

## 7. Enemies (The Greed)
- [ ] **Spawning**: Spawn from Portals at night. Wave size increases over days.
- [ ] **Greedling**: Basic enemy. Runs at player/units.
    - Action: Hit unit -> unit drops tool/coin.
    - Action: Pick up coin/tool -> Run back to portal.
    - Action: Attack Walls.
- [ ] **Portals**:
    - Located at far ends of map.
    - Spawn enemies.
    - Vulnerable to attack (Win Condition).

## 8. Game Logic
- [ ] **Win Condition**: Destroy all Portals (or at least one side to "escape" in New Lands, but Classic is usually destroy portals/survive). Let's aim for Destroy Portals.
- [ ] **Lose Condition**: Crown is stolen by Greed and enters a Portal.

## 9. Visuals (Pixel Art Style)
- [ ] **Procedural Assets**: Use `pygame.Surface` and `draw.rect` to create blocky, low-res sprites.
- [ ] **Animations**: Simple frame-based animation or bobbing effects.
