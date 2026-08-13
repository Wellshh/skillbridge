# Class: DboGraphicObject(DboLibObject):

START class DboGraphicObject(DboLibObject):
GetBoundingBox() : returns CRect
Class : DboGraphicObject(DboLibObject):
Parameters:
PinsAllowed(status) : returns int
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
GetColor(status) : returns ColorT
Class : DboGraphicObject(DboLibObject):

---

Parameters:
status: DboState &
GetGraphicsArray() : returns DboPtrArray
Class : DboGraphicObject(DboLibObject):
Parameters:
sGetName(obj, status) : returns CString
Class : DboGraphicObject(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
NewVectorsIter(status, mode) : returns DboGraphicObjectVectorsIter
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
SetColor(color) : returns DboState
Class : DboGraphicObject(DboLibObject):
Parameters:
color: enum DboValue::ColorT
SetBoundingBox(box) : returns DboState
Class : DboGraphicObject(DboLibObject):
Parameters:
box: CRect
DeleteVector(pVector) : returns DboState
Class : DboGraphicObject(DboLibObject):
Parameters:
pVector: DboVector *
Clear() : returns DboState
Class : DboGraphicObject(DboLibObject):
Parameters:
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE,
Class : DboGraphicObject(DboLibObject):

---

lineWidth = THIN_WIDTH, fillStyle = HOLLOW_FILL,
Class : DboGraphicObject(DboLibObject):
hatchStyle = HORIZONTAL_HATCH) : returns DboBox
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
hatchStyle: enum DboValue::HatchStyleT
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE,
Class : DboGraphicObject(DboLibObject):
lineWidth = THIN_WIDTH, fillStyle = HOLLOW_FILL) : returns DboBox
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE,
Class : DboGraphicObject(DboLibObject):
lineWidth = THIN_WIDTH) : returns DboBox
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewBox(status, upperLeft, lowerRight, lineStyle = SOLID_LINE) : returns DboBox
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &

---

upperLeft: CPoint
lowerRight: CPoint
lineStyle: enum DboValue::LineStyleT
NewBox(status, upperLeft, lowerRight) : returns DboBox
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
upperLeft: CPoint
lowerRight: CPoint
NewLine(status, start, end, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns DboLine
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewLine(status, start, end, lineStyle = SOLID_LINE) : returns DboLine
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
lineStyle: enum DboValue::LineStyleT
NewLine(status, start, end) : returns DboLine
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
start: CPoint
end: CPoint
NewArc(status, boundingBox, start, end, lineStyle = SOLID_LINE,
Class : DboGraphicObject(DboLibObject):
lineWidth = THIN_WIDTH) : returns DboArc
Class : DboGraphicObject(DboLibObject):
Parameters:

---

status: DboState &
boundingBox: CRect
start: CPoint
end: CPoint
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewArc(status, boundingBox, start, end, lineStyle = SOLID_LINE) : returns DboArc
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
boundingBox: CRect
start: CPoint
end: CPoint
lineStyle: enum DboValue::LineStyleT
NewArc(status, boundingBox, start, end) : returns DboArc
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
boundingBox: CRect
start: CPoint
end: CPoint
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboGraphicObject(DboLibObject):
fillStyle = HOLLOW_FILL, hatchStyle = HORIZONTAL_HATCH) : returns DboEllipse
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
hatchStyle: enum DboValue::HatchStyleT
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboGraphicObject(DboLibObject):
fillStyle = HOLLOW_FILL) : returns DboEllipse
Class : DboGraphicObject(DboLibObject):

---

Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns
DboEllipse
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewEllipse(status, boundingBox, lineStyle = SOLID_LINE) : returns DboEllipse
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
boundingBox: CRect
lineStyle: enum DboValue::LineStyleT
NewEllipse(status, boundingBox) : returns DboEllipse
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
boundingBox: CRect
NewPolygon(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboGraphicObject(DboLibObject):
fillStyle = HOLLOW_FILL, hatchStyle = HORIZONTAL_HATCH) : returns DboPolygon
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
hatchStyle: enum DboValue::HatchStyleT

---

NewPolygon(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH,
Class : DboGraphicObject(DboLibObject):
fillStyle = HOLLOW_FILL) : returns DboPolygon
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
fillStyle: enum DboValue::FillStyleT
NewPolygon(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns DboPolygon
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewPolygon(status, lineStyle = SOLID_LINE) : returns DboPolygon
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
NewPolygon(status) : returns DboPolygon
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
NewPolyline(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns DboPolyline
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewPolyline(status, lineStyle = SOLID_LINE) : returns DboPolyline
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT

---

NewPolyline(status) : returns DboPolyline
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
NewCommentText(status, text, rectBound, location, font) : returns DboCommentText
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
text: CString &
rectBound: CRect &
location: CPoint
font: LOGFONT &
NewFill(status, start, fillStyle = SOLID_FILL, hatchStyle = HORIZONTAL_HATCH) : returns DboFill
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
start: CPoint
fillStyle: enum DboValue::FillStyleT
hatchStyle: enum DboValue::HatchStyleT
NewFill(status, start, fillStyle = SOLID_FILL) : returns DboFill
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
start: CPoint
fillStyle: enum DboValue::FillStyleT
NewFill(status, start) : returns DboFill
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
start: CPoint
NewBezier(status, lineStyle = SOLID_LINE, lineWidth = THIN_WIDTH) : returns DboBezier
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &

---

lineStyle: enum DboValue::LineStyleT
lineWidth: enum DboValue::LineWidthT
NewBezier(status, lineStyle = SOLID_LINE) : returns DboBezier
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
lineStyle: enum DboValue::LineStyleT
NewBezier(status) : returns DboBezier
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
NewBitMap(status, BoundingBox, location, bmDimension, dwSize,
Class : DboGraphicObject(DboLibObject):
lpDib) : returns DboBitMap
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
BoundingBox: CRect
location: CPoint
bmDimension: CSize
dwSize: unsigned long
lpDib: unsigned char const *
NewOleEmbed(status, BoundingBox, location, bmDimension, dwSize,
Class : DboGraphicObject(DboLibObject):
lpByte) : returns DboOleEmbed
Class : DboGraphicObject(DboLibObject):
Parameters:
status: DboState &
BoundingBox: CRect
location: CPoint
bmDimension: CSize
dwSize: unsigned long
lpByte: unsigned char *
NewSymbolVector(status, location) : returns DboSymbolVector
Class : DboGraphicObject(DboLibObject):

---

Parameters:
status: DboState &
location: CPoint
sGetColor(obj, status) : returns ColorT
Class : DboGraphicObject(DboLibObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sSetColor(obj, color) : returns DboState
Class : DboGraphicObject(DboLibObject):
Parameters:
obj: DboBaseObject *
color: enum DboValue::ColorT
END class DboGraphicObject(DboLibObject):
DboGraphicObject_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicObject_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicObject_sSetColor(obj, color) : returns DboState
Parameters:
obj: DboBaseObject *
color: enum DboValue::ColorT
START class DboGraphicObjectVectorsIter
NextVector(status) : returns DboVector
Class : DboGraphicObjectVectorsIter
Parameters:
status: DboState &