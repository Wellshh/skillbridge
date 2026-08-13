# Class: DboPrimitiveAndVisiblePowerPins

Parameters:
obj: DboBaseObject *
name: CString &
DboAlias_sSetLocationX(obj, x) : returns DboState
Parameters:
obj: DboBaseObject *
x: int
DboAlias_sSetLocationY(obj, y) : returns DboState
Parameters:
obj: DboBaseObject *
y: int
DboAlias_sSetRotation(obj, rotation) : returns DboState
Parameters:
obj: DboBaseObject *
rotation: enum DboValue::RotationT
DboAlias_sSetFont(obj, font) : returns DboState
Parameters:
obj: DboBaseObject *
font: LOGFONT &
DboAlias_sSetColor(obj, color) : returns DboState
Parameters:
obj: DboBaseObject *
color: enum DboValue::ColorT
START class DboPrimitiveAndVisiblePowerPins
GetVisiblePowerPins() : returns int
Class : DboPrimitiveAndVisiblePowerPins
Parameters:
GetPrimitive() : returns PrimitiveTypeT
Class : DboPrimitiveAndVisiblePowerPins
Parameters:
GetViewType() : returns ViewTypeT

---

Class : DboPrimitiveAndVisiblePowerPins
Parameters:
SetPrimitive(nPrimitive)
Class : DboPrimitiveAndVisiblePowerPins
Parameters:
nPrimitive: enum DboValue::PrimitiveTypeT
SetVisiblePowerPins(bVisiblePowerPins)
Class : DboPrimitiveAndVisiblePowerPins
Parameters:
bVisiblePowerPins: int
SetViewType(nViewType)
Class : DboPrimitiveAndVisiblePowerPins
Parameters:
nViewType: enum DboValue::ViewTypeT
END class DboPrimitiveAndVisiblePowerPins
DboGraphicInstanceToDboPartInst(x) : returns DboPartInst
Parameters:
x: DboGraphicInstance *
DboInstOccMapperToDboPartInst(x) : returns DboPartInst
Parameters:
x: DboInstOccMapper *
START class DboPartInst(DboGraphicInstance,DboInstOccMapper):
GetReference(Ref) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
Ref: CString &
GetReferenceDesignator(RefDes) : returns DboState
Class : DboPartInst(DboGraphicInstance,DboInstOccMapper):
Parameters:
RefDes: CString &