<!--
source: database_commands/DboSchematicNetBusMembersIterTBaseDboSchematicNetsIter_.md
part: 2/2
-->

color: enum DboValue::ColorT
bNewVersion: int
style: enum DboValue::LineStyleT
width: enum DboValue::LineWidthT
NewWireScalar(status, start, end, color = DEFAULT_OBJECT_COLOR, bNewVersion = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
bNewVersion: int
style: enum DboValue::LineStyleT
NewWireScalar(status, start, end, color = DEFAULT_OBJECT_COLOR, bNewVersion = 0) : returns
DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
bNewVersion: int
NewWireScalar(status, start, end, color = DEFAULT_OBJECT_COLOR) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
NewWireScalar(status, start, end) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &

---

start: CPoint
end: CPoint
NewWireScalar(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bNewVersion = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE, width = DEFAULT_LINE_WIDTH) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bNewVersion: int
style: enum DboValue::LineStyleT
width: enum DboValue::LineWidthT
NewWireScalar(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bNewVersion = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bNewVersion: int
style: enum DboValue::LineStyleT
NewWireScalar(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bNewVersion = 0) : returns DboWireScalar
Class : DboPage(DboBaseObject):

---

Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bNewVersion: int
NewWireScalar(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR) :
returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
NewWireScalar(status, start, end, bJunctionStart, bJunctionEnd) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
NewWireScalar(status, bNewVersion = 0) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
bNewVersion: int
NewWireScalar(status) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &

---

NewWireScalar(pSource, status, bNewVersion = 0) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboWireScalar *
status: DboState &
bNewVersion: int
NewWireScalar(pSource, status) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboWireScalar *
status: DboState &
NewWireBus(status, Name, start, end, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bBundle = 0, style = DEFAULT_LINE_STYLE,
Class : DboPage(DboBaseObject):
width = DEFAULT_LINE_WIDTH) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
bBundle: int
style: enum DboValue::LineStyleT
width: enum DboValue::LineWidthT
NewWireBus(status, Name, start, end, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bBundle = 0, style = DEFAULT_LINE_STYLE) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
bBundle: int

---

style: enum DboValue::LineStyleT
NewWireBus(status, Name, start, end, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bBundle = 0) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
bBundle: int
NewWireBus(status, Name, start, end, color = DEFAULT_OBJECT_COLOR) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
NewWireBus(status, Name, start, end) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
NewWireBus(status, start, end, color = DEFAULT_OBJECT_COLOR, bBundle = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE, width = DEFAULT_LINE_WIDTH) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
color: enum DboValue::ColorT

---

bBundle: int
style: enum DboValue::LineStyleT
width: enum DboValue::LineWidthT
NewWireBus(status, start, end, color = DEFAULT_OBJECT_COLOR, bBundle = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
bBundle: int
style: enum DboValue::LineStyleT
NewWireBus(status, start, end, color = DEFAULT_OBJECT_COLOR, bBundle = 0) : returns
DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
bBundle: int
NewWireBus(status, start, end, color = DEFAULT_OBJECT_COLOR) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
color: enum DboValue::ColorT
NewWireBus(status, start, end) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint

---

NewWireBus(status, Name, start, end, bJunctionStart, bJunctionEnd,
Class : DboPage(DboBaseObject):
color = DEFAULT_OBJECT_COLOR, bBundle = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE, width = DEFAULT_LINE_WIDTH) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bBundle: int
style: enum DboValue::LineStyleT
width: enum DboValue::LineWidthT
NewWireBus(status, Name, start, end, bJunctionStart, bJunctionEnd,
Class : DboPage(DboBaseObject):
color = DEFAULT_OBJECT_COLOR, bBundle = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bBundle: int
style: enum DboValue::LineStyleT
NewWireBus(status, Name, start, end, bJunctionStart, bJunctionEnd,
Class : DboPage(DboBaseObject):
color = DEFAULT_OBJECT_COLOR, bBundle = 0) : returns DboWireBus
Class : DboPage(DboBaseObject):

---

Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bBundle: int
NewWireBus(status, Name, start, end, bJunctionStart, bJunctionEnd,
Class : DboPage(DboBaseObject):
color = DEFAULT_OBJECT_COLOR) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
NewWireBus(status, Name, start, end, bJunctionStart, bJunctionEnd) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
NewWireBus(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bNewVersion = 0,
Class : DboPage(DboBaseObject):
bBundle = 0, style = DEFAULT_LINE_STYLE, width = DEFAULT_LINE_WIDTH) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bNewVersion: int
bBundle: int
style: enum DboValue::LineStyleT
width: enum DboValue::LineWidthT
NewWireBus(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bNewVersion = 0,
Class : DboPage(DboBaseObject):
bBundle = 0, style = DEFAULT_LINE_STYLE) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bNewVersion: int
bBundle: int
style: enum DboValue::LineStyleT
NewWireBus(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bNewVersion = 0,
Class : DboPage(DboBaseObject):
bBundle = 0) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int

---

color: enum DboValue::ColorT
bNewVersion: int
bBundle: int
NewWireBus(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
bNewVersion = 0) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
bNewVersion: int
NewWireBus(status, start, end, bJunctionStart, bJunctionEnd, color = DEFAULT_OBJECT_COLOR) :
returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
color: enum DboValue::ColorT
NewWireBus(status, start, end, bJunctionStart, bJunctionEnd) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
bJunctionStart: int
bJunctionEnd: int
NewWireBus(status, bBundle = 0) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
bBundle: int
NewWireBus(status) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewWireBus(pSource, status, bNewVersion = 0) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboWireBus *
status: DboState &
bNewVersion: int
NewWireBus(pSource, status) : returns DboWireBus
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboWireBus *
status: DboState &
NewBusEntry(status, BusPoint, EndPoint, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
nID = 0) : returns DboBusEntry
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
BusPoint: CPoint
EndPoint: CPoint
color: enum DboValue::ColorT
nID: unsigned long
NewBusEntry(status, BusPoint, EndPoint, color = DEFAULT_OBJECT_COLOR) : returns DboBusEntry
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
BusPoint: CPoint
EndPoint: CPoint
color: enum DboValue::ColorT

---

NewBusEntry(status, BusPoint, EndPoint) : returns DboBusEntry
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
BusPoint: CPoint
EndPoint: CPoint
NewBusEntry(pSource, status, bNewVersion = 0) : returns DboBusEntry
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboBusEntry *
status: DboState &
bNewVersion: int
NewBusEntry(pSource, status) : returns DboBusEntry
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboBusEntry *
status: DboState &
AddJunctionToWire(location, status)
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &
NewTitleBlock(status, symbol, Name) : returns DboTitleBlock
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
symbol: DboTitleBlockSymbol *
Name: CString &
NewTitleBlock(pSource, status, bNewVersion = 0) : returns DboTitleBlock
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboTitleBlock *
status: DboState &
bNewVersion: int

---

NewTitleBlock(pSource, status) : returns DboTitleBlock
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboTitleBlock *
status: DboState &
NewGlobal(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0, nId = 0) : returns DboGlobal
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboGlobalSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
nId: unsigned long
NewGlobal(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0) : returns DboGlobal
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboGlobalSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
NewGlobal(status, Name, symbol, location, rotation = NOROTATION) : returns DboGlobal
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboGlobalSymbol *
location: CPoint
rotation: enum DboValue::RotationT

---

NewGlobal(status, Name, symbol, location) : returns DboGlobal
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboGlobalSymbol *
location: CPoint
NewGlobal(pSource, status, bNewVersion = 0) : returns DboGlobal
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGlobal *
status: DboState &
bNewVersion: int
NewGlobal(pSource, status) : returns DboGlobal
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGlobal *
status: DboState &
NewPort(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0, nID = 0) : returns DboPort
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboPortSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
nID: unsigned long
NewPort(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0) : returns DboPort
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &

---

Name: CString &
symbol: DboPortSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
NewPort(status, Name, symbol, location, rotation = NOROTATION) : returns DboPort
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboPortSymbol *
location: CPoint
rotation: enum DboValue::RotationT
NewPort(status, Name, symbol, location) : returns DboPort
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboPortSymbol *
location: CPoint
NewPort(pSource, status, bNewVersion = 0) : returns DboPort
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboPort *
status: DboState &
bNewVersion: int
NewPort(pSource, status) : returns DboPort
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboPort *
status: DboState &
NewOffPageConnector(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0, nId = 0) : returns DboOffPageConnector
Class : DboPage(DboBaseObject):

---

Parameters:
status: DboState &
Name: CString &
symbol: DboOffPageSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
nId: unsigned long
NewOffPageConnector(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0) : returns DboOffPageConnector
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboOffPageSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
NewOffPageConnector(status, Name, symbol, location, rotation = NOROTATION) : returns
DboOffPageConnector
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboOffPageSymbol *
location: CPoint
rotation: enum DboValue::RotationT
NewOffPageConnector(status, Name, symbol, location) : returns DboOffPageConnector
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboOffPageSymbol *
location: CPoint
NewOffPageConnector(pSource, status, bNewVersion = 0) : returns DboOffPageConnector

---

Class : DboPage(DboBaseObject):
Parameters:
pSource: DboOffPageConnector *
status: DboState &
bNewVersion: int
NewOffPageConnector(pSource, status) : returns DboOffPageConnector
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboOffPageConnector *
status: DboState &
NewCommentGraphic(status, location, rotation) : returns DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint
rotation: enum DboValue::RotationT
NewCommentGraphic(status, graphic, location, rotation, objType = GRAPHIC_INSTANCE) : returns
DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
graphic: DboGraphicObject *
location: CPoint
rotation: enum DboValue::RotationT
objType: enum DboBaseObject::ObjectTypeT
NewCommentGraphic(status, graphic, location, rotation) : returns DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
graphic: DboGraphicObject *
location: CPoint
rotation: enum DboValue::RotationT
NewCommentGraphic(pSource, status, bNewVersion = 0) : returns DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:

---

pSource: DboGraphicInstance *
status: DboState &
bNewVersion: int
NewCommentGraphic(pSource, status) : returns DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicInstance *
status: DboState &
NewGraphicSymbolVectorInst(status, location, rotation) : returns DboGraphicSymbolVectorInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint
rotation: enum DboValue::RotationT
NewGraphicBoxInst(status, rect, location, rotation, nId = 0) : returns DboGraphicBoxInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rect: CRect &
location: CPoint
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicBoxInst(status, rect, location, rotation) : returns DboGraphicBoxInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rect: CRect &
location: CPoint
rotation: enum DboValue::RotationT
NewGraphicBoxInst(pSource, status, bNewVersion = 0) : returns DboGraphicBoxInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicBoxInst *
status: DboState &
bNewVersion: int

---

NewGraphicBoxInst(pSource, status) : returns DboGraphicBoxInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicBoxInst *
status: DboState &
NewGraphicLineInst(status, ptStart, ptEnd, location, rotation, nId = 0) : returns DboGraphicLineInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
ptStart: CPoint
ptEnd: CPoint
location: CPoint
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicLineInst(status, ptStart, ptEnd, location, rotation) : returns DboGraphicLineInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
ptStart: CPoint
ptEnd: CPoint
location: CPoint
rotation: enum DboValue::RotationT
NewGraphicLineInst(pSource, status, bNewVersion = 0) : returns DboGraphicLineInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicLineInst *
status: DboState &
bNewVersion: int
NewGraphicLineInst(pSource, status) : returns DboGraphicLineInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicLineInst *
status: DboState &
NewGraphicArcInst(status, rectBound, ptStart, ptEnd, location, rotation,

---

Class : DboPage(DboBaseObject):
nId = 0) : returns DboGraphicArcInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rectBound: CRect &
ptStart: CPoint
ptEnd: CPoint
location: CPoint
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicArcInst(status, rectBound, ptStart, ptEnd, location, rotation) : returns
DboGraphicArcInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rectBound: CRect &
ptStart: CPoint
ptEnd: CPoint
location: CPoint
rotation: enum DboValue::RotationT
NewGraphicArcInst(pSource, status, bNewVersion = 0) : returns DboGraphicArcInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicArcInst *
status: DboState &
bNewVersion: int
NewGraphicArcInst(pSource, status) : returns DboGraphicArcInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicArcInst *
status: DboState &
NewGraphicEllipseInst(status, rectBound, location, rotation, nId = 0) : returns
DboGraphicEllipseInst
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
rectBound: CRect &
location: CPoint
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicEllipseInst(status, rectBound, location, rotation) : returns DboGraphicEllipseInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rectBound: CRect &
location: CPoint
rotation: enum DboValue::RotationT
NewGraphicEllipseInst(pSource, status, bNewVersion = 0) : returns DboGraphicEllipseInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicEllipseInst *
status: DboState &
bNewVersion: int
NewGraphicEllipseInst(pSource, status) : returns DboGraphicEllipseInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicEllipseInst *
status: DboState &
NewGraphicPolygonInst(status, location, rotation, nId = 0) : returns DboGraphicPolygonInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicPolygonInst(status, location, rotation) : returns DboGraphicPolygonInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint

---

rotation: enum DboValue::RotationT
NewGraphicPolygonInst(pSource, status, bNewVersion = 0) : returns DboGraphicPolygonInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicPolygonInst *
status: DboState &
bNewVersion: int
NewGraphicPolygonInst(pSource, status) : returns DboGraphicPolygonInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicPolygonInst *
status: DboState &
NewGraphicPolylineInst(status, location, rotation, nId = 0) : returns DboGraphicPolylineInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicPolylineInst(status, location, rotation) : returns DboGraphicPolylineInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint
rotation: enum DboValue::RotationT
NewGraphicPolylineInst(pSource, status, bNewVersion = 0) : returns DboGraphicPolylineInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicPolylineInst *
status: DboState &
bNewVersion: int
NewGraphicPolylineInst(pSource, status) : returns DboGraphicPolylineInst
Class : DboPage(DboBaseObject):
Parameters:

---

pSource: DboGraphicPolylineInst *
status: DboState &
NewGraphicBezierInst(status, location, rotation, nId = 0) : returns DboGraphicBezierInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicBezierInst(status, location, rotation) : returns DboGraphicBezierInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
location: CPoint
rotation: enum DboValue::RotationT
NewGraphicBezierInst(pSource, status, bNewVersion = 0) : returns DboGraphicBezierInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicBezierInst *
status: DboState &
bNewVersion: int
NewGraphicBezierInst(pSource, status) : returns DboGraphicBezierInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicBezierInst *
status: DboState &
NewGraphicOleEmbedInst(status, rect, location, bmDimension, dwDibSize, lpByte,
Class : DboPage(DboBaseObject):
rotation, nId = 0) : returns DboGraphicOleEmbedInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rect: CRect &
location: CPoint
bmDimension: CSize

---

dwDibSize: unsigned long
lpByte: unsigned char *
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicOleEmbedInst(status, rect, location, bmDimension, dwDibSize, lpByte,
Class : DboPage(DboBaseObject):
rotation) : returns DboGraphicOleEmbedInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rect: CRect &
location: CPoint
bmDimension: CSize
dwDibSize: unsigned long
lpByte: unsigned char *
rotation: enum DboValue::RotationT
NewGraphicOleEmbedInst(pSource, status, bNewVersion = 0) : returns DboGraphicOleEmbedInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicOleEmbedInst *
status: DboState &
bNewVersion: int
NewGraphicOleEmbedInst(pSource, status) : returns DboGraphicOleEmbedInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicOleEmbedInst *
status: DboState &
NewGraphicCommentTextInst(status, rectBound, location, rText, rLF, rotation,
Class : DboPage(DboBaseObject):
nId = 0) : returns DboGraphicCommentTextInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rectBound: CRect &
location: CPoint
rText: CString &

---

rLF: LOGFONT &
rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicCommentTextInst(status, rectBound, location, rText, rLF, rotation) : returns
DboGraphicCommentTextInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rectBound: CRect &
location: CPoint
rText: CString &
rLF: LOGFONT &
rotation: enum DboValue::RotationT
NewGraphicCommentTextInst(pSource, status, bNewVersion = 0) : returns
DboGraphicCommentTextInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicCommentTextInst *
status: DboState &
bNewVersion: int
NewGraphicCommentTextInst(pSource, status) : returns DboGraphicCommentTextInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicCommentTextInst *
status: DboState &
NewGraphicBitMapInst(status, rect, location, bmDimension, dwDibSize, lpDib,
Class : DboPage(DboBaseObject):
rotation, nId = 0) : returns DboGraphicBitMapInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rect: CRect &
location: CPoint
bmDimension: CSize
dwDibSize: unsigned long
lpDib: unsigned char *

---

rotation: enum DboValue::RotationT
nId: unsigned long
NewGraphicBitMapInst(status, rect, location, bmDimension, dwDibSize, lpDib,
Class : DboPage(DboBaseObject):
rotation) : returns DboGraphicBitMapInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
rect: CRect &
location: CPoint
bmDimension: CSize
dwDibSize: unsigned long
lpDib: unsigned char *
rotation: enum DboValue::RotationT
NewGraphicBitMapInst(pSource, status, bNewVersion = 0) : returns DboGraphicBitMapInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicBitMapInst *
status: DboState &
bNewVersion: int
NewGraphicBitMapInst(pSource, status) : returns DboGraphicBitMapInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboGraphicBitMapInst *
status: DboState &
NewERC(status, Name, strError, strDetail, strLocation, symbol,
Class : DboPage(DboBaseObject):
location, rotation = NOROTATION, mirror = 0,
Class : DboPage(DboBaseObject):
bNewVersion = 0) : returns DboERC
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
strError: CString const &
strDetail: CString const &

---

strLocation: CString const &
symbol: DboERCSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
bNewVersion: int
NewERC(status, Name, strError, strDetail, strLocation, symbol,
Class : DboPage(DboBaseObject):
location, rotation = NOROTATION, mirror = 0) : returns DboERC
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
strError: CString const &
strDetail: CString const &
strLocation: CString const &
symbol: DboERCSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
NewERC(status, Name, strError, strDetail, strLocation, symbol,
Class : DboPage(DboBaseObject):
location, rotation = NOROTATION) : returns DboERC
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
strError: CString const &
strDetail: CString const &
strLocation: CString const &
symbol: DboERCSymbol *
location: CPoint
rotation: enum DboValue::RotationT
NewERC(status, Name, strError, strDetail, strLocation, symbol,
Class : DboPage(DboBaseObject):
location) : returns DboERC
Class : DboPage(DboBaseObject):

---

Parameters:
status: DboState &
Name: CString &
strError: CString const &
strDetail: CString const &
strLocation: CString const &
symbol: DboERCSymbol *
location: CPoint
NewERC(pSource, status, bNewVersion = 0) : returns DboERC
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboERC *
status: DboState &
bNewVersion: int
NewERC(pSource, status) : returns DboERC
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboERC *
status: DboState &
NewBookMark(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0, nId = 0) : returns DboBookMark
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboBookMarkSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
nId: unsigned long
NewBookMark(status, Name, symbol, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0) : returns DboBookMark
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
Name: CString &
symbol: DboBookMarkSymbol *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
NewBookMark(status, Name, symbol, location, rotation = NOROTATION) : returns DboBookMark
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboBookMarkSymbol *
location: CPoint
rotation: enum DboValue::RotationT
NewBookMark(status, Name, symbol, location) : returns DboBookMark
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
symbol: DboBookMarkSymbol *
location: CPoint
NewBookMark(pSource, status, bNewVersion = 0) : returns DboBookMark
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboBookMark *
status: DboState &
bNewVersion: int
NewBookMark(pSource, status) : returns DboBookMark
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboBookMark *
status: DboState &
NewCustomItemInstance(pDefiningObj, nType, idInterfaceID, strPluginName,
Class : DboPage(DboBaseObject):
nCookie, nDefColorIdx, pSchOcc) : returns DboCustomItemInstance

---

Class : DboPage(DboBaseObject):
Parameters:
pDefiningObj: DboSymbol *
nType: int
idInterfaceID: IID
strPluginName: CString const &
nCookie: int
nDefColorIdx: UINT
pSchOcc: DboInstOccurrence *
Import(pBlock) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pBlock: DboExportBlock *
DeleteTitleBlock(pTibleBlock, bInstVer = 0, bOccVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pTibleBlock: DboTitleBlock *
bInstVer: int
bOccVer: int
DeleteTitleBlock(pTibleBlock, bInstVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pTibleBlock: DboTitleBlock *
bInstVer: int
DeleteTitleBlock(pTibleBlock) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pTibleBlock: DboTitleBlock *
DeletePartInst(inst, bNewVer = 0, bNewOccVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
inst: DboPartInst *
bNewVer: int
bNewOccVer: int

---

DeletePartInst(inst, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
inst: DboPartInst *
bNewVer: int
DeletePartInst(inst) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
inst: DboPartInst *
DeleteWire(wire, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
wire: DboWire *
bNewVer: int
DeleteWire(wire) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
wire: DboWire *
DeleteBusEntry(busEntry, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
busEntry: DboBusEntry *
bNewVer: int
DeleteBusEntry(busEntry) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
busEntry: DboBusEntry *
DeleteERC(ERC, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
ERC: DboERC *
bNewVer: int
DeleteERC(ERC) : returns DboState

---

Class : DboPage(DboBaseObject):
Parameters:
ERC: DboERC *
DeleteBookMark(bookMark, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bookMark: DboBookMark *
bNewVer: int
DeleteBookMark(bookMark) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bookMark: DboBookMark *
DeleteGlobal(_global, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
global: DboGlobal *
bNewVer: int
DeleteGlobal(_global) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
global: DboGlobal *
DeletePort(port, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
port: DboPort *
bNewVer: int
DeletePort(port) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
port: DboPort *
DeleteOffPageConnector(connector, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:

---

connector: DboOffPageConnector *
bNewVer: int
DeleteOffPageConnector(connector) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
connector: DboOffPageConnector *
DeleteCommentGraphic(instance, bNewVer = 0) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
instance: DboGraphicInstance *
bNewVer: int
DeleteCommentGraphic(instance) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
instance: DboGraphicInstance *
DeleteCustomItemInst(pCustomItemInst) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pCustomItemInst: DboCustomItemInstance *
END class DboPage(DboBaseObject):
DboPage_sGetPageNumber(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetModifyTime(obj, status) : returns time_t
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetCreateTime(obj, status) : returns time_t
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboPage_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetSizeName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetSizeX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetSizeY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetOuterBorderMarginX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetOuterBorderMarginY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetOuterBorderLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetOuterBorderLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboPage_sGetOuterBorderIsVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetInnerBorderMarginX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetInnerBorderMarginY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetInnerBorderLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetInnerBorderLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetInnerBorderIsVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetLabelColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &

---

DboPage_sGetHorizontalLabelCount(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetHorizontalLabelIsChar(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetHorizontalLabelIsVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetHorizontalLabelIsAscending(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetHorizontalSeparatorLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetHorizontalSeparatorLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetVerticalLabelCount(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPage_sGetVerticalLabelIsChar(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &