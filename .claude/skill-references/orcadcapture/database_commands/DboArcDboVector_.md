# Class: DboArc(DboVector):

DboLine_sGetEndY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLine_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboLine_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboVectorToDboArc(x) : returns DboArc
Parameters:
x: DboVector *
START class DboArc(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboArc(DboVector):
Parameters:
GetBoundingBox() : returns CRect
Class : DboArc(DboVector):
Parameters:
GetStart(status) : returns CPoint
Class : DboArc(DboVector):
Parameters:
status: DboState &
GetEnd(status) : returns CPoint
Class : DboArc(DboVector):
Parameters:
status: DboState &
GetLineStyle(status) : returns LineStyleT

---

Class : DboArc(DboVector):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboArc(DboVector):
Parameters:
status: DboState &
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxRight(obj, status) : returns int
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartX(obj, status) : returns int
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartY(obj, status) : returns int

---

Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndX(obj, status) : returns int
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndY(obj, status) : returns int
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboArc(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
SetBoundingBox(box) : returns DboState
Class : DboArc(DboVector):
Parameters:
box: CRect
SetStart(point) : returns DboState
Class : DboArc(DboVector):
Parameters:
point: CPoint
SetEnd(point) : returns DboState

---

Class : DboArc(DboVector):
Parameters:
point: CPoint
SetLineStyle(style) : returns DboState
Class : DboArc(DboVector):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboArc(DboVector):
Parameters:
width: enum DboValue::LineWidthT
Move(ptOffset) : returns DboState
Class : DboArc(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboArc(DboVector):
DboArc_sGetBoundingBoxLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetBoundingBoxBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &