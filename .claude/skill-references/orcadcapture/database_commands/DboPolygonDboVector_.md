# Class: DboPolygon(DboVector):

DboEllipse_sGetBoundingBoxBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboEllipse_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboEllipse_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboEllipse_sGetFillStyle(obj, status) : returns FillStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboEllipse_sGetHatchStyle(obj, status) : returns HatchStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboVectorToDboPolygon(x) : returns DboPolygon
Parameters:
x: DboVector *
START class DboPolygon(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboPolygon(DboVector):
Parameters:
GetLineStyle(status) : returns LineStyleT
Class : DboPolygon(DboVector):
Parameters:
status: DboState &

---

GetLineWidth(status) : returns LineWidthT
Class : DboPolygon(DboVector):
Parameters:
status: DboState &
GetFillStyle(status) : returns FillStyleT
Class : DboPolygon(DboVector):
Parameters:
status: DboState &
GetHatchStyle(status) : returns HatchStyleT
Class : DboPolygon(DboVector):
Parameters:
status: DboState &
GetCount(status) : returns int
Class : DboPolygon(DboVector):
Parameters:
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboPolygon(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboPolygon(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFillStyle(obj, status) : returns FillStyleT
Class : DboPolygon(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHatchStyle(obj, status) : returns HatchStyleT
Class : DboPolygon(DboVector):

---

Parameters:
obj: DboBaseObject *
status: DboState &
NewPointsIter(status) : returns DboPolygonPointsIter
Class : DboPolygon(DboVector):
Parameters:
status: DboState &
SetLineStyle(style) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
width: enum DboValue::LineWidthT
SetFillStyle(style) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
style: enum DboValue::FillStyleT
SetHatchStyle(style) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
style: enum DboValue::HatchStyleT
NewPoint(point, position = -1) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
point: CPoint
position: int
NewPoint(point) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
point: CPoint

---

RemovePoint(nIndex) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
nIndex: int
RemoveAllPoints() : returns DboState
Class : DboPolygon(DboVector):
Parameters:
MovePoint(position, ptOffset) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
position: int
ptOffset: CPoint &
Move(ptOffset) : returns DboState
Class : DboPolygon(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboPolygon(DboVector):
DboPolygon_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPolygon_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPolygon_sGetFillStyle(obj, status) : returns FillStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPolygon_sGetHatchStyle(obj, status) : returns HatchStyleT
Parameters:
obj: DboBaseObject *