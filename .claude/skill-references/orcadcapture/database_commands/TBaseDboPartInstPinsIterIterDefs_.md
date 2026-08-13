# Class: TBaseDboPartInstPinsIter(IterDefs):

pProp: DboDisplayProp *
DboPartInst_PositionAllDisplayProp(pPage, pInst) : returns int
Parameters:
pPage: DboPage *
pInst: DboPartInst *
START class TBaseDboPartInstPinsIter(IterDefs):
GetType() : returns int
Class : TBaseDboPartInstPinsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboPartInstPinsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboPartInstPinsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboPartInstPinsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboPartInstPinsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboPartInstPinsIter(IterDefs):
START class DboPartInstPinsIter(TBaseDboSchematicNetPortInstsIter):
Next(status) : returns DboBaseObject
Class : DboPartInstPinsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:

---

status: DboState &
GetKey(pObject) : returns std::string
Class : DboPartInstPinsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
pObject: DboPortInst *&
NextPin(status) : returns DboPortInst
Class : DboPartInstPinsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
status: DboState &
END class DboPartInstPinsIter(TBaseDboSchematicNetPortInstsIter):
DboPartInstToDboPlacedInst(x) : returns DboPlacedInst
Parameters:
x: DboPartInst *
START class DboPlacedInst(DboPartInst):
GetReferenceDesignator(RefDes) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
RefDes: CString &
GetDeviceDesignator(designator) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
designator: CString &
GetPart(status) : returns DboLibPart
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
GetPackage(status) : returns DboPackage
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &

---

GetDevice(status) : returns DboDevice
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
GetSourcePartName(name) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
name: CString &
GetSourcePackageName(name) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
name: CString &
GetSourceDeviceDesignator(designator) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
designator: CString &
GetSourceLibName(libName) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
libName: CString &
GetPartValue(value) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
value: CString &
GetPCBLib(lib) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
lib: CString &
GetPCBFootprint(footprint) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
footprint: CString &

---

GetSourcePart(status) : returns DboLibPart
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
GetSourcePackage(status) : returns DboPackage
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
GetSourceDevice(status) : returns DboDevice
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
GetSourceDevicePosition(status) : returns short
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
sGetSourcePartName(obj, status) : returns CString
Class : DboPlacedInst(DboPartInst):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSourcePackageName(obj, status) : returns CString
Class : DboPlacedInst(DboPartInst):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetReferenceDesignator(pObj, status) : returns CString
Class : DboPlacedInst(DboPartInst):
Parameters:
pObj: DboBaseObject *
status: DboState &
sGetSourceDeviceDesignator(obj, status) : returns CString
Class : DboPlacedInst(DboPartInst):

---

Parameters:
obj: DboBaseObject *
status: DboState &
sGetSourceLibName(obj, status) : returns CString
Class : DboPlacedInst(DboPartInst):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPCBLib(obj, status) : returns CString
Class : DboPlacedInst(DboPartInst):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPCBFootprint(obj, status) : returns CString
Class : DboPlacedInst(DboPartInst):
Parameters:
obj: DboBaseObject *
status: DboState &
IsOptimizerTemplate(status) : returns int
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
GetGraphicName(status) : returns CString
Class : DboPlacedInst(DboPartInst):
Parameters:
status: DboState &
GetEffectivePropValueChoices(name, choices) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
name: CString const &
choices: CStringList &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboPlacedInst(DboPartInst):

---

Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
StatefulCreate() : returns DboBaseObject
Class : DboPlacedInst(DboPartInst):
Parameters:
SetDeviceDesignator(designator) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
designator: CString &
SetPCBLib(libname) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
libname: CString &
SetPCBFootprint(name) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
name: CString &
Update() : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
SetGraphic(graphic) : returns DboState
Class : DboPlacedInst(DboPartInst):
Parameters:
graphic: CString &
NewCachedPinShapeSymbol(pOwningLib, pPin) : returns DboPinShapeSymbol
Class : DboPlacedInst(DboPartInst):
Parameters:
pOwningLib: DboLib *
pPin: DboPortInst *

---

UpdateOpProp()
Class : DboPlacedInst(DboPartInst):
Parameters:
CheckAndResetDisplayProperty(pOldInst)
Class : DboPlacedInst(DboPartInst):
Parameters:
pOldInst: DboPlacedInst *
END class DboPlacedInst(DboPartInst):
DboPlacedInst_sGetSourcePartName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPlacedInst_sGetSourcePackageName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPlacedInst_sGetReferenceDesignator(pObj, status) : returns CString
Parameters:
pObj: DboBaseObject *
status: DboState &
DboPlacedInst_sGetSourceDeviceDesignator(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPlacedInst_sGetSourceLibName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPlacedInst_sGetPCBLib(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &