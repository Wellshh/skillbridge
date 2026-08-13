# Class: DboGraphicBitMapInst(DboGraphicInstance):

Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicBitMapInst(x) : returns DboGraphicBitMapInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicBitMapInst(DboGraphicInstance):
GetDboBitMap() : returns DboBitMap
Class : DboGraphicBitMapInst(DboGraphicInstance):
Parameters:
GetBoundingBox() : returns CRect
Class : DboGraphicBitMapInst(DboGraphicInstance):
Parameters:
sGetLeft(obj, status) : returns int
Class : DboGraphicBitMapInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetTop(obj, status) : returns int
Class : DboGraphicBitMapInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetRight(obj, status) : returns int
Class : DboGraphicBitMapInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBottom(obj, status) : returns int
Class : DboGraphicBitMapInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *

---

status: DboState &
SetBoundingBox(rect) : returns DboState
Class : DboGraphicBitMapInst(DboGraphicInstance):
Parameters:
rect: CRect
END class DboGraphicBitMapInst(DboGraphicInstance):
DboGraphicBitMapInst_sGetLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBitMapInst_sGetTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBitMapInst_sGetRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBitMapInst_sGetBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicOleEmbedInst(x) : returns DboGraphicOleEmbedInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicOleEmbedInst(DboGraphicInstance):
GetDboOleEmbed() : returns DboOleEmbed
Class : DboGraphicOleEmbedInst(DboGraphicInstance):
Parameters:
GetBoundingBox() : returns CRect