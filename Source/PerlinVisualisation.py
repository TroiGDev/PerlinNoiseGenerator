import pygame
import Perlin

wolrdWidth = 100
worldHeight = 100
drawnCellSize = 5

pygame.init()
screenWidth = wolrdWidth * drawnCellSize
screenHeight = worldHeight * drawnCellSize
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('PerlinVisualisation')

#remove window icon
transparent_surface = pygame.Surface((32, 32), pygame.SRCALPHA)
transparent_surface.fill((0, 0, 0, 0))
pygame.display.set_icon(transparent_surface)

def drawWorld(world):
    #draw squares where there is a 1 in the world array
    for x in range(wolrdWidth):
        for y in range(worldHeight):
            
            #using 2 layer threshold
            if world[x][y] > threshold:
                pygame.draw.rect(screen, (255, 255, 255), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))

            """#using 3 layer threshold
            if world[x][y] > 0.66:
                pygame.draw.rect(screen, (255, 255, 255), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))
            elif world[x][y] > 0.33 and world[x][y] < 0.66:
                pygame.draw.rect(screen, (177, 177, 177), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))
            else:
                pygame.draw.rect(screen, (0, 0, 0), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))"""

            #using float intensity
            """pygame.draw.rect(screen, (world[x][y] * 255, world[x][y] * 255, world[x][y] * 255), (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))"""

#generate perlin grid
world = Perlin.perlin(wolrdWidth, worldHeight, 10, 10)
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
