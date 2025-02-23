import pygame
import Perlin

worldWidth = 100
worldHeight = 100
drawnCellSize = 5

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
            
            color = (0, 50, 100)
            intensity = world[x][y]

            for i in range(len(thresholds)):
                if intensity > thresholds[i]:
                    color = colors[i]
                else:
                    break

            #using float intensity
            pygame.draw.rect(screen, color, (x * drawnCellSize, y * drawnCellSize, drawnCellSize, drawnCellSize))

#stacking 2 perlin noises
params = [
    (10, 10, "fade"),
    (5, 100, "fade")
]
world = Perlin.fractalStackedPerlin(worldWidth, worldHeight, params, 100)

thresholds = [40, 55, 60, 65, 70, 80, 85, 90, 93, 96]
colors = [(0, 75, 155), (0, 170, 220), (250, 210, 130), (230, 180, 60), (20, 150, 0), (40, 100, 0), (80, 80, 80), (60, 60, 60), (220, 220, 220), (255, 255, 255)]

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill screen
    screen.fill((0, 0, 0))

    #draw world
    drawWorld(world)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
