# Class: DboEllipse(DboVector):

DboArc_sGetStartX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetStartY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetEndX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetEndY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
DboArc_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboVectorToDboEllipse(x) : returns DboEllipse
Parameters:
x: DboVector *
START class DboEllipse(DboVector):
GetObjectType() : returns ObjectTypeT
Class : DboEllipse(DboVector):
Parameters:

---

GetBoundingBox() : returns CRect
Class : DboEllipse(DboVector):
Parameters:
GetLineStyle(status) : returns LineStyleT
Class : DboEllipse(DboVector):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboEllipse(DboVector):
Parameters:
status: DboState &
GetFillStyle(status) : returns FillStyleT
Class : DboEllipse(DboVector):
Parameters:
status: DboState &
GetHatchStyle(status) : returns HatchStyleT
Class : DboEllipse(DboVector):
Parameters:
status: DboState &
sGetBoundingBoxLeft(obj, status) : returns int
Class : DboEllipse(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxRight(obj, status) : returns int
Class : DboEllipse(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetBoundingBoxTop(obj, status) : returns int
Class : DboEllipse(DboVector):
Parameters:

---

obj: DboBaseObject *
status: DboState &
sGetBoundingBoxBottom(obj, status) : returns int
Class : DboEllipse(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineStyle(obj, status) : returns LineStyleT
Class : DboEllipse(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLineWidth(obj, status) : returns LineWidthT
Class : DboEllipse(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFillStyle(obj, status) : returns FillStyleT
Class : DboEllipse(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHatchStyle(obj, status) : returns HatchStyleT
Class : DboEllipse(DboVector):
Parameters:
obj: DboBaseObject *
status: DboState &
SetBoundingBox(box) : returns DboState
Class : DboEllipse(DboVector):
Parameters:
box: CRect
SetLineStyle(style) : returns DboState
Class : DboEllipse(DboVector):

---

Parameters:
style: enum DboValue::LineStyleT
SetLineWidth(width) : returns DboState
Class : DboEllipse(DboVector):
Parameters:
width: enum DboValue::LineWidthT
SetFillStyle(style) : returns DboState
Class : DboEllipse(DboVector):
Parameters:
style: enum DboValue::FillStyleT
SetHatchStyle(style) : returns DboState
Class : DboEllipse(DboVector):
Parameters:
style: enum DboValue::HatchStyleT
Move(ptOffset) : returns DboState
Class : DboEllipse(DboVector):
Parameters:
ptOffset: CPoint const &
END class DboEllipse(DboVector):
DboEllipse_sGetBoundingBoxLeft(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboEllipse_sGetBoundingBoxRight(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboEllipse_sGetBoundingBoxTop(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &