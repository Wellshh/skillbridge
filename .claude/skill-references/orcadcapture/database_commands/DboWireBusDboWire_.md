# Class: DboWireBus(DboWire):

START class DboWireBus(DboWire):
GetObjectType() : returns ObjectTypeT
Class : DboWireBus(DboWire):
Parameters:
IsBundleObject() : returns bool
Class : DboWireBus(DboWire):
Parameters:
NormalizeBundleWire() : returns DboState
Class : DboWireBus(DboWire):
Parameters:
SetName(name) : returns DboState
Class : DboWireBus(DboWire):
Parameters:
name: CString &
NewAlias(status, alias, location, font, rotation, color, ID = None) : returns DboAlias

---

Class : DboWireBus(DboWire):
Parameters:
status: DboState &
alias: CString &
location: CPoint
font: LOGFONT &
rotation: enum DboValue::RotationT
color: enum DboValue::ColorT
ID: unsigned long
NewAlias(status, alias, location, font, rotation, color) : returns DboAlias
Class : DboWireBus(DboWire):
Parameters:
status: DboState &
alias: CString &
location: CPoint
font: LOGFONT &
rotation: enum DboValue::RotationT
color: enum DboValue::ColorT
END class DboWireBus(DboWire):
DboDisplayPropsIterToDboWireDisplayPropsIter(x) : returns DboWireDisplayPropsIter
Parameters:
x: DboDisplayPropsIter *
START class DboWireDisplayPropsIter(DboDisplayPropsIter):
Next(status) : returns DboBaseObject
Class : DboWireDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
NextProp(status) : returns DboDisplayProp
Class : DboWireDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboWireDisplayPropsIter(DboDisplayPropsIter):