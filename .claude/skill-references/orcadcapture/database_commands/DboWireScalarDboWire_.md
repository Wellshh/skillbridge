# Class: DboWireScalar(DboWire):

status: DboState &
DboWire_sGetNetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboWire_PointOnLine(point, LineStart, LineEnd) : returns int
Parameters:
point: CPoint
LineStart: CPoint
LineEnd: CPoint
DboWire_LinesIntersect(Start1, End1, Start2, End2) : returns int
Parameters:
Start1: CPoint
End1: CPoint
Start2: CPoint
End2: CPoint
DboWire_GetLinesIntersect(Start1, End1, Start2, End2, Intersection) : returns int
Parameters:
Start1: CPoint
End1: CPoint
Start2: CPoint
End2: CPoint
Intersection: CPoint &
DboWire_LineIntersectsRect(rect, LineStart, LineEnd) : returns int
Parameters:
rect: CRect
LineStart: CPoint
LineEnd: CPoint
DboWireToDboWireScalar(x) : returns DboWireScalar
Parameters:
x: DboWire *
START class DboWireScalar(DboWire):

---

GetObjectType() : returns ObjectTypeT
Class : DboWireScalar(DboWire):
Parameters:
SetName(name) : returns DboState
Class : DboWireScalar(DboWire):
Parameters:
name: CString &
DeleteAlias(pAlias) : returns DboState
Class : DboWireScalar(DboWire):
Parameters:
pAlias: DboAlias *
END class DboWireScalar(DboWire):
DboWireToDboWireBus(x) : returns DboWireBus
Parameters:
x: DboWire *
START class DboWireBus(DboWire):
GetObjectType() : returns ObjectTypeT
Class : DboWireBus(DboWire):
Parameters:
IsBundleObject() : returns bool
Class : DboWireBus(DboWire):
Parameters:
NormalizeBundleWire() : returns DboState
Class : DboWireBus(DboWire):
Parameters:
SetName(name) : returns DboState
Class : DboWireBus(DboWire):
Parameters:
name: CString &
NewAlias(status, alias, location, font, rotation, color, ID = None) : returns DboAlias