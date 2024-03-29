
from blockMeshDictClassV8 import *

# parameters
l1 = 0.025
l2 = 0.125
l3 = 0.150

d0 = 0.01
d1 = 0.01044842266

rAdd = d0*0.2

dX = dY = dZ = 0.5e-3

nCZ = 1

x0 = y0 = z0 = 0.0
grX = grY = grZ = "1.0"

# create mesh
fvMesh = mesh()

### BLOCKS ###
# -- first block
xC, yC, zC = x0, y0, z0
xE, yE, zE = xC+l1, yC+d0, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
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
xC, yC, zC = xE, y0, z0
xE, yE, zE = x0+l2, yC+d0, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
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

# add arc edge
fvMesh.addEdge("arc", secondMid.retEYEZ0(), [((xE+xC)*0.5, yE+rAdd, zC)])
fvMesh.addEdge("arc", secondMid.retEYEZE(), [((xE+xC)*0.5, yE+rAdd, zE)])
fvMesh.addEdge("arc", secondMid.retEY0Z0(), [((xE+xC)*0.5, yC-rAdd, zC)])
fvMesh.addEdge("arc", secondMid.retEY0ZE(), [((xE+xC)*0.5, yC-rAdd, zE)])

# -- second top block
xC, yC, zC = xC, yE, z0
xE, yE, zE = xE, y0+d1, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
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

# add arc edge
fvMesh.addEdge("arc", secondTop.retEYEZ0(), [((xE+xC)*0.5, yE+rAdd, zC)])
fvMesh.addEdge("arc", secondTop.retEYEZE(), [((xE+xC)*0.5, yE+rAdd, zE)])

# -- second bellow block
xC, yC, zC = xC, y0-(d1-d0), z0
xE, yE, zE = xE, y0, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
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
secondBel = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# add arc edge
fvMesh.addEdge("arc", secondBel.retEY0Z0(), [((xE+xC)*0.5, yC-rAdd, zC)])
fvMesh.addEdge("arc", secondBel.retEY0ZE(), [((xE+xC)*0.5, yC-rAdd, zE)])

# -- third block
xC, yC, zC = xE, y0, z0
xE, yE, zE = x0+l3, yC+d0, zC+dZ

# vertices
vertices = [
        [xC, yC, zC],
        [xE, yC, zC],
        [xE, yE, zC],
        [xC, yE, zC],
        [xC, yC, zE],
        [xE, yC, zE],
        [xE, yE, zE],
        [xC, yE, zE],
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
# -- empty
empty = list()
for block in fvMesh.blocks:
    empty.append(block.retFXY0())
    empty.append(block.retFXYE())

fvMesh.addPatch("frontAndBack", "empty", empty)

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
walls.append(thirdMid.retFXZ0())
walls.append(firstMid.retFXZE())

walls.append(secondTop.retFYZ0())
walls.append(secondTop.retFXZE())
walls.append(secondTop.retFYZE())

walls.append(secondBel.retFYZ0())
walls.append(secondBel.retFXZ0())
walls.append(secondBel.retFYZE())

walls.append(thirdMid.retFXZE())

fvMesh.addPatch("walls", "wall", walls)

### WRITE ###
fvMesh.writeBMD("./system/")
