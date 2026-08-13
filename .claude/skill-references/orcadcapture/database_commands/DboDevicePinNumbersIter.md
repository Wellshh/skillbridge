# Class: DboDevicePinNumbersIter

DboDevice_sGetDesignator(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboDevice_sGetSize(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
START class DboDevicePinNumbersIter
NextNumber(pinNumber) : returns DboState
Class : DboDevicePinNumbersIter
Parameters:
pinNumber: CString &
END class DboDevicePinNumbersIter
START class DboArcData
END class DboArcData
START class DboBoxData
END class DboBoxData
START class DboEllipseData
END class DboEllipseData
START class DboLineData
END class DboLineData
START class DboPolygonData
END class DboPolygonData
START class DboPolylineData

---

END class DboPolylineData
START class DboPartTextData
END class DboPartTextData
START class DboBitMapData
END class DboBitMapData
START class DboPinData
END class DboPinData
START class DispPropData
END class DispPropData
START class DboInstData
END class DboInstData
START class DboWireData
END class DboWireData
START class DboBusEntryData
END class DboBusEntryData
START class DboAliasData
END class DboAliasData
DboBaseObjectToDboNet(x) : returns DboNet
Parameters:
x: DboBaseObject *
START class DboNet(DboBaseObject):

---

GetObjectType() : returns ObjectTypeT
Class : DboNet(DboBaseObject):
Parameters:
GetUserProp(name, status) : returns DboUserProp
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
status: DboState &
GetId(status) : returns unsigned long
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
GetNetName(name) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString &
GetOwner() : returns DboPage
Class : DboNet(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboNet(DboBaseObject):
Parameters:
GetName(name) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString &
GetObjectCount() : returns int
Class : DboNet(DboBaseObject):
Parameters:
IsBusMember(pBus, status) : returns int
Class : DboNet(DboBaseObject):

---

Parameters:
pBus: DboNetBus *&
status: DboState &
IsBundle() : returns int
Class : DboNet(DboBaseObject):
Parameters:
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
nNameID: UINT
value: CString &
GetEffectivePropStringValue(name, value) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
value: CString &
sGetName(obj, status) : returns CString
Class : DboNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetNetName(obj, status) : returns CString
Class : DboNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetId(obj, status) : returns int
Class : DboNet(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetObjectOccurrence(pParentSchematicOcc) : returns DboOccurrence
Class : DboNet(DboBaseObject):

---

Parameters:
pParentSchematicOcc: DboInstOccurrence *
GetEffectivePropValueExists(name, bExists) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
bExists: int &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
AssertValid() : returns int
Class : DboNet(DboBaseObject):
Parameters:
ValidateName(Name) : returns int
Class : DboNet(DboBaseObject):
Parameters:
Name: CString &
IsEmpty() : returns int
Class : DboNet(DboBaseObject):
Parameters:
EffectivePropsMatch(strFindWhat, bMatchCase, PatternMatcher = DboPatternMatch) : returns int
Class : DboNet(DboBaseObject):
Parameters:
strFindWhat: CString const &
bMatchCase: int
PatternMatcher: TPatternMatch
EffectivePropsMatch(strFindWhat, bMatchCase) : returns int
Class : DboNet(DboBaseObject):
Parameters:

---

strFindWhat: CString const &
bMatchCase: int
GetEffectiveColorValue(dbColor, dbLineStyle, dbLineWidth, pParentSchematicOcc) : returns
DboState
Class : DboNet(DboBaseObject):
Parameters:
dbColor: DboValue::ColorT &
dbLineStyle: DboValue::LineStyleT &
dbLineWidth: DboValue::LineWidthT &
pParentSchematicOcc: DboInstOccurrence *
GetSchematicNet() : returns DboSchematicNet
Class : DboNet(DboBaseObject):
Parameters:
GetColor(status) : returns ColorT
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
GetLineStyle(status) : returns LineStyleT
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
HasBundleConnection() : returns bool
Class : DboNet(DboBaseObject):
Parameters:
HasNonNGOverrider() : returns bool
Class : DboNet(DboBaseObject):
Parameters:
SetNonNGOverrider(flag)

---

Class : DboNet(DboBaseObject):
Parameters:
flag: bool
IsBundleObject() : returns bool
Class : DboNet(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboNet(DboBaseObject):
Parameters:
NewWiresIter(status, mode = TOP) : returns DboNetWiresIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewWiresIter(status) : returns DboNetWiresIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
NewPortInstsIter(status, mode = TOP) : returns DboNetPortInstsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPortInstsIter(status) : returns DboNetPortInstsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
NewPortsIter(status, mode = TOP) : returns DboNetPortsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT

---

NewPortsIter(status) : returns DboNetPortsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
NewGlobalsIter(status) : returns DboNetGlobalsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
NewOffPageConnectorsIter(status, mode = TOP) : returns DboNetOffPageConnectorsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewOffPageConnectorsIter(status) : returns DboNetOffPageConnectorsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
NewNetAliasesIter(status) : returns DboNetAliasesIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
NewBusEntriesIter(status) : returns DboNetBusEntriesIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboNet(DboBaseObject):
Parameters:
status: DboState &
SetColor(color) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
color: enum DboValue::ColorT

---

SetLineStyle(linestyle) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
linestyle: enum DboValue::LineStyleT
SetLineWidth(linewidth) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
linewidth: enum DboValue::LineWidthT
SetName(Name) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
Name: CString &
SetSchematicNet(pSchNet)
Class : DboNet(DboBaseObject):
Parameters:
pSchNet: DboSchematicNet *
DeleteUserProp(name) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
DeleteEffectiveProp(name) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
SetEffectivePropStringValue(name, value, bNewVer = 0) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
bNewVer: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboNet(DboBaseObject):

---

Parameters:
name: CString const &
value: CString const &
GetAttributeLockingInfo(propName, lLock, preTrigger, postTrigger) : returns bool
Class : DboNet(DboBaseObject):
Parameters:
propName: CString
lLock: MaskT &
preTrigger: CString &
postTrigger: CString &
ComputeNetName(name) : returns DboState
Class : DboNet(DboBaseObject):
Parameters:
name: CString &
NewUserProp(name, value, status) : returns DboUserProp
Class : DboNet(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
status: DboState &
SetEffectiveColorValue(dbColor, dbLineStyle, dbLineWidth, pParentSchematicOcc) : returns
DboState
Class : DboNet(DboBaseObject):
Parameters:
dbColor: enum DboValue::ColorT
dbLineStyle: enum DboValue::LineStyleT
dbLineWidth: enum DboValue::LineWidthT
pParentSchematicOcc: DboInstOccurrence *
END class DboNet(DboBaseObject):
DboNet_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &