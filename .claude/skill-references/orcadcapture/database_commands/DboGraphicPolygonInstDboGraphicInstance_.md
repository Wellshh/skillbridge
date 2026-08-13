# Class: DboGraphicPolygonInst(DboGraphicInstance):

x: DboGraphicInstance *
START class DboGraphicPolygonInst(DboGraphicInstance):
GetDboPolygon() : returns DboPolygon
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFillStyle(obj, status) : returns FillStyleT
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHatchStyle(obj, status) : returns HatchStyleT
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
StatefulCreate() : returns DboBaseObject
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
offset: CPoint

---

SetLineStyle(style) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
width: enum DboValue::LineWidthT
SetFillStyle(style) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
style: enum DboValue::FillStyleT
SetHatchStyle(style) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
style: enum DboValue::HatchStyleT
NewPoint(point, position = -1) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
point: CPoint
position: int
NewPoint(point) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
point: CPoint
MovePoint(nPoint, offset) : returns DboState
Class : DboGraphicPolygonInst(DboGraphicInstance):
Parameters:
nPoint: int
offset: CPoint
END class DboGraphicPolygonInst(DboGraphicInstance):