# Class: DboBezierPointsIter

DboBezier_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboBezier_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
START class DboBezierPointsIter
Next(returnPt) : returns DboState
Class : DboBezierPointsIter
Parameters:
returnPt: CPoint &
END class DboBezierPointsIter
DboVectorToDboCommentText(x) : returns DboCommentText
Parameters:
x: DboVector *
START class DboCommentText(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboCommentText(DboVector):
Parameters:
GetBoundingBox() : returns CRect
Class : DboCommentText(DboVector):
Parameters:
GetText(txt) : returns DboState
Class : DboCommentText(DboVector):
Parameters:
txt: CString &
GetLocation(status) : returns CPoint
Class : DboCommentText(DboVector):

---

Parameters:
status: DboState &
GetFont(status) : returns LOGFONT
Class : DboCommentText(DboVector):
Parameters:
status: DboState &
IsFontDefault(status) : returns int
Class : DboCommentText(DboVector):
Parameters:
status: DboState &
GetFontId() : returns short
Class : DboCommentText(DboVector):
Parameters:
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxRight(obj, status) : returns int
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetText(obj, status) : returns CString
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationX(obj, status) : returns int
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFont(obj, status) : returns LOGFONT
Class : DboCommentText(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
SetBoundingBox(box) : returns DboState
Class : DboCommentText(DboVector):
Parameters:
box: CRect const &
SetText(text) : returns DboState
Class : DboCommentText(DboVector):
Parameters:
text: CString &
SetLocation(point) : returns DboState
Class : DboCommentText(DboVector):
Parameters:
point: CPoint

---

SetFont(font) : returns DboState
Class : DboCommentText(DboVector):
Parameters:
font: LOGFONT &
Move(ptOffset) : returns DboState
Class : DboCommentText(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboCommentText(DboVector):
DboCommentText_sGetBoundingBoxLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboCommentText_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboCommentText_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboCommentText_sGetBoundingBoxBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboCommentText_sGetText(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboCommentText_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *