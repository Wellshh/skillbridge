# Class: DboPolygonPointsIter

status: DboState &
START class DboPolygonPointsIter
Next(returnPt) : returns DboState
Class : DboPolygonPointsIter
Parameters:
returnPt: CPoint &
END class DboPolygonPointsIter
DboVectorToDboPolyline(x) : returns DboPolyline
Parameters:
x: DboVector *
START class DboPolyline(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboPolyline(DboVector):
Parameters:
GetLineStyle(status) : returns LineStyleT
Class : DboPolyline(DboVector):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboPolyline(DboVector):
Parameters:
status: DboState &
GetCount(status) : returns int
Class : DboPolyline(DboVector):
Parameters:
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboPolyline(DboVector):
Parameters:
obj: DboBaseObject *

---

status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboPolyline(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
NewPointsIter(status) : returns DboPolylinePointsIter
Class : DboPolyline(DboVector):
Parameters:
status: DboState &
SetLineStyle(style) : returns DboState
Class : DboPolyline(DboVector):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboPolyline(DboVector):
Parameters:
width: enum DboValue::LineWidthT
NewPoint(point, position = -1) : returns DboState
Class : DboPolyline(DboVector):
Parameters:
point: CPoint
position: int
NewPoint(point) : returns DboState
Class : DboPolyline(DboVector):
Parameters:
point: CPoint
RemovePoint(nIndex) : returns DboState
Class : DboPolyline(DboVector):
Parameters:
nIndex: int
RemoveAllPoints() : returns DboState

---

Class : DboPolyline(DboVector):
Parameters:
MovePoint(position, ptOffset) : returns DboState
Class : DboPolyline(DboVector):
Parameters:
position: int
ptOffset: CPoint &
Move(ptOffset) : returns DboState
Class : DboPolyline(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboPolyline(DboVector):
DboPolyline_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPolyline_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
START class DboPolylinePointsIter
Next(returnPt) : returns DboState
Class : DboPolylinePointsIter
Parameters:
returnPt: CPoint &
END class DboPolylinePointsIter
DboVectorToDboBezier(x) : returns DboBezier
Parameters:
x: DboVector *
START class DboBezier(DboVector):

---

GetObjectType() : returns ObjectTypeT
Class : DboBezier(DboVector):
Parameters:
GetLineStyle(status) : returns LineStyleT
Class : DboBezier(DboVector):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboBezier(DboVector):
Parameters:
status: DboState &
GetCount(status) : returns int
Class : DboBezier(DboVector):
Parameters:
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboBezier(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboBezier(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
NewPointsIter(status) : returns DboBezierPointsIter
Class : DboBezier(DboVector):
Parameters:
status: DboState &
SetLineStyle(style) : returns DboState
Class : DboBezier(DboVector):
Parameters:

---

style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboBezier(DboVector):
Parameters:
width: enum DboValue::LineWidthT
NewPoint(point, position = -1) : returns DboState
Class : DboBezier(DboVector):
Parameters:
point: CPoint
position: int
NewPoint(point) : returns DboState
Class : DboBezier(DboVector):
Parameters:
point: CPoint
RemovePoint(nIndex) : returns DboState
Class : DboBezier(DboVector):
Parameters:
nIndex: int
RemoveAllPoints() : returns DboState
Class : DboBezier(DboVector):
Parameters:
MovePoint(position, ptOffset) : returns DboState
Class : DboBezier(DboVector):
Parameters:
position: int
ptOffset: CPoint &
Move(ptOffset) : returns DboState
Class : DboBezier(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboBezier(DboVector):