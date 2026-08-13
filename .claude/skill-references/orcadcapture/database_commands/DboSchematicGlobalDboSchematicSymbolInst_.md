# Class: DboSchematicGlobal(DboSchematicSymbolInst):

DboSchematicSymbolInstToDboSchematicGlobal(x) : returns DboSchematicGlobal
Parameters:
x: DboSchematicSymbolInst *
START class DboSchematicGlobal(DboSchematicSymbolInst):
GetObjectType() : returns ObjectTypeT
Class : DboSchematicGlobal(DboSchematicSymbolInst):
Parameters:
GetPinType(status) : returns PinTypeT
Class : DboSchematicGlobal(DboSchematicSymbolInst):
Parameters:
status: DboState &
IsPower(status) : returns int
Class : DboSchematicGlobal(DboSchematicSymbolInst):
Parameters:
status: DboState &
END class DboSchematicGlobal(DboSchematicSymbolInst):
DboBaseObjectToDboSchematicNet(x) : returns DboSchematicNet
Parameters:
x: DboBaseObject *
DboInstOccMapperToDboSchematicNet(x) : returns DboSchematicNet
Parameters:
x: DboInstOccMapper *
START class DboSchematicNet(DboBaseObject,DboInstOccMapper):
GetObjectType() : returns ObjectTypeT
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
GetId(status) : returns unsigned long
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &

---

GetOwner() : returns DboSchematic
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
GetContainingLib() : returns DboLib
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
GetSchNetNameForOldPspiceConnectivity(pEffectiveNetName) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
pEffectiveNetName: CString &
GetName(name) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString &
IsGlobal(status) : returns int
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
IsBusMember(pBusNet, status) : returns int
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
pBusNet: DboSchematicNet *&
status: DboState &
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
nNameID: UINT
value: CString &
GetEffectivePropStringValue(name, value) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &

---

value: CString &
sGetName(obj, status) : returns CString
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetId(obj, status) : returns int
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
EffectivePropsMatch(strFindWhat, bMatchCase, PatternMatcher = DboPatternMatch) : returns int
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
strFindWhat: CString const &
bMatchCase: int
PatternMatcher: TPatternMatch
EffectivePropsMatch(strFindWhat, bMatchCase) : returns int
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
strFindWhat: CString const &
bMatchCase: int
ResolveComputedNameConflict(pName) : returns CString
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
pName: CString
GetLocalNetName(name) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString &
GetObjectOccurrence(pParentSchematicOcc) : returns DboOccurrence
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:

---

pParentSchematicOcc: DboInstOccurrence *
GetEffectivePropValueExists(name, bExists) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
bExists: int &
GetEffectivePropValueChoices(name, choices) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
choices: CStringList &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
GetObjectOccurrences(occArr, pDesign, status, bOnlyCurrent = False)
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool
GetObjectOccurrences(occArr, pDesign, status)
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
GetColor(status) : returns ColorT
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:

---

status: DboState &
GetLineStyle(status) : returns LineStyleT
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetLineWidth(status) : returns LineWidthT
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
GetParentObj() : returns DboBaseObject
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
HasBundleConnection() : returns bool
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
HasNonNGOverrider() : returns bool
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
IsBundleObject() : returns bool
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
NewWiresIter(status, mode = TOP) : returns DboSchematicNetWiresIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewWiresIter(status) : returns DboSchematicNetWiresIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
NewPortInstsIter(status, mode = TOP) : returns DboSchematicNetPortInstsIter

---

Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPortInstsIter(status) : returns DboSchematicNetPortInstsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
NewPortsIter(status, mode = TOP) : returns DboSchematicNetPortsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPortsIter(status) : returns DboSchematicNetPortsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
NewGlobalsIter(status) : returns DboSchematicNetGlobalsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
NewOffPageConnectorsIter(status) : returns DboSchematicNetOffPageConnectorsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
NewNetsIter(status, mode = TOP) : returns DboSchematicNetNetsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewNetsIter(status) : returns DboSchematicNetNetsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:

---

status: DboState &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
status: DboState &
SetColor(color) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
color: enum DboValue::ColorT
SetLineStyle(linestyle) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
linestyle: enum DboValue::LineStyleT
SetLineWidth(linewidth) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
linewidth: enum DboValue::LineWidthT
SetEffectivePropStringValue(name, value, bNewObj = 0) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
value: CString const &
bNewObj: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
value: CString const &
GetAttributeLockingInfo(propName, lLock, preTrigger, postTrigger) : returns bool
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
propName: CString
lLock: MaskT &

---

preTrigger: CString &
postTrigger: CString &
DeleteEffectiveProp(name) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString const &
SetName(Name) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
Name: CString &
ComputeNetName(name) : returns DboState
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
name: CString &
GetBusNets() : returns DboPtrArray
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
AddBusNet(pBusNet)
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
pBusNet: DboSchematicNetBus *
RemoveBusNet(pBusNet)
Class : DboSchematicNet(DboBaseObject,DboInstOccMapper):
Parameters:
pBusNet: DboSchematicNetBus *
END class DboSchematicNet(DboBaseObject,DboInstOccMapper):
DboSchematicNet_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboSchematicNet_sGetId(obj, status) : returns int