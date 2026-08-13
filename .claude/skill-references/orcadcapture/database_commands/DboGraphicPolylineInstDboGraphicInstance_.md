# Class: DboGraphicPolylineInst(DboGraphicInstance):

DboGraphicPolygonInst_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicPolygonInst_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicPolygonInst_sGetFillStyle(obj, status) : returns FillStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicPolygonInst_sGetHatchStyle(obj, status) : returns HatchStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicPolylineInst(x) : returns DboGraphicPolylineInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicPolylineInst(DboGraphicInstance):
GetDboPolyline() : returns DboPolyline
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *

---

status: DboState &
StatefulCreate() : returns DboBaseObject
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
offset: CPoint
SetLineStyle(style) : returns DboState
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
width: enum DboValue::LineWidthT
NewPoint(point, position = -1) : returns DboState
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
point: CPoint
position: int
NewPoint(point) : returns DboState
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
point: CPoint
MovePoint(nPoint, offset) : returns DboState
Class : DboGraphicPolylineInst(DboGraphicInstance):
Parameters:
nPoint: int
offset: CPoint
END class DboGraphicPolylineInst(DboGraphicInstance):