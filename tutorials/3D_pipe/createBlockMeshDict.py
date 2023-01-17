
from blockMeshDictClassV8 import *

# auxiliar functions
def squareSideLength(diameter):
    sqrDiag = sqrRatio*diameter
    sqrSide = sqrDiag/math.sqrt(2)
    return sqrSide

def sideResidue(diameter):
    diagRes = (1-sqrRatio)*diameter
    sideRes = diagRes/math.sqrt(2)/2
    return sideRes

# parameters
# inlet diameter
DIn = 0.02
DIn2 = 0.03

# outlet diameter
DOut = 0.1

# length
L = 0.1

# origin
x0 = y0 = z0 = 0.0

# cell size
dX = dY = dZ = 1e-3

# auxiliar computation
RIn = DIn*0.5
RIn2 = DIn2*0.5
ROut = DOut*0.5

global sqrRatio
sqrRatio = 3/4
cirRatio = 0.25

# number of cells
nCX  = int(round(L/dX))

# mesh grading (basic)
grX, grY, grZ = "1.0", "1.0", "1.0"

# mesh scale
mScale  = 1

# number of cells
SHSide = squareSideLength(RIn*2)
nCRY = int(round(SHSide/dY))
nCRZ = int(round(SHSide/dZ))

# note, I assume dY = dZ
densK = 2.0
nCAR = int(round((1-sqrRatio)*RIn*(1-cirRatio)*densK/dY))
nCBR = int(round((RIn2-RIn)/dY))
nCCR = int(round((ROut-RIn2)/dY))

nCCir = int(round(SHSide/dZ))

# create mesh
fvMesh = mesh()

# -----------------------------------
# - inner rectangle
SHSide = squareSideLength(RIn*2)/2
rRec = SHSide+(RIn-SHSide)*cirRatio

xC, xE = x0, x0+L
yC, yE = y0-SHSide, y0+SHSide
zC, zE = z0-SHSide, z0+SHSide

xCR, xER = xC, xE
yCR, yER = yC, yE
zCR, zER = zC, zE

# vertex coordinates
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
nCells = [nCX, nCRY, nCRZ]

# grading
grading = [grX, grY, grZ]

# create the block
ARec = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", ARec.retEX0Z0(), [(xC, y0, z0-rRec)])
fvMesh.addEdge("arc", ARec.retEX0YE(), [(xC, y0+rRec, z0)])
fvMesh.addEdge("arc", ARec.retEX0ZE(), [(xC, y0, z0+rRec)])
fvMesh.addEdge("arc", ARec.retEX0Y0(), [(xC, y0-rRec, z0)])

fvMesh.addEdge("arc", ARec.retEXEZ0(), [(xE, y0, z0-rRec)])
fvMesh.addEdge("arc", ARec.retEXEYE(), [(xE, y0+rRec, z0)])
fvMesh.addEdge("arc", ARec.retEXEZE(), [(xE, y0, z0+rRec)])
fvMesh.addEdge("arc", ARec.retEXEY0(), [(xE, y0-rRec, z0)])

# - A, top part
sideRes = sideResidue(RIn*2)
radius = RIn

xC, xE = xCR, xER
yC, yE = yER, yER+sideRes

zC01, zE01 = z0-SHSide, z0+SHSide
zC02, zE02 = z0-SHSide-sideRes, z0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC, zC01],
        [xE, yC, zC01],
        [xE, yE, zC02],
        [xC, yE, zC02],
        [xC, yC, zE01],
        [xE, yC, zE01],
        [xE, yE, zE02],
        [xC, yE, zE02],
    ]

# neighbouring blocks
neighbours = [ARec]

# number of cells
nCells = [nCX, nCAR, nCCir]

# grading
grading = [grX, grY, grZ]

# create the block
ATop = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", ATop.retEX0YE(), [(xC, y0+radius, z0)])
fvMesh.addEdge("arc", ATop.retEXEYE(), [(xE, y0+radius, z0)])

# - A, bottom part
xC, xE = xCR, xER
yC, yE = yCR-sideRes, yCR

zC02, zE02 = z0-SHSide, z0+SHSide
zC01, zE01 = z0-SHSide-sideRes, z0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC, zC01],
        [xE, yC, zC01],
        [xE, yE, zC02],
        [xC, yE, zC02],
        [xC, yC, zE01],
        [xE, yC, zE01],
        [xE, yE, zE02],
        [xC, yE, zE02],
    ]

# neighbouring blocks
neighbours = [ARec]

# number of cells
nCells = [nCX, nCAR, nCCir]

# grading
grading = [grX, grY, grZ]

# create the block
ABottom = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", ABottom.retEX0Y0(), [(xC, y0-radius, z0)])
fvMesh.addEdge("arc", ABottom.retEXEY0(), [(xE, y0-radius, z0)])

# - A, right part
xC, xE = xCR, xER
zC, zE = zER, zER+sideRes

yC02, yE02 = y0-SHSide, y0+SHSide
yC01, yE01 = y0-SHSide-sideRes, y0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC02, zC],
        [xE, yC02, zC],
        [xE, yE02, zC],
        [xC, yE02, zC],
        [xC, yC01, zE],
        [xE, yC01, zE],
        [xE, yE01, zE],
        [xC, yE01, zE],
    ]

# neighbouring blocks
neighbours = [ARec, ATop, ABottom]

# number of cells
nCells = [nCX, nCCir, nCAR]

# grading
grading = [grX, grY, grZ]

# create the block
ARight = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", ARight.retEX0ZE(), [(xC, y0, z0+radius)])
fvMesh.addEdge("arc", ARight.retEXEZE(), [(xE, y0, z0+radius)])

# - A, left part
xC, xE = xCR, xER
zC, zE = zCR-sideRes, zCR

yC01, yE01 = y0-SHSide, y0+SHSide
yC02, yE02 = y0-SHSide-sideRes, y0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC02, zC],
        [xE, yC02, zC],
        [xE, yE02, zC],
        [xC, yE02, zC],
        [xC, yC01, zE],
        [xE, yC01, zE],
        [xE, yE01, zE],
        [xC, yE01, zE],
    ]

# neighbouring blocks
neighbours = [ARec, ATop, ABottom]

# number of cells
nCells = [nCX, nCCir, nCAR]

# grading
grading = [grX, grY, grZ]

# create the block
ALeft = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", ALeft.retEX0Z0(), [(xC, y0, z0-radius)])
fvMesh.addEdge("arc", ALeft.retEXEZ0(), [(xE, y0, z0-radius)])

# - B, inner rectangle, fictional
rRec = radius
SHSide = rRec/math.sqrt(2)

yC, yE = y0-SHSide, y0+SHSide
zC, zE = z0-SHSide, z0+SHSide

xCR, xER = xC, xE
yCR, yER = yC, yE
zCR, zER = zC, zE

# number of cells
nCX = int(round(abs(xE-xC)/dX))

# - B, top part
sideRes = ((RIn2-RIn))/math.sqrt(2)
radius = RIn2

xC, xE = xCR, xER
yC, yE = yER, yER+sideRes

zC01, zE01 = z0-SHSide, z0+SHSide
zC02, zE02 = z0-SHSide-sideRes, z0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC, zC01],
        [xE, yC, zC01],
        [xE, yE, zC02],
        [xC, yE, zC02],
        [xC, yC, zE01],
        [xE, yC, zE01],
        [xE, yE, zE02],
        [xC, yE, zE02],
    ]

# neighbouring blocks
neighbours = [ATop]

# number of cells
nCells = [nCX, nCBR, nCCir]

# grading
grading = [grX, grY, grZ]

# create the block
BTop = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", BTop.retEX0YE(), [(xC, y0+radius, z0)])
fvMesh.addEdge("arc", BTop.retEXEYE(), [(xE, y0+radius, z0)])

# - B, bottom part
xC, xE = xCR, xER
yC, yE = yCR-sideRes, yCR

zC02, zE02 = z0-SHSide, z0+SHSide
zC01, zE01 = z0-SHSide-sideRes, z0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC, zC01],
        [xE, yC, zC01],
        [xE, yE, zC02],
        [xC, yE, zC02],
        [xC, yC, zE01],
        [xE, yC, zE01],
        [xE, yE, zE02],
        [xC, yE, zE02],
    ]

# neighbouring blocks
neighbours = [ABottom]

# number of cells
nCells = [nCX, nCBR, nCCir]

# grading
grading = [grX, grY, grZ]

# create the block
BBottom = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", BBottom.retEX0Y0(), [(xC, y0-radius, z0)])
fvMesh.addEdge("arc", BBottom.retEXEY0(), [(xE, y0-radius, z0)])

# - B, right part
xC, xE = xCR, xER
zC, zE = zER, zER+sideRes

yC02, yE02 = y0-SHSide, y0+SHSide
yC01, yE01 = y0-SHSide-sideRes, y0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC02, zC],
        [xE, yC02, zC],
        [xE, yE02, zC],
        [xC, yE02, zC],
        [xC, yC01, zE],
        [xE, yC01, zE],
        [xE, yE01, zE],
        [xC, yE01, zE],
    ]

# neighbouring blocks
neighbours = [BTop, BBottom, ARight]

# number of cells
nCells = [nCX, nCCir, nCBR]

# grading
grading = [grX, grY, grZ]

# create the block
BRight = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", BRight.retEX0ZE(), [(xC, y0, z0+radius)])
fvMesh.addEdge("arc", BRight.retEXEZE(), [(xE, y0, z0+radius)])

# - B, left part
xC, xE = xCR, xER
zC, zE = zCR-sideRes, zCR

yC01, yE01 = y0-SHSide, y0+SHSide
yC02, yE02 = y0-SHSide-sideRes, y0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC02, zC],
        [xE, yC02, zC],
        [xE, yE02, zC],
        [xC, yE02, zC],
        [xC, yC01, zE],
        [xE, yC01, zE],
        [xE, yE01, zE],
        [xC, yE01, zE],
    ]

# neighbouring blocks
neighbours = [BTop, BBottom, ALeft]

# number of cells
nCells = [nCX, nCCir, nCBR]

# grading
grading = [grX, grY, grZ]

# create the block
BLeft = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", BLeft.retEX0Z0(), [(xC, y0, z0-radius)])
fvMesh.addEdge("arc", BLeft.retEXEZ0(), [(xE, y0, z0-radius)])

# - C, inner rectangle, fictional
rRec = radius
SHSide = rRec/math.sqrt(2)

yC, yE = y0-SHSide, y0+SHSide
zC, zE = z0-SHSide, z0+SHSide

xCR, xER = xC, xE
yCR, yER = yC, yE
zCR, zER = zC, zE

# number of cells
nCX = int(round(abs(xE-xC)/dX))

# - C, top part
sideRes = ((ROut-RIn2))/math.sqrt(2)
radius = ROut

xC, xE = xCR, xER
yC, yE = yER, yER+sideRes

zC01, zE01 = z0-SHSide, z0+SHSide
zC02, zE02 = z0-SHSide-sideRes, z0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC, zC01],
        [xE, yC, zC01],
        [xE, yE, zC02],
        [xC, yE, zC02],
        [xC, yC, zE01],
        [xE, yC, zE01],
        [xE, yE, zE02],
        [xC, yE, zE02],
    ]

# neighbouring blocks
neighbours = [BTop]

# number of cells
nCells = [nCX, nCCR, nCCir]

# grading
grading = [grX, grY, grZ]

# create the block
CTop = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", CTop.retEX0YE(), [(xC, y0+radius, z0)])
fvMesh.addEdge("arc", CTop.retEXEYE(), [(xE, y0+radius, z0)])

# - C, bottom part
xC, xE = xCR, xER
yC, yE = yCR-sideRes, yCR

zC02, zE02 = z0-SHSide, z0+SHSide
zC01, zE01 = z0-SHSide-sideRes, z0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC, zC01],
        [xE, yC, zC01],
        [xE, yE, zC02],
        [xC, yE, zC02],
        [xC, yC, zE01],
        [xE, yC, zE01],
        [xE, yE, zE02],
        [xC, yE, zE02],
    ]

# neighbouring blocks
neighbours = [BBottom]

# number of cells
nCells = [nCX, nCCR, nCCir]

# grading
grading = [grX, grY, grZ]

# create the block
CBottom = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", CBottom.retEX0Y0(), [(xC, y0-radius, z0)])
fvMesh.addEdge("arc", CBottom.retEXEY0(), [(xE, y0-radius, z0)])

# - C, right part
xC, xE = xCR, xER
zC, zE = zER, zER+sideRes

yC02, yE02 = y0-SHSide, y0+SHSide
yC01, yE01 = y0-SHSide-sideRes, y0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC02, zC],
        [xE, yC02, zC],
        [xE, yE02, zC],
        [xC, yE02, zC],
        [xC, yC01, zE],
        [xE, yC01, zE],
        [xE, yE01, zE],
        [xC, yE01, zE],
    ]

# neighbouring blocks
neighbours = [CTop, CBottom, BRight]

# number of cells
nCells = [nCX, nCCir, nCCR]

# grading
grading = [grX, grY, grZ]

# create the block
CRight = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", CRight.retEX0ZE(), [(xC, y0, z0+radius)])
fvMesh.addEdge("arc", CRight.retEXEZE(), [(xE, y0, z0+radius)])

# - C, left part
xC, xE = xCR, xER
zC, zE = zCR-sideRes, zCR

yC01, yE01 = y0-SHSide, y0+SHSide
yC02, yE02 = y0-SHSide-sideRes, y0+SHSide+sideRes

# vertex coordinates
vertices = [
        [xC, yC02, zC],
        [xE, yC02, zC],
        [xE, yE02, zC],
        [xC, yE02, zC],
        [xC, yC01, zE],
        [xE, yC01, zE],
        [xE, yE01, zE],
        [xC, yE01, zE],
    ]

# neighbouring blocks
neighbours = [CTop, CBottom, BLeft]

# number of cells
nCells = [nCX, nCCir, nCCR]

# grading
grading = [grX, grY, grZ]

# create the block
CLeft = fvMesh.addBlock(vertices, neighbours, nCells, grading)

# define special edges
fvMesh.addEdge("arc", CLeft.retEX0Z0(), [(xC, y0, z0-radius)])
fvMesh.addEdge("arc", CLeft.retEXEZ0(), [(xE, y0, z0-radius)])

#-----------------------------------------------------------------------
# prepare boundaries

# -- walls - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# other walls
walls = []
walls.append(BTop.retFYZ0())
walls.append(BBottom.retFYZ0())
walls.append(BLeft.retFYZ0())
walls.append(BRight.retFYZ0())

walls.append(CTop.retFYZ0())
walls.append(CBottom.retFYZ0())
walls.append(CLeft.retFYZ0())
walls.append(CRight.retFYZ0())

fvMesh.addPatch("walls", "wall", walls)

# -- in/out - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - inlet boundary
inlet = []
inlet.append(ARec.retFYZ0())
inlet.append(ATop.retFYZ0())
inlet.append(ABottom.retFYZ0())
inlet.append(ALeft.retFYZ0())
inlet.append(ARight.retFYZ0())

fvMesh.addPatch("inlet", "patch", inlet)

outlet = []
outlet.append(ARec.retFYZE())
outlet.append(ATop.retFYZE())
outlet.append(ABottom.retFYZE())
outlet.append(ALeft.retFYZE())
outlet.append(ARight.retFYZE())

outlet.append(BTop.retFYZE())
outlet.append(BBottom.retFYZE())
outlet.append(BLeft.retFYZE())
outlet.append(BRight.retFYZE())

outlet.append(CTop.retFYZE())
outlet.append(CBottom.retFYZE())
outlet.append(CLeft.retFYZE())
outlet.append(CRight.retFYZE())

fvMesh.addPatch("outlet", "patch", outlet)

atmosphere = []
atmosphere.append(CTop.retFXZE())
atmosphere.append(CBottom.retFXZ0())
atmosphere.append(CLeft.retFXY0())
atmosphere.append(CRight.retFXYE())

fvMesh.addPatch("atmosphere", "patch", atmosphere)

### WRITE ###
fvMesh.writeBMD("./system/")
