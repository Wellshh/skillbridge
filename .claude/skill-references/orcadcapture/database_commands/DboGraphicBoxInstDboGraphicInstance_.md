# Class: DboGraphicBoxInst(DboGraphicInstance):

status: DboState &
DboGraphicInstance_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstance_sGetRotation(obj, status) : returns RotationT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstance_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstance_sGetMirror(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboGraphicBoxInst(x) : returns DboGraphicBoxInst
Parameters:
x: DboGraphicInstance *
START class DboGraphicBoxInst(DboGraphicInstance):
GetDboBox() : returns DboBox
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
sGetLeft(obj, status) : returns int
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetTop(obj, status) : returns int
Class : DboGraphicBoxInst(DboGraphicInstance):

---

Parameters:
obj: DboBaseObject *
status: DboState &
sGetRight(obj, status) : returns int
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBottom(obj, status) : returns int
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFillStyle(obj, status) : returns FillStyleT
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHatchStyle(obj, status) : returns HatchStyleT
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
obj: DboBaseObject *
status: DboState &

---

StatefulCreate() : returns DboBaseObject
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
Move(offset) : returns DboState
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
offset: CPoint
SetUpperLeft(point) : returns DboState
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
point: CPoint
SetLowerRight(point) : returns DboState
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
point: CPoint
SetLineStyle(style) : returns DboState
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
width: enum DboValue::LineWidthT
SetFillStyle(style) : returns DboState
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
style: enum DboValue::FillStyleT
SetHatchStyle(style) : returns DboState
Class : DboGraphicBoxInst(DboGraphicInstance):
Parameters:
style: enum DboValue::HatchStyleT
END class DboGraphicBoxInst(DboGraphicInstance):