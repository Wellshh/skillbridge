# Class: DboBitMap(DboVector):

status: DboState &
DboCommentText_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboCommentText_sGetFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboVectorToDboBitMap(x) : returns DboBitMap
Parameters:
x: DboVector *
START class DboBitMap(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboBitMap(DboVector):
Parameters:
GetBoundingBox() : returns CRect
Class : DboBitMap(DboVector):
Parameters:
GetLocation(status) : returns CPoint
Class : DboBitMap(DboVector):
Parameters:
status: DboState &
GetDib(status) : returns HGLOBAL
Class : DboBitMap(DboVector):
Parameters:
status: DboState &
GetDibSize(status) : returns unsigned long
Class : DboBitMap(DboVector):
Parameters:
status: DboState &

---

GetBitmapDimension(status) : returns CSize
Class : DboBitMap(DboVector):
Parameters:
status: DboState &
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboBitMap(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxRight(obj, status) : returns int
Class : DboBitMap(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboBitMap(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboBitMap(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationX(obj, status) : returns int
Class : DboBitMap(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int
Class : DboBitMap(DboVector):
Parameters:
obj: DboBaseObject *

---

status: DboState &
SetLocation(point) : returns DboState
Class : DboBitMap(DboVector):
Parameters:
point: CPoint
SetBoundingBox(box) : returns DboState
Class : DboBitMap(DboVector):
Parameters:
box: CRect const
SetBitmapDimension(nWidth, nHeight) : returns DboState
Class : DboBitMap(DboVector):
Parameters:
nWidth: int
nHeight: int
END class DboBitMap(DboVector):
DboBitMap_sGetBoundingBoxLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBitMap_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBitMap_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboBitMap_sGetBoundingBoxBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &