import pygame
import random
from enum import Enum

# --------------- Settings ---------------
WIDTH, HEIGHT = 896, 640        # 28x20 tiles @ 32px
TILE = 32
FPS = 60
TITLE = "Tiny Visual RPG (no assets)"
FONT_NAME = "arial"

# Colors
BLACK=(0,0,0); WHITE=(255,255,255); GREY=(60,60,70)
DARK=(24,24,32); UI_BG=(15,15,20); UI_ACC=(230,230,230)
GRASS=(46,153,61); WALL=(84,84,104); FLOOR=(160,160,180); NPC_COL=(255,210,80)
PLAYER_COL=(80,180,255); ENEMY_COL=(255,80,120)

# --------------- Map Legend ---------------
# 0 = floor, 1 = wall, 2 = tall grass (encounters), 3 = NPC
MAP_DATA = [
    "1111111111111111111111111111",
    "1000000000000000000222200001",
    "1022222000000000000222200031",
    "1020002000000222200222200001",
    "1020002222220222200000000001",
    "1020002000000000000000000001",
    "1022202000000000000000000001",
    "1000002000000000000000000001",
    "1000002222220000000000000001",
    "1000000000020000000000000001",
    "1000000000020000000000000001",
    "1000000000020000000000000001",
    "1000000000020000000000000001",
    "1000000000020000022222222201",
    "1000000000000000000000000001",
    "1000000000000000000000000001",
    "1000000000000000000000000001",
    "1000000000000000000000000001",
    "1000000000000000000000000001",
    "1111111111111111111111111111",
]
MAP_W, MAP_H = len(MAP_DATA[0]), len(MAP_DATA)

# --------------- Helpers ---------------
def world_to_screen(wx, wy, cam):
    return wx - cam[0], wy - cam[1]

def clamp(v, lo, hi):
    return max(lo, min(hi, v))

class Mode(Enum):
    EXPLORE = 1
    DIALOG = 2
    BATTLE = 3

# --------------- Entities ---------------
class Player:
    def __init__(self, x, y):
        self.w = TILE-6
        self.h = TILE-6
        self.rect = pygame.Rect(x, y, self.w, self.h)
        self.speed = 3
        self.hp_max = 30
        self.hp = self.hp_max
        self.potions = 3

    def move(self, dx, dy, game):
        # attempt axis-aligned movement for simple collision
        if dx:
            self.rect.x += dx * self.speed
            self._collide(game, axis='x')
        if dy:
            self.rect.y += dy * self.speed
            self._collide(game, axis='y')

    def _collide(self, game, axis):
        tiles = nearby_solid_tiles(game, self.rect)
        for t in tiles:
            if self.rect.colliderect(t):
                if axis == 'x':
                    if self.rect.centerx > t.centerx:
                        self.rect.left = t.right
                    else:
                        self.rect.right = t.left
                else:
                    if self.rect.centery > t.centery:
                        self.rect.top = t.bottom
                    else:
                        self.rect.bottom = t.top

    def draw(self, surf, cam):
        pygame.draw.rect(surf, PLAYER_COL, (*world_to_screen(self.rect.x, self.rect.y, cam), self.w, self.h))

class NPC:
    def __init__(self, tx, ty, lines):
        self.tx, self.ty = tx, ty
        self.rect = pygame.Rect(tx*TILE, ty*TILE, TILE, TILE)
        self.lines = lines

    def draw(self, surf, cam):
        x, y = world_to_screen(self.rect.x, self.rect.y, cam)
        pygame.draw.rect(surf, NPC_COL, (x+4, y+4, TILE-8, TILE-8))
        # tiny eyes
        pygame.draw.rect(surf, BLACK, (x+9, y+12, 4, 4))
        pygame.draw.rect(surf, BLACK, (x+TILE-13, y+12, 4, 4))

# --------------- Map & Collision ---------------
def is_wall(tx, ty):
    if tx < 0 or ty < 0 or tx >= MAP_W or ty >= MAP_H: return True
    return MAP_DATA[ty][tx] == '1'

def is_grass(tx, ty):
    return 0 <= tx < MAP_W and 0 <= ty < MAP_H and MAP_DATA[ty][tx] == '2'

def is_npc(tx, ty):
    return 0 <= tx < MAP_W and 0 <= ty < MAP_H and MAP_DATA[ty][tx] == '3'

def nearby_solid_tiles(game, rect):
    tiles = []
    min_tx = max(0, rect.left // TILE - 1)
    max_tx = min(MAP_W-1, rect.right // TILE + 1)
    min_ty = max(0, rect.top // TILE - 1)
    max_ty = min(MAP_H-1, rect.bottom // TILE + 1)
    for ty in range(min_ty, max_ty+1):
        for tx in range(min_tx, max_tx+1):
            if is_wall(tx, ty):
                tiles.append(pygame.Rect(tx*TILE, ty*TILE, TILE, TILE))
    return tiles

# --------------- Battle System ---------------
class Enemy:
    def __init__(self, name="Slime", hp=20, atk=(3,6)):
        self.name = name
        self.hp_max = hp
        self.hp = hp
        self.atk_min, self.atk_max = atk

    def attack(self):
        return random.randint(self.atk_min, self.atk_max)

class Battle:
    def __init__(self, player):
        self.player = player
        self.enemy = Enemy()
        self.menu = ["Attack", "Defend", f"Potion ({player.potions})", "Run"]
        self.sel = 0
        self.log = ["A wild Slime appears!"]
        self.player_defending = False
        self.over = False
        self.result = None  # "win", "lose", "run"

    def update_menu(self):
        self.menu = ["Attack", "Defend", f"Potion ({self.player.potions})", "Run"]

    def handle_input(self, event):
        if self.over: return
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.sel = (self.sel - 1) % len(self.menu)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.sel = (self.sel + 1) % len(self.menu)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.take_turn(self.sel)

    def add_log(self, text):
        self.log.append(text)
        if len(self.log) > 6:
            self.log.pop(0)

    def take_turn(self, choice):
        if self.over: return
        self.player_defending = False
        if choice == 0:  # Attack
            dmg = random.randint(6, 9)
            self.enemy.hp = max(0, self.enemy.hp - dmg)
            self.add_log(f"You hit {self.enemy.name} for {dmg}.")
        elif choice == 1:  # Defend
            self.player_defending = True
            self.add_log("You brace for impact.")
        elif choice == 2:  # Potion
            if self.player.potions > 0 and self.player.hp < self.player.hp_max:
                heal = random.randint(8, 14)
                self.player.hp = min(self.player.hp_max, self.player.hp + heal)
                self.player.potions -= 1
                self.add_log(f"You drink a potion and heal {heal}.")
            else:
                self.add_log("No effect.")
        elif choice == 3:  # Run
            if random.random() < 0.55:
                self.add_log("You got away safely!")
                self.over = True
                self.result = "run"
                return
            else:
                self.add_log("Couldn't escape!")

        # enemy acts if still alive
        if self.enemy.hp > 0 and not self.over:
            raw = self.enemy.attack()
            dmg = raw // 2 if self.player_defending else raw
            self.player.hp = max(0, self.player.hp - dmg)
            if self.player_defending:
                self.add_log(f"{self.enemy.name} attacks for {raw}, you block to {dmg}.")
            else:
                self.add_log(f"{self.enemy.name} hits you for {dmg}.")

        # check end
        if self.enemy.hp <= 0:
            self.add_log(f"{self.enemy.name} is defeated!")
            self.over = True
            self.result = "win"
        elif self.player.hp <= 0:
            self.add_log("You collapse...")
            self.over = True
            self.result = "lose"

        self.update_menu()

    def draw_bar(self, surf, x, y, w, h, frac):
        pygame.draw.rect(surf, GREY, (x, y, w, h))
        pygame.draw.rect(surf, UI_ACC, (x+2, y+2, int((w-4)*frac), h-4))

    def draw(self, surf, font_big, font_small):
        # background
        surf.fill(DARK)
        # enemy blob
        pygame.draw.circle(surf, ENEMY_COL, (WIDTH//2, HEIGHT//3), 60)
        # frame
        ui = pygame.Rect(16, HEIGHT-220, WIDTH-32, 204)
        pygame.draw.rect(surf, UI_BG, ui, border_radius=8)
        pygame.draw.rect(surf, UI_ACC, ui, width=2, border_radius=8)

        # HP bars
        self.draw_bar(surf, 32, 24, 280, 24, self.player.hp / self.player.hp_max)
        surf.blit(font_small.render(f"HP {self.player.hp}/{self.player.hp_max}", True, WHITE), (36, 26))
        self.draw_bar(surf, WIDTH-312, 24, 280, 24, self.enemy.hp / self.enemy.hp_max)
        surf.blit(font_small.render(f"{self.enemy.name} {self.enemy.hp}/{self.enemy.hp_max}", True, WHITE), (WIDTH-308, 26))

        # Menu
        for i, item in enumerate(self.menu):
            y = ui.y + 16 + i*36
            col = UI_ACC if i == self.sel else WHITE
            surf.blit(font_big.render(item, True, col), (ui.x+20, y))

        # Log
        for i, line in enumerate(self.log[-6:]):
            surf.blit(font_small.render(line, True, WHITE), (ui.x+360, ui.y+18 + i*28))

# --------------- Dialog UI ---------------
def draw_dialog(surf, text_lines, font, hint_font):
    panel = pygame.Rect(16, HEIGHT-180, WIDTH-32, 164)
    pygame.draw.rect(surf, UI_BG, panel, border_radius=8)
    pygame.draw.rect(surf, UI_ACC, panel, width=2, border_radius=8)
    for i, line in enumerate(text_lines[:4]):
        surf.blit(font.render(line, True, WHITE), (panel.x+20, panel.y+20 + i*32))
    surf.blit(hint_font.render("Press Esc to close", True, UI_ACC), (panel.right-220, panel.bottom-28))

# --------------- Rendering Map ---------------
def draw_map(surf, cam):
    start_tx = clamp(cam[0]//TILE, 0, MAP_W-1)
    end_tx = clamp((cam[0]+WIDTH)//TILE + 1, 0, MAP_W-1)
    start_ty = clamp(cam[1]//TILE, 0, MAP_H-1)
    end_ty = clamp((cam[1]+HEIGHT)//TILE + 1, 0, MAP_H-1)

    for ty in range(start_ty, end_ty+1):
        for tx in range(start_tx, end_tx+1):
            ch = MAP_DATA[ty][tx]
            wx, wy = tx*TILE, ty*TILE
            sx, sy = world_to_screen(wx, wy, cam)
            if ch == '1':
                color = WALL
            elif ch == '2':
                color = GRASS
            else:
                color = FLOOR
            pygame.draw.rect(surf, color, (sx, sy, TILE, TILE))
            # subtle grid
            pygame.draw.rect(surf, DARK, (sx, sy, TILE, TILE), width=1)

# --------------- Game Loop ---------------
def main():
    pygame.init()
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(FONT_NAME, 24)
    font_big = pygame.font.SysFont(FONT_NAME, 28, bold=True)
    font_small = pygame.font.SysFont(FONT_NAME, 20)

    # Find a starting open tile
    spawn_found = False
    for ty in range(MAP_H):
        for tx in range(MAP_W):
            if MAP_DATA[ty][tx] in ('0','2'):
                start_tx, start_ty = tx, ty
                spawn_found = True
                break
        if spawn_found: break

    player = Player(start_tx*TILE+3, start_ty*TILE+3)
    npcs = []
    # locate NPC tiles and create an NPC entity at the first one
    for ty in range(MAP_H):
        for tx in range(MAP_W):
            if is_npc(tx, ty):
                npcs.append(NPC(tx, ty, [
                    "Welcome to the demo!",
                    "Walk on tall grass for battles.",
                    "Press E near me to chat.",
                    "Good luck, adventurer."
                ]))

    mode = Mode.EXPLORE
    dialog_lines = []
    battle = None

    # Camera
    cam = [0, 0]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if mode == Mode.DIALOG:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    mode = Mode.EXPLORE

            elif mode == Mode.BATTLE:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # allow leaving only if battle concluded
                    if battle and battle.over:
                        mode = Mode.EXPLORE
                if battle:
                    battle.handle_input(event)

        keys = pygame.key.get_pressed()
        if mode == Mode.EXPLORE:
            dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
            dy = (keys[pygame.K_DOWN]  or keys[pygame.K_s]) - (keys[pygame.K_UP]   or keys[pygame.K_w])
            player.move(dx, dy, game=None)

            # Interact: talk to NPC if adjacent and E pressed
            if keys[pygame.K_e]:
                for npc in npcs:
                    if player.rect.colliderect(npc.rect.inflate(TILE, TILE)):
                        dialog_lines = npc.lines
                        mode = Mode.DIALOG
                        break

            # Random encounters in grass when stepping between tiles
            tx, ty = player.rect.centerx // TILE, player.rect.centery // TILE
            if is_grass(tx, ty):
                # low chance each frame while in grass and moving
                if (dx or dy) and random.random() < 0.012:
                    battle = Battle(player)
                    mode = Mode.BATTLE

        # Camera follows player
        cam[0] = clamp(player.rect.centerx - WIDTH//2, 0, MAP_W*TILE - WIDTH)
        cam[1] = clamp(player.rect.centery - HEIGHT//2, 0, MAP_H*TILE - HEIGHT)

        # Draw
        if mode != Mode.BATTLE:
            screen.fill(BLACK)
            draw_map(screen, cam)
            for npc in npcs:
                npc.draw(screen, cam)
            player.draw(screen, cam)

            # HUD
            pygame.draw.rect(screen, UI_BG, (16, 12, 300, 52), border_radius=8)
            pygame.draw.rect(screen, UI_ACC, (16, 12, 300, 52), width=2, border_radius=8)
            hp_text = font_small.render(f"HP {player.hp}/{player.hp_max}", True, WHITE)
            pot_text = font_small.render(f"Potions: {player.potions}", True, WHITE)
            screen.blit(hp_text, (28, 22))
            screen.blit(pot_text, (28, 44))

            if mode == Mode.DIALOG:
                draw_dialog(screen, dialog_lines, font, font_small)
        else:
            # Battle scene
            battle.draw(screen, font_big, font_small)
            if battle.over:
                # hint
                hint = font_small.render("Press Esc to return", True, UI_ACC)
                screen.blit(hint, (WIDTH//2 - hint.get_width()//2, HEIGHT-36))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
