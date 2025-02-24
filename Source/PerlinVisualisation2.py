import pygame
import math
import Perlin

from pyRecorder import Recorder
recorder = Recorder("gameoflife")

worldWidth = 100
worldHeight = 100
drawnCellSize = 5

pygame.init()
screenWidth = worldWidth * drawnCellSize
screenHeight = worldHeight * drawnCellSize
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('PerlinVisualisation')

#cloud transparent surface
cloudSurface = pygame.Surface((worldWidth, worldHeight), pygame.SRCALPHA)


def drawWorld(world):
    cloudSurface.fill((0, 0, 0, 0))

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

            #draw clouds perlin
            cx = math.trunc((x + cloudOffsetx)) % worldWidth
            cy = math.trunc((y + cloudOffsety)) % worldHeight
            if cloudNoise[x][y] > cloudThreshold:
                pygame.draw.rect(cloudSurface, (255, 255, 255, 60), pygame.Rect(cx, cy, drawnCellSize, drawnCellSize))

    scaledClouds = pygame.transform.scale(cloudSurface, (worldWidth * drawnCellSize, worldHeight * drawnCellSize))  # Scale to match screen size

    screen.blit(scaledClouds, (0, 0))

#stacking 2 perlin noises
params = [
    (10, 10, "fade"),
    (5, 100, "fade")
]
world = Perlin.fractalStackedPerlin(worldWidth, worldHeight, params, 100)

wave = 55
waveMag = 1.5
waveFreq = 0.01
waveIter = 0

cloudSpeedx = 0.008
cloudSpeedy = 0.002
cloudOffsetx = 0
cloudOffsety = 0
cloudThreshold = 0.8
cloudMag = 0.0001
cloudFreq = 0.01
cloudIter = 0

cloudNoise = Perlin.perlin(worldWidth, worldHeight, 5, 1, "fade")

thresholds = [40, wave, 60, 65, 70, 80, 90, 95]
colors = [(0, 75, 155), (0, 170, 220), (250, 210, 130), (230, 180, 60), (0, 150, 80), (0, 100, 50), (100, 100, 100), (150, 150, 150)]

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill screen
    screen.fill((0, 0, 0))

    #update wave sin threshold
    waveIter += 1
    thresholds[1] = wave + math.sin(waveIter * waveFreq) * waveMag

    #udpate cloud pos
    cloudOffsetx += cloudSpeedx
    cloudOffsety += cloudSpeedy
    cloudIter += 1
    cloudThreshold = cloudThreshold + math.sin(cloudIter * cloudFreq) * cloudMag

    #draw world
    drawWorld(world)

    # Update the display
    pygame.display.flip()

    #after rendered frame, take recorder shot
    recorder.takeShot(screen)

#get video from taken shots
recorder.getVideo("GOL_Plants.avi", 24)

# Quit Pygame
pygame.quit()
