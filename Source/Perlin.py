import random
import math

#get randomized unit vector
def GetRandomVectorRotation():
    #get random rotation in degrees
    angleDeg = random.uniform(0, 360)
    angleRad = math.radians(angleDeg)
    # Calculate unit vector components
    x = math.cos(angleRad) * random.uniform(0, 1)
    y = math.sin(angleRad) * random.uniform(0, 1)
    return (x, y)

#get normalized vector
def normalizeVector(v):
    magnitude = math.sqrt(v[0] ** 2 + v[1] ** 2)
    if magnitude > 0:
        return (v[0] / magnitude, v[1] / magnitude)
    else:
        return (0, 0)

#get dot product
def dotProduct(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

#----------------------------------------------------------------------INTERPOLATION METHODS

#linear interpolation
def Interpolate(p1, p2, t):
    return (1-t)*p1 + (t)*p2

#bilinear interpolation
def BiInterpolate(a1, a2, b1, b2, tx, ty):
    subInterpolation1 = Interpolate(a1, a2, tx)
    subInterpolation2 = Interpolate(b1, b2, tx)
    return Interpolate(subInterpolation1, subInterpolation2, ty)

#fade function ...I HAVE NO IDEA WHAT THIS IS : https://adrianb.io/2014/08/09/perlinnoise.html
def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def fadeInterpolate(d1, d2, d3, d4, tx, ty):
    ft = fade(tx)
    fb = fade(ty)
    p0p1 = Interpolate(d1, d2, ft)
    p2p3 = Interpolate(d3, d4, ft)
    return Interpolate(p0p1, p2p3, fb)

def smoothstep(t):
    return t * t * (3 - 2 * t)

def smoothStepBiInterpolate(q11, q12, q21, q22, x, y):
    # Horizontal interpolation
    r1 = q11 * (1 - smoothstep(x)) + q21 * smoothstep(x)
    r2 = q12 * (1 - smoothstep(x)) + q22 * smoothstep(x)
    
    # Vertical interpolation
    return r1 * (1 - smoothstep(y)) + r2 * smoothstep(y)

#----------------------------------------------------------------------

#generate perlin noise
def perlin(cWidth, cHeight, frequency, amplitude, interpolationMethod):
    #get some usefull variables
    cellSizeX = int(round(cWidth / frequency))
    cellSizeY = int(round(cHeight / frequency))

    #create 2d child grid
    cGrid = [[0 for _ in range(cWidth)] for _ in range(cHeight)]

    #create 2d parent grid
    pGrid = [[GetRandomVectorRotation() for _ in range(frequency + 1)] for _ in range(frequency + 1)]

    #for every pixel in child
    for x in range(cWidth):
        for y in range(cHeight):

            #get gradient vectors
            px = math.trunc(x / (cWidth/frequency))
            py = math.trunc(y / (cHeight/frequency))

            g1 = pGrid[px][py]              #top left
            g2 = pGrid[px + 1][py]          #top right
            g3 = pGrid[px][py + 1]          #bottom left
            g4 = pGrid[px + 1][py + 1]      #bottom right

            #get offset vectors
            o1 = (px * cellSizeX - x, py * cellSizeY - y)
            o2 = ((px + 1) * cellSizeX - x, py * cellSizeY - y)
            o3 = (px * cellSizeX - x, (py + 1) * cellSizeY - y)
            o4 = ((px + 1) * cellSizeX - x, (py + 1) * cellSizeY - y)

            #get dot products
            d1 = dotProduct(g1, o1)
            d2 = dotProduct(g2, o2)
            d3 = dotProduct(g3, o3)
            d4 = dotProduct(g4, o4)

            #bilinearly interpolate the dot products
            tx = (x - (px * cellSizeX)) / cellSizeX
            ty = (y - (py * cellSizeY)) / cellSizeY

            #interpolate, using bilinnear, fade or smoothstep bilinear interpolation
            if interpolationMethod == "smoothstep":
                intensity = smoothStepBiInterpolate(d1, d2, d3, d4, tx, ty)
            elif interpolationMethod == "bilinear":
                intensity = BiInterpolate(d1, d2, d3, d4, tx, ty)
            elif interpolationMethod == "fade":
                intensity = fadeInterpolate(d1, d2, d3, d4, tx, ty)
            else:
                print("No such interpolation method exists!")

            #apply final intensity to return array
            cGrid[x][y] = intensity

    #normalize grid between 0 and 1
    min = 0
    max = 0
    for x in range(cWidth):
        for y in range(cHeight):
            if cGrid[x][y] > max:
                max = cGrid[x][y]
            if cGrid[x][y] < min:
                min = cGrid[x][y]
    
    #add min*-1 to all cells to get positive
    for x in range(cWidth):
        for y in range(cHeight):
            cGrid[x][y] += min * -1
    
    #update max value to get range ratio comparison
    max += min * -1

    #go trhough grid again and normalize, then multiply by amplitude
    for x in range(cWidth):
        for y in range(cHeight):
            cGrid[x][y] = (cGrid[x][y] / max) * amplitude

    #return final array
    return cGrid

#generate fractal stacked perlin
def fractalStackedPerlin(cWidth, cHeight, params, amplitude):
    #generate perlin by parameters
    noises = []
    for i in range(len(params)):
        noises.append(perlin(cWidth, cHeight, params[i][0], params[i][1], params[i][2]))    #params[i] = parameter tuple (freq, amp, interp)

    #create 2d child grid
    cGrid = [[0 for _ in range(cWidth)] for _ in range(cHeight)]

    #apply avarage intensity
    for x in range(cWidth):
        for y in range(cHeight):
            for noise in noises:
                cGrid[x][y] += noise[x][y]       #for every pixel, for every noise, add noise to child grid
            
            #divide for correct avarage
            cGrid[x][y] = cGrid[x][y] / len(noises)

    #normalize grid and multiply by final amplitude
    min = 0
    max = 0
    for x in range(cWidth):
        for y in range(cHeight):
            if cGrid[x][y] > max:
                max = cGrid[x][y]
            if cGrid[x][y] < min:
                min = cGrid[x][y]

    #add min*-1 to all cells to get positive
    for x in range(cWidth):
        for y in range(cHeight):
            cGrid[x][y] += min * -1
    
    #update max value to get range ratio comparison
    max += min * -1

    #go trhough grid again and normalize, then multiply by amplitude
    for x in range(cWidth):
        for y in range(cHeight):
            cGrid[x][y] = (cGrid[x][y] / max) * amplitude

    #return final grid
    return cGrid
