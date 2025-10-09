import pygame
import sys
import random
from settings import *
from entities import *

# --- Systémoví Správci ---

class SubjectManager:
    def __init__(self, all_sprites, beggar_camp):
        self.all_sprites = all_sprites
        self.beggar_camp = beggar_camp
        self.all_npcs = pygame.sprite.Group()

    def spawn_beggar(self, initial=False):
        if initial or not any(n.state == 'BEGGAR' for n in self.all_npcs):
            beggar = NPC(self.beggar_camp.centerx, self.beggar_camp.bottom)
            self.all_npcs.add(beggar)
            self.all_sprites.add(beggar)

    def recruit_beggars(self, coins_on_ground):
        for beggar in [n for n in self.all_npcs if n.state == 'BEGGAR']:
            collided_coin = pygame.sprite.spritecollideany(beggar, coins_on_ground)
            if collided_coin:
                collided_coin.kill()
                beggar.recruit()

    def collect_coins(self, coins_on_ground):
        for npc in [n for n in self.all_npcs if n.state != 'BEGGAR']:
            collected = pygame.sprite.spritecollide(npc, coins_on_ground, True)
            npc.held_coins += len(collected)

    def drop_coins_for_monarch(self, monarch, all_sprites, coins_on_ground):
        for npc in [n for n in self.all_npcs if n.held_coins > 0 and abs(n.rect.centerx - monarch.rect.centerx) < 70]:
            for _ in range(npc.held_coins):
                new_coin = Coin(npc.rect.centerx + random.randint(-20, 20), npc.rect.bottom - 10)
                all_sprites.add(new_coin)
                coins_on_ground.add(new_coin)
            npc.held_coins = 0

    def handle_attack(self, npc):
        if npc.state in ['BUILDER', 'ARCHER', 'FARMER']:
            npc.state, npc.profession, npc.image.fill(WHITE) = 'VILLAGER_IDLE', None,
        elif npc.state in ['VILLAGER_IDLE', 'VILLAGER_FOLLOWING']:
            npc.state, npc.held_coins, npc.image.fill(GRAY) = 'BEGGAR', 0,

    def update_all(self, monarch, town_center, tool_stations):
        self.all_npcs.update(monarch, town_center, tool_stations)

class EnemyManager:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.enemies = pygame.sprite.Group()

    def spawn_greeds(self, portals):
        for portal in portals:
            for _ in range(random.randint(1, 3)):
                greed = Greed(portal.rect.centerx, portal.rect.bottom, portal)
                self.enemies.add(greed)
                self.all_sprites.add(greed)

    def update(self, game_objects):
        self.enemies.update(game_objects)
        for greed in self.enemies:
            if greed.state == 'ROAMING' and greed.target and greed.rect.colliderect(greed.target.rect):
                target = greed.target
                if isinstance(target, (Coin, Crown)):
                    greed.steal(target)
                elif isinstance(target, NPC):
                    game_objects['subjects'].handle_attack(target)
                    greed.attack()
                elif isinstance(target, Monarch):
                    self.attack_monarch(greed, game_objects)

            if greed.home_portal and greed.rect.colliderect(greed.home_portal.rect):
                greed.kill()

    def attack_monarch(self, greed, game_objects):
        monarch = game_objects['monarch']
        greed.attack()
        if monarch.coin_system.player_coins > 0:
            new_coin = monarch.lose_coin_from_attack()
            if new_coin:
                game_objects['all_sprites'].add(new_coin)
                game_objects['coins'].add(new_coin)
        elif monarch.has_crown:
            new_crown = monarch.drop_crown()
            if new_crown:
                game_objects['all_sprites'].add(new_crown)
                game_objects['crown'].add(new_crown)

class CameraController:
    def __init__(self, target):
        self.target = target
        self.offset_x = 0
    def update(self):
        self.offset_x = self.target.rect.centerx - WIDTH / 2

class TimeManager:
    def __init__(self, enemy_manager, portals):
        self.enemy_manager = enemy_manager
        self.portals = portals
        self.cycle_timer = pygame.time.get_ticks()
        self.is_night = False
    def update(self):
        current_time = pygame.time.get_ticks()
        if self.is_night and current_time - self.cycle_timer > NIGHT_LENGTH:
            self.is_night, self.cycle_timer = False, current_time
        elif not self.is_night and current_time - self.cycle_timer > DAY_LENGTH:
            self.is_night, self.cycle_timer = True, current_time
            self.trigger_night_events()
    def trigger_night_events(self):
        self.enemy_manager.spawn_greeds(self.portals)

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.clock, self.font = pygame.time.Clock(), pygame.font.Font(None, 36)
        self.game_over = False

        self.all_sprites = pygame.sprite.Group()
        self.monarch = Monarch(); self.all_sprites.add(self.monarch)
        self.coins = pygame.sprite.Group()
        self.crown_group = pygame.sprite.Group()

        self.ground_rect = pygame.Rect(0, HEIGHT - 50, WORLD_WIDTH, 50)
        self.town_center = pygame.Rect(WIDTH*1.5 - 50, HEIGHT-50, 100, 10)
        self.beggar_camp = pygame.Rect(300, HEIGHT-100, 80, 50)

        self.subject_manager = SubjectManager(self.all_sprites, self.beggar_camp)
        self.enemy_manager = EnemyManager(self.all_sprites)
        self.portals = [Portal(100, HEIGHT-90), Portal(WORLD_WIDTH-100, HEIGHT-90)]
        self.all_sprites.add(self.portals)

        self.time_manager = TimeManager(self.enemy_manager, self.portals)
        self.camera = CameraController(self.monarch)

        self.tool_stations = [ToolStation(x, HEIGHT-110, t, c, cl) for x,t,c,cl in
                              [(self.town_center.left-80,'hammer',3,ORANGE), (self.town_center.right+20,'bow',2,LIGHT_GREEN), (self.town_center.left-160,'scythe',4,LIGHT_BROWN)]]
        self.chests = pygame.sprite.Group(TreasureChest(WORLD_WIDTH - 200, HEIGHT - 90))
        self.all_sprites.add(self.chests)
        self.bg_layers = [{'r':pygame.Rect(0,y,WIDTH,150),'c':c,'s':s} for y,c,s in [(HEIGHT-250,(100,150,200),0.2),(HEIGHT-200,(50,100,150),0.4),(HEIGHT-150,(20,50,80),0.6)]]

        self.subject_manager.spawn_beggar(initial=True)
        pygame.time.set_timer(SPAWN_BEGGAR_EVENT, 10000)

    def run(self):
        while not self.game_over:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        print("Game Over!"); pygame.quit(); sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.game_over = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                new_coin = self.monarch.drop_coin()
                if new_coin: self.all_sprites.add(new_coin); self.coins.add(new_coin)
            if event.type == SPAWN_BEGGAR_EVENT: self.subject_manager.spawn_beggar()

    def update(self):
        self.time_manager.update()
        game_objects = {'monarch': self.monarch, 'coins': self.coins, 'crown': self.crown_group, 'npcs': self.subject_manager.all_npcs, 'subjects': self.subject_manager, 'town_center': self.town_center}
        self.monarch.update(pygame.key.get_pressed())
        self.subject_manager.update_all(self.monarch, self.town_center, self.tool_stations)
        self.enemy_manager.update(game_objects)
        self.camera.update()

        if not self.monarch.has_crown and pygame.sprite.spritecollide(self.monarch, self.crown_group, True): self.monarch.pickup_crown()
        self.monarch.coin_system.add_coins(len(pygame.sprite.spritecollide(self.monarch, self.coins, True)))
        self.subject_manager.collect_coins(self.coins)
        self.subject_manager.recruit_beggars(self.coins)
        self.subject_manager.drop_coins_for_monarch(self.monarch, self.all_sprites, self.coins)

        for station in self.tool_stations:
            for coin in [c for c in self.coins if station.rect.colliderect(c.rect)]: station.add_coin(), coin.kill()
        for chest in self.chests:
            if chest.state == 'closed' and self.monarch.rect.colliderect(chest.rect):
                for _ in range(chest.open()):
                    new_coin = Coin(chest.rect.centerx+random.randint(-40,40), chest.rect.bottom-10)
                    self.all_sprites.add(new_coin), self.coins.add(new_coin)

        self.check_game_over()

    def check_game_over(self):
        if self.monarch.rect.left < 0: self.monarch.rect.left = 0
        if self.monarch.rect.right > WORLD_WIDTH: self.monarch.rect.right = WORLD_WIDTH
        if self.monarch.coin_system.player_coins <= 0 and not self.monarch.has_crown: self.game_over = True
        for greed in self.enemy_manager.enemies:
            if greed.state == 'CARRYING_CROWN' and not self.screen.get_rect().colliderect(greed.rect): self.game_over = True

    def draw(self):
        self.screen.fill(DARK_BLUE if self.time_manager.is_night else SKY_BLUE)
        offset = self.camera.offset_x
        for l in self.bg_layers:
            for i in range(2): self.screen.fill(l['c'], pygame.Rect(((-offset*l['s'])%WIDTH)+(i-1)*WIDTH, l['r'].y, WIDTH, l['r'].height))
        ground_rect_scrolled = self.ground_rect.copy(); ground_rect_scrolled.x = -offset; self.screen.fill(GREEN, ground_rect_scrolled)
        for loc in [self.beggar_camp, self.town_center]:
            loc_rect = loc.copy(); loc_rect.x -= offset; pygame.draw.rect(self.screen, BROWN if loc==self.beggar_camp else GRAY, loc_rect)
        for station in self.tool_stations: station.draw(self.screen, offset)
        for sprite in self.all_sprites: self.screen.blit(sprite.image, sprite.rect.move(-offset, 0))

        self.screen.blit(self.font.render(f"Coins: {self.monarch.coin_system.player_coins}", True, WHITE), (10, 10))
        pygame.display.flip()