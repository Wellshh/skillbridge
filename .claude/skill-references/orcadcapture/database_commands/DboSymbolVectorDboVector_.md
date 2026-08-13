# Class: DboSymbolVector(DboVector):

obj: DboBaseObject *
status: DboState &
DboOleEmbed_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboOleEmbed_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboVectorToDboSymbolVector(x) : returns DboSymbolVector
Parameters:
x: DboVector *
START class DboSymbolVector(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboSymbolVector(DboVector):
Parameters:
GetLocation(status) : returns CPoint
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
GetName(name) : returns DboState
Class : DboSymbolVector(DboVector):
Parameters:
name: CString &
sGetLocationX(obj, status) : returns int
Class : DboSymbolVector(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int

---

Class : DboSymbolVector(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
NewVectorsIter(status, mode = ALL) : returns DboSymbolVectorVectorsIter
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewVectorsIter(status) : returns DboSymbolVectorVectorsIter
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
SetLocation(point) : returns DboState
Class : DboSymbolVector(DboVector):
Parameters:
point: CPoint
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE,
Class : DboSymbolVector(DboVector):
lineWidth = THIN_WIDTH, fillStyle = HOLLOW_FILL,
Class : DboSymbolVector(DboVector):
hatchStyle = HORIZONTAL_HATCH) : returns DboBox
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
hatchStyle: enum DboValue::HatchStyleT
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE,
Class : DboSymbolVector(DboVector):
lineWidth = THIN_WIDTH, fillStyle = HOLLOW_FILL) : returns DboBox
Class : DboSymbolVector(DboVector):

---

Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE,
Class : DboSymbolVector(DboVector):
lineWidth = THIN_WIDTH) : returns DboBox
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE) : returns DboBox
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
NewBox(status, upperLeft, lowerRight) : returns DboBox
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
NewLine(status, start, end, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns DboLine
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
start: CPoint
end: CPoint

---

lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewLine(status, start, end, lineStyle = SOLID_LINE) : returns DboLine
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
start: CPoint
end: CPoint
lineStyle: enum DboValue::LineStyleT
NewLine(status, start, end) : returns DboLine
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
start: CPoint
end: CPoint
NewArc(status, boundingBox, start, end, lineStyle = SOLID_LINE,
Class : DboSymbolVector(DboVector):
lineWidth = THIN_WIDTH) : returns DboArc
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
start: CPoint
end: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewArc(status, boundingBox, start, end, lineStyle = SOLID_LINE) : returns DboArc
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
start: CPoint
end: CPoint
lineStyle: enum DboValue::LineStyleT
NewArc(status, boundingBox, start, end) : returns DboArc

---

Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
start: CPoint
end: CPoint
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboSymbolVector(DboVector):
fillStyle = HOLLOW_FILL, hatchStyle = HORIZONTAL_HATCH) : returns DboEllipse
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
hatchStyle: enum DboValue::HatchStyleT
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboSymbolVector(DboVector):
fillStyle = HOLLOW_FILL) : returns DboEllipse
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns
DboEllipse
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE) : returns DboEllipse

---

Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
NewEllipse(status, boundingBox) : returns DboEllipse
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
boundingBox: CRect
NewPolygon(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboSymbolVector(DboVector):
fillStyle = HOLLOW_FILL, hatchStyle = HORIZONTAL_HATCH) : returns DboPolygon
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
hatchStyle: enum DboValue::HatchStyleT
NewPolygon(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboSymbolVector(DboVector):
fillStyle = HOLLOW_FILL) : returns DboPolygon
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
NewPolygon(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns DboPolygon
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT

---

NewPolygon(status, lineStyle = SOLID_LINE) : returns DboPolygon
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
NewPolygon(status) : returns DboPolygon
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
NewPolyline(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns DboPolyline
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewPolyline(status, lineStyle = SOLID_LINE) : returns DboPolyline
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
NewPolyline(status) : returns DboPolyline
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
NewCommentText(status, text, rectBound, location, font) : returns DboCommentText
Class : DboSymbolVector(DboVector):
Parameters:
status: DboState &
text: CString &
rectBound: CRect &
location: CPoint
font: LOGFONT &
END class DboSymbolVector(DboVector):