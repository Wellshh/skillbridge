# Class: DboFill(DboVector):

DboVectorToDboFill(x) : returns DboFill
Parameters:
x: DboVector *
START class DboFill(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboFill(DboVector):
Parameters:
GetStart(status) : returns CPoint
Class : DboFill(DboVector):
Parameters:
status: DboState &
GetFillStyle(status) : returns FillStyleT
Class : DboFill(DboVector):
Parameters:
status: DboState &
GetHatchStyle(status) : returns HatchStyleT
Class : DboFill(DboVector):
Parameters:
status: DboState &
sGetStartX(obj, status) : returns int
Class : DboFill(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetStartY(obj, status) : returns int
Class : DboFill(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFillStyle(obj, status) : returns FillStyleT
Class : DboFill(DboVector):

---

Parameters:
obj: DboBaseObject *
status: DboState &
sGetHatchStyle(obj, status) : returns HatchStyleT
Class : DboFill(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
SetStart(point) : returns DboState
Class : DboFill(DboVector):
Parameters:
point: CPoint
SetFillStyle(style) : returns DboState
Class : DboFill(DboVector):
Parameters:
style: enum DboValue::FillStyleT
SetHatchStyle(style) : returns DboState
Class : DboFill(DboVector):
Parameters:
style: enum DboValue::HatchStyleT
Move(ptOffset) : returns DboState
Class : DboFill(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboFill(DboVector):
DboFill_sGetStartX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboFill_sGetStartY(obj, status) : returns int
Parameters:
obj: DboBaseObject *