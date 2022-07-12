"""

I get help from youtuber who is sh*t at math (Code Monkey King)
to learn math
The more someone hates math 
the more they have to explain it
Great Sucsess (probably misspelled)

"""

class LEVEL():
    def __init__(self, _map):
        self.map = _map

    def get_map(self):
        return self.map

MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
]

import pygame
import math

SCREEN_W = 480*2
SCREEN_H = 480
HALF_SCREEN_W = SCREEN_W//2

FOV = 60
HALF_FOV = FOV/2

# Jo, mer jo saktere
CASTED_RAYS_TOTAL = 120

TILE_SIZE = HALF_SCREEN_W // len(MAP)

# Maks lengde hver ray kan gå
# Sånn at det ikke må være uendelig
MAX_DEPTH = len(MAP) * TILE_SIZE


ANGLE_CHANGE_PER_STEP = math.radians(FOV) / CASTED_RAYS_TOTAL

SCALE =  HALF_SCREEN_W / CASTED_RAYS_TOTAL




level_one = LEVEL(MAP)

def draw_map(_map, screen, player_x, player_y, player_angle):

    # Venstre

    map_h = len(MAP)
    map_w = len(MAP[0])

    size_h = 480 // map_h
    size_w = 480 // map_w

    for y in range(map_h):
        for x in range(map_w):
            if _map[y][x] == 0:
                pygame.draw.rect(screen, ((100,100,100)), (x*size_w,y*size_h,size_w,size_h))
            elif _map[y][x] == 1:
                pygame.draw.rect(screen, ((200,200,200)), (x*size_w,y*size_h,size_w,size_h))
    
    for y in range(1, map_h):
        pygame.draw.line(screen, ((0,0,0)), (0, y*size_h), (480, y*size_h), 2)

    for x in range(1, map_w):
        pygame.draw.line(screen, ((0,0,0)), (x*size_w,0), (x*size_w,480), 2)

    pygame.draw.circle(screen, ((255,0,0)), (player_x,player_y),  8.0)


    # Retning Karakter
    pygame.draw.line(screen, ((0,255,0)), (player_x,player_y), (player_x - math.sin(player_angle)*50,player_y + math.cos(player_angle)*50), 3)

    # FOV karakter
    pygame.draw.line(screen, ((0,255,0)), (player_x,player_y), (player_x - math.sin(player_angle-math.radians(HALF_FOV))*50,player_y + math.cos(player_angle-math.radians(HALF_FOV))*50), 3)
    pygame.draw.line(screen, ((0,255,0)), (player_x,player_y), (player_x - math.sin(player_angle+math.radians(HALF_FOV))*50,player_y + math.cos(player_angle+math.radians(HALF_FOV))*50), 3)
    #pygame.draw.line(screen, ((0,255,0)), (player_x + math.sin(player_angle-math.radians(HALF_FOV))*50,player_y + math.cos(player_angle-math.radians(HALF_FOV))*50), (player_x + math.sin(player_angle+math.radians(HALF_FOV))*50,player_y + math.cos(player_angle+math.radians(HALF_FOV))*50), 3)

def distance(p1, p2):
    x1 = p1[0]
    x2 = p2[0]
    y1 = p1[1]
    y2 = p2[1]

    return math.sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

# Raycasting
def cast_rays(player_angle, player_x, player_y, level_map, screen):

    # Vinkel lengst til venstre
    start_vinkel = player_angle - math.radians(HALF_FOV)

    # Vinkel lengst til høyre
    slutt_vinkel = player_angle + math.radians(HALF_FOV)

    for d in range(MAX_DEPTH):
        pygame.draw.line(screen, ((0,0,0)), (480+d,0),(480+d,SCREEN_H))


    # Gå gjennom hver ray
    for ray in range(CASTED_RAYS_TOTAL):

        # Gå til ny vinkel 
        start_vinkel += ANGLE_CHANGE_PER_STEP

        for depth in range(MAX_DEPTH):
            

            pos_x = player_x - math.sin(start_vinkel)*depth
            pos_y = player_y + math.cos(start_vinkel)*depth

            map_x = int(pos_x // TILE_SIZE)
            map_y = int(pos_y // TILE_SIZE)

            if level_map[map_y][map_x] == 1:
                pygame.draw.rect(screen, ((0,255,0)), (map_x*TILE_SIZE + 5,map_y*TILE_SIZE+5,TILE_SIZE-5,TILE_SIZE-5) )
                pygame.draw.line(screen, ((0,255,255)), (player_x,player_y), (pos_x,pos_y), 1)

                lineHeight = SCREEN_H / distance((player_x,player_y), (pos_x,pos_y)) * 10
                pygame.draw.line(screen, ((255,255,255)), (480+ray*4,SCREEN_H//2-lineHeight//2),(480+ray*4,SCREEN_H//2+lineHeight//2))
                pygame.draw.line(screen, ((255,255,255)), (480+ray*4+1,SCREEN_H//2-lineHeight//2),(480+ray*4+1,SCREEN_H//2+lineHeight//2))
                pygame.draw.line(screen, ((255,255,255)), (480+ray*4+2,SCREEN_H//2-lineHeight//2),(480+ray*4+2,SCREEN_H//2+lineHeight//2))
                pygame.draw.line(screen, ((255,255,255)), (480+ray*4+3,SCREEN_H//2-lineHeight//2),(480+ray*4+3,SCREEN_H//2+lineHeight//2))


                break
        
        if start_vinkel > slutt_vinkel:
            return


def main():

    player_x = SCREEN_W//2 - 240
    player_y = SCREEN_H//2
    player_angle = math.pi # Radianer ... 1 PI betyr at karakteren ser rett opp
    player_speed = 2

    # You know the drill
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_W,SCREEN_H))

    pygame.display.set_caption("Ratcasting") # Don't ask questions
    clock = pygame.time.Clock()

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        held_keys = pygame.key.get_pressed()
        if held_keys[pygame.K_d]:
            oldDegrees = math.degrees(player_angle)
            player_angle = math.radians(oldDegrees + 5)
        if held_keys[pygame.K_a]:
            oldDegrees = math.degrees(player_angle)
            player_angle = math.radians(oldDegrees - 5)

        # Movement 
        if held_keys[pygame.K_w]:
            newX = math.sin(player_angle) * player_speed
            newY = math.cos(player_angle) * player_speed
            if level_one.get_map()[int((player_y + newY)//TILE_SIZE)][int((player_x - newX)//TILE_SIZE)] == 0:
                player_x -= newX
                player_y += newY
        if held_keys[pygame.K_s]:
            newX = math.sin(player_angle) * player_speed
            newY = math.cos(player_angle) * player_speed
            if level_one.get_map()[int((player_y - newY)//TILE_SIZE)][int((player_x + newX)//TILE_SIZE)] == 0:
                player_x += newX
                player_y -= newY


        screen.fill((255,255,255))

        draw_map(level_one.map, screen, player_x, player_y, player_angle)

        # bruk raycasting
        cast_rays(player_angle,player_x,player_y,level_one.get_map(),screen)
        
        pygame.display.update()
        clock.tick(40)


if __name__ == "__main__":
    main()
    pygame.quit()