# Class: DboBox(DboVector):

START class DboBox(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboBox(DboVector):
Parameters:
GetUpperLeft(status) : returns CPoint
Class : DboBox(DboVector):
Parameters:
status: DboState &
GetLowerRight(status) : returns CPoint
Class : DboBox(DboVector):
Parameters:
status: DboState &
GetLineStyle(status) : returns LineStyleT
Class : DboBox(DboVector):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboBox(DboVector):
Parameters:
status: DboState &
GetFillStyle(status) : returns FillStyleT
Class : DboBox(DboVector):
Parameters:
status: DboState &
GetHatchStyle(status) : returns HatchStyleT
Class : DboBox(DboVector):
Parameters:
status: DboState &
sGetLeft(obj, status) : returns int
Class : DboBox(DboVector):
Parameters:
obj: DboBaseObject *

---

status: DboState &
sGetTop(obj, status) : returns int
Class : DboBox(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetRight(obj, status) : returns int
Class : DboBox(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBottom(obj, status) : returns int
Class : DboBox(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboBox(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboBox(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFillStyle(obj, status) : returns FillStyleT
Class : DboBox(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHatchStyle(obj, status) : returns HatchStyleT
Class : DboBox(DboVector):

---

Parameters:
obj: DboBaseObject *
status: DboState &
SetUpperLeft(point) : returns DboState
Class : DboBox(DboVector):
Parameters:
point: CPoint
SetLowerRight(point) : returns DboState
Class : DboBox(DboVector):
Parameters:
point: CPoint
SetLineStyle(style) : returns DboState
Class : DboBox(DboVector):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboBox(DboVector):
Parameters:
width: enum DboValue::LineWidthT
SetFillStyle(style) : returns DboState
Class : DboBox(DboVector):
Parameters:
style: enum DboValue::FillStyleT
SetHatchStyle(style) : returns DboState
Class : DboBox(DboVector):
Parameters:
style: enum DboValue::HatchStyleT
Move(ptOffset) : returns DboState
Class : DboBox(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboBox(DboVector):