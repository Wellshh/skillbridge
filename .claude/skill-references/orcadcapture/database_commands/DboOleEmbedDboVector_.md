# Class: DboOleEmbed(DboVector):

DboBitMap_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBitMap_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboVectorToDboOleEmbed(x) : returns DboOleEmbed
Parameters:
x: DboVector *
START class DboOleEmbed(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboOleEmbed(DboVector):
Parameters:
GetBoundingBox() : returns CRect
Class : DboOleEmbed(DboVector):
Parameters:
GetLocation(status) : returns CPoint
Class : DboOleEmbed(DboVector):
Parameters:
status: DboState &
GetByte(status) : returns unsigned char
Class : DboOleEmbed(DboVector):
Parameters:
status: DboState &
SetByte(pByte)
Class : DboOleEmbed(DboVector):
Parameters:
pByte: unsigned char *
GetDibSize(status) : returns unsigned long

---

Class : DboOleEmbed(DboVector):
Parameters:
status: DboState &
GetBitmapDimension(status) : returns CSize
Class : DboOleEmbed(DboVector):
Parameters:
status: DboState &
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboOleEmbed(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxRight(obj, status) : returns int
Class : DboOleEmbed(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboOleEmbed(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboOleEmbed(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationX(obj, status) : returns int
Class : DboOleEmbed(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int

---

Class : DboOleEmbed(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
SetLocation(point) : returns DboState
Class : DboOleEmbed(DboVector):
Parameters:
point: CPoint
SetBoundingBox(box) : returns DboState
Class : DboOleEmbed(DboVector):
Parameters:
box: CRect const
SetBitmapDimension(nWidth, nHeight) : returns DboState
Class : DboOleEmbed(DboVector):
Parameters:
nWidth: int
nHeight: int
END class DboOleEmbed(DboVector):
DboOleEmbed_sGetBoundingBoxLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboOleEmbed_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboOleEmbed_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboOleEmbed_sGetBoundingBoxBottom(obj, status) : returns int
Parameters: