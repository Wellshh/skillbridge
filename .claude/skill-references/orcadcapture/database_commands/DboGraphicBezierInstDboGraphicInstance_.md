# Class: DboGraphicBezierInst(DboGraphicInstance):

DboGraphicPolylineInst_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicPolylineInst_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicBezierInst(x) : returns DboGraphicBezierInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicBezierInst(DboGraphicInstance):
GetDboBezier() : returns DboBezier
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
StatefulCreate() : returns DboBaseObject
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
offset: CPoint

---

SetLineStyle(style) : returns DboState
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
width: enum DboValue::LineWidthT
NewPoint(point, position = -1) : returns DboState
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
point: CPoint
position: int
NewPoint(point) : returns DboState
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
point: CPoint
MovePoint(nPoint, offset) : returns DboState
Class : DboGraphicBezierInst(DboGraphicInstance):
Parameters:
nPoint: int
offset: CPoint
END class DboGraphicBezierInst(DboGraphicInstance):
DboGraphicBezierInst_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicBezierInst_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &