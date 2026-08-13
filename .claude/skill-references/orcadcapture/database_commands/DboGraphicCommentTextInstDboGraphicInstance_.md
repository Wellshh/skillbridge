# Class: DboGraphicCommentTextInst(DboGraphicInstance):

DboGraphicInstanceToDboGraphicCommentTextInst(x) : returns DboGraphicCommentTextInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicCommentTextInst(DboGraphicInstance):
GetDboCommentText() : returns DboCommentText
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxRight(obj, status) : returns int
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetText(obj, status) : returns CString
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetLocationX(obj, status) : returns int
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFont(obj, status) : returns LOGFONT
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
StatefulCreate() : returns DboBaseObject
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
offset: CPoint
SetText(rText) : returns DboState
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
rText: CString &
SetLocation(pt) : returns DboState
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:
pt: CPoint
SetFont(rLF) : returns DboState
Class : DboGraphicCommentTextInst(DboGraphicInstance):
Parameters:

---

rLF: LOGFONT &
END class DboGraphicCommentTextInst(DboGraphicInstance):
DboGraphicCommentTextInst_sGetBoundingBoxLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicCommentTextInst_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicCommentTextInst_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicCommentTextInst_sGetBoundingBoxBottom(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicCommentTextInst_sGetText(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicCommentTextInst_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicCommentTextInst_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicCommentTextInst_sGetFont(obj, status) : returns LOGFONT