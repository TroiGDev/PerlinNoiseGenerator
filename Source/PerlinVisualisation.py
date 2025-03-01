import pygame
import Perlin

worldWidth = 500
worldHeight = 500
drawnCellSize = 1

pygame.init()
screenWidth = worldWidth * drawnCellSize
screenHeight = worldHeight * drawnCellSize
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('PerlinVisualisation')

#remove window icon
transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))
pygame.display.set_icon(transparent_surface)

def drawWorld(world):
    #draw squares where there is a 1 in the world array
    for x in range(worldWidth):
        for y in range(worldHeight):
            
            #using 2 layer threshold
            """if world[x][y] > threshold:
                pygame.draw.rect(screen, (255, 255, 255), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))"""

            #using 3 layer threshold
            """if world[x][y] > 0.50:
                pygame.draw.rect(screen, (255, 255, 255), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))
            elif world[x][y] > 0.25 and world[x][y] < 0.50:
                pygame.draw.rect(screen, (177, 177, 177), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))"""

            #using float intensity
            pygame.draw.rect(screen, (world[x][y] * 255, world[x][y] * 255, world[x][y] * 255), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))

#generate perlin grid
world = Perlin.perlin(worldWidth, worldHeight, 10, 1, "fade")

#generate fractal perlin grid
"""params = [
    (40, 0.2, "fade"),
    (20, 0.5, "fade"),
    (10, 1, "fade")
]
world = Perlin.fractalStackedPerlin(worldWidth, worldHeight, params, 1)"""

#stacking 2 perlin noises
"""world1 = Perlin.perlin(worldWidth, worldHeight, 20, 0.5, "fade")
world2 = Perlin.perlin(worldWidth, worldHeight, 10, 1, "fade")
noises = [world1, world2]
world = Perlin.stackPerlinNoises(noises, 1)"""

threshold = 0

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill screen
    screen.fill((0, 0, 0))

    #increase threshold
    threshold += 0.001

    #clamp to 0 and 1
    if threshold > 1:
        threshold = 0

    #draw world
    drawWorld(world)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
