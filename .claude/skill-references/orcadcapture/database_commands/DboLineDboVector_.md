# Class: DboLine(DboVector):

status: DboState &
DboFill_sGetFillStyle(obj, status) : returns FillStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboFill_sGetHatchStyle(obj, status) : returns HatchStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboVectorToDboLine(x) : returns DboLine
Parameters:
x: DboVector *
START class DboLine(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboLine(DboVector):
Parameters:
GetStart(status) : returns CPoint
Class : DboLine(DboVector):
Parameters:
status: DboState &
GetEnd(status) : returns CPoint
Class : DboLine(DboVector):
Parameters:
status: DboState &
GetLineStyle(status) : returns LineStyleT
Class : DboLine(DboVector):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboLine(DboVector):
Parameters:

---

status: DboState &
sGetStartX(obj, status) : returns int
Class : DboLine(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartY(obj, status) : returns int
Class : DboLine(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndX(obj, status) : returns int
Class : DboLine(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetEndY(obj, status) : returns int
Class : DboLine(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboLine(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboLine(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
SetStart(point) : returns DboState
Class : DboLine(DboVector):

---

Parameters:
point: CPoint
SetEnd(point) : returns DboState
Class : DboLine(DboVector):
Parameters:
point: CPoint
SetLineStyle(style) : returns DboState
Class : DboLine(DboVector):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboLine(DboVector):
Parameters:
width: enum DboValue::LineWidthT
Move(ptOffset) : returns DboState
Class : DboLine(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboLine(DboVector):
DboLine_sGetStartX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLine_sGetStartY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLine_sGetEndX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &