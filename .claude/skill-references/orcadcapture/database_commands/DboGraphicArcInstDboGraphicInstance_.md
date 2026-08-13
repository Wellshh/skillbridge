# Class: DboGraphicArcInst(DboGraphicInstance):

obj: DboBaseObject *
status: DboState &
DboGraphicLineInst_sGetStartY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicLineInst_sGetEndX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicLineInst_sGetEndY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicLineInst_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicLineInst_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicArcInst(x) : returns DboGraphicArcInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicArcInst(DboGraphicInstance):
GetDboArc() : returns DboArc
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):

---

Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxRight(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartX(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartY(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndX(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetEndY(obj, status) : returns int
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
StatefulCreate() : returns DboBaseObject
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
offset: CPoint
SetBoundingRect(rect) : returns DboState
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
rect: CRect
SetStart(point) : returns DboState
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
point: CPoint
SetEnd(point) : returns DboState
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:

---

point: CPoint
SetLineStyle(style) : returns DboState
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboGraphicArcInst(DboGraphicInstance):
Parameters:
width: enum DboValue::LineWidthT
END class DboGraphicArcInst(DboGraphicInstance):
DboGraphicArcInst_sGetBoundingBoxLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetBoundingBoxBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetStartX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetStartY(obj, status) : returns int