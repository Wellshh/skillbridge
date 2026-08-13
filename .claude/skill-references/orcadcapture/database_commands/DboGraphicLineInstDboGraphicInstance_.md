# Class: DboGraphicLineInst(DboGraphicInstance):

DboGraphicInstanceToDboGraphicLineInst(x) : returns DboGraphicLineInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicLineInst(DboGraphicInstance):
sGetStartX(obj, status) : returns int
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartY(obj, status) : returns int
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndX(obj, status) : returns int
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndY(obj, status) : returns int
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:

---

obj: DboBaseObject *
status: DboState &
GetDboLine() : returns DboLine
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
StatefulCreate() : returns DboBaseObject
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
offset: CPoint
SetStart(point) : returns DboState
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
point: CPoint
SetEnd(point) : returns DboState
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
point: CPoint
SetLineStyle(style) : returns DboState
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboGraphicLineInst(DboGraphicInstance):
Parameters:
width: enum DboValue::LineWidthT
END class DboGraphicLineInst(DboGraphicInstance):
DboGraphicLineInst_sGetStartX(obj, status) : returns int
Parameters: