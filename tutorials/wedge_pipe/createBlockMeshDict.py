
import math
from blockMeshDictClassV8 import *

# parameters
l1 = 0.025
l2 = 0.125
l3 = 0.150

d0 = 0.01
d1 = 0.01044842266

rAdd = d0*0.2

dX = dY = 0.5e-3
dZ = 1.0e-3

nCZ = 1

x0 = y0 = z0 = 0.0
grX = grY = grZ = "1.0"

wAng = 1.0 # wedge angle
yMax = dZ/math.atan(wAng/180*math.pi*0.5)

# create mesh
fvMesh = mesh()

### BLOCKS ###
# -- first block
xC, yC = x0, y0
xE, yE = xC+l1, yC+d0

# vertices
vertices = [
        [xC, yC, z0-yC/yMax*dZ],
        [xE, yC, z0-yC/yMax*dZ],
        [xE, yE, z0-yE/yMax*dZ],
        [xC, yE, z0-yE/yMax*dZ],
        [xC, yC, z0+yC/yMax*dZ],
        [xE, yC, z0+yC/yMax*dZ],
        [xE, yE, z0+yE/yMax*dZ],
        [xC, yE, z0+yE/yMax*dZ],
    ]

# neighbouring blocks
neighbours = []

# number of cells
nCX = int(round(abs(xE-xC)/dX))
nCY = int(round(abs(yE-yC)/dY))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
firstMid = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# -- second block
xC, yC = xE, y0
xE, yE = x0+l2, yC+d0

# vertices
vertices = [
        [xC, yC, z0-yC/yMax*dZ],
        [xE, yC, z0-yC/yMax*dZ],
        [xE, yE, z0-yE/yMax*dZ],
        [xC, yE, z0-yE/yMax*dZ],
        [xC, yC, z0+yC/yMax*dZ],
        [xE, yC, z0+yC/yMax*dZ],
        [xE, yE, z0+yE/yMax*dZ],
        [xC, yE, z0+yE/yMax*dZ],
    ]

# neighbouring blocks
neighbours = [firstMid]

# number of cells
nCX = int(round(abs(xE-xC)/dX))
nCY = int(round(abs(yE-yC)/dY))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
secondMid = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# -- second top block
xC, yC = xC, yE
xE, yE = xE, y0+d1

# vertices
vertices = [
        [xC, yC, z0-yC/yMax*dZ],
        [xE, yC, z0-yC/yMax*dZ],
        [xE, yE, z0-yE/yMax*dZ],
        [xC, yE, z0-yE/yMax*dZ],
        [xC, yC, z0+yC/yMax*dZ],
        [xE, yC, z0+yC/yMax*dZ],
        [xE, yE, z0+yE/yMax*dZ],
        [xC, yE, z0+yE/yMax*dZ],
    ]

# neighbouring blocks
neighbours = [secondMid]

# number of cells
nCX = int(round(abs(xE-xC)/dX))
nCY = int(round(abs(yE-yC)/dY))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
secondTop = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# -- third block
xC, yC = xE, y0
xE, yE = x0+l3, yC+d0

# vertices
vertices = [
        [xC, yC, z0-yC/yMax*dZ],
        [xE, yC, z0-yC/yMax*dZ],
        [xE, yE, z0-yE/yMax*dZ],
        [xC, yE, z0-yE/yMax*dZ],
        [xC, yC, z0+yC/yMax*dZ],
        [xE, yC, z0+yC/yMax*dZ],
        [xE, yE, z0+yE/yMax*dZ],
        [xC, yE, z0+yE/yMax*dZ],
    ]

# neighbouring blocks
neighbours = [secondMid]

# number of cells
nCX = int(round(abs(xE-xC)/dX))
nCY = int(round(abs(yE-yC)/dY))
nCells = [nCX, nCY, nCZ]

# grading
grading = [grX, grY, grZ]

# create the block
thirdMid = fvMesh.addBlock(vertices, neighbours, nCells, grading)

### PATCHES ###
# -- wedge patches
wedgeZ0 = list()
for block in fvMesh.blocks:
    wedgeZ0.append(block.retFXY0())

fvMesh.addPatch("wedgeZ0", "wedge", wedgeZ0)

wedgeZE = list()
for block in fvMesh.blocks:
    wedgeZE.append(block.retFXYE())

fvMesh.addPatch("wedgeZE", "wedge", wedgeZE)

# -- inlet
inlet = list()
inlet.append(firstMid.retFYZ0())

fvMesh.addPatch("inlet", "patch", inlet)

# -- outlet
outlet = list()
outlet.append(thirdMid.retFYZE())

fvMesh.addPatch("outlet", "patch", outlet)

# -- walls
walls = list()
walls.append(firstMid.retFXZ0())
walls.append(firstMid.retFXZE())

walls.append(secondMid.retFXZ0())

walls.append(secondTop.retFYZ0())
walls.append(secondTop.retFXZE())
walls.append(secondTop.retFYZE())

walls.append(thirdMid.retFXZ0())
walls.append(thirdMid.retFXZE())

fvMesh.addPatch("walls", "wall", walls)

### WRITE ###
fvMesh.writeBMD("./system/")
