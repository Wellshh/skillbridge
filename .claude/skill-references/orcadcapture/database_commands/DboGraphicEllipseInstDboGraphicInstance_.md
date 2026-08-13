# Class: DboGraphicEllipseInst(DboGraphicInstance):

Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetEndX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetEndY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicArcInst_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicEllipseInst(x) : returns DboGraphicEllipseInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicEllipseInst(DboGraphicInstance):
GetDboEllipse() : returns DboEllipse
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetBoundingBoxRight(obj, status) : returns int
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFillStyle(obj, status) : returns FillStyleT
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHatchStyle(obj, status) : returns HatchStyleT
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *

---

status: DboState &
StatefulCreate() : returns DboBaseObject
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
offset: CPoint
SetBoundingRect(rect) : returns DboState
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
rect: CRect
SetLineStyle(style) : returns DboState
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
width: enum DboValue::LineWidthT
SetFillStyle(style) : returns DboState
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
style: enum DboValue::FillStyleT
SetHatchStyle(style) : returns DboState
Class : DboGraphicEllipseInst(DboGraphicInstance):
Parameters:
style: enum DboValue::HatchStyleT
END class DboGraphicEllipseInst(DboGraphicInstance):
DboGraphicEllipseInst_sGetBoundingBoxLeft(obj, status) : returns int
Parameters: