# Class: TBaseDboWireAliasesIter(IterDefs):

START class TBaseDboWireAliasesIter(IterDefs):
GetType() : returns int
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboWireAliasesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboWireAliasesIter(IterDefs):
START class DboWireAliasesIter(TBaseDboWireAliasesIter):
Next(status) : returns DboBaseObject
Class : DboWireAliasesIter(TBaseDboWireAliasesIter):
Parameters:
status: DboState &

---

GetKey(pObject) : returns std::string
Class : DboWireAliasesIter(TBaseDboWireAliasesIter):
Parameters:
pObject: DboAlias *&
NextAlias(status) : returns DboAlias
Class : DboWireAliasesIter(TBaseDboWireAliasesIter):
Parameters:
status: DboState &
END class DboWireAliasesIter(TBaseDboWireAliasesIter):
START class DboWireJunctionsIter
NextJunction(status) : returns CPoint
Class : DboWireJunctionsIter
Parameters:
status: DboState &
END class DboWireJunctionsIter
START class TBaseDboWirePortInstsIter(IterDefs):
GetType() : returns int
Class : TBaseDboWirePortInstsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboWirePortInstsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWirePortInstsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWirePortInstsIter(IterDefs):
Parameters:
flag: UINT

---

status: DboState &
Sort(status)
Class : TBaseDboWirePortInstsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboWirePortInstsIter(IterDefs):
START class DboWirePortInstsIter(TBaseDboSchematicNetPortInstsIter):
Next(status) : returns DboBaseObject
Class : DboWirePortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboWirePortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
pObject: DboPortInst *&
NextPortInst(status) : returns DboPortInst
Class : DboWirePortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
status: DboState &
END class DboWirePortInstsIter(TBaseDboSchematicNetPortInstsIter):
START class TBaseDboWireBusEntriesIter(IterDefs):
GetType() : returns int
Class : TBaseDboWireBusEntriesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboWireBusEntriesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWireBusEntriesIter(IterDefs):

---

Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWireBusEntriesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboWireBusEntriesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboWireBusEntriesIter(IterDefs):
START class DboWireBusEntriesIter(TBaseDboPageBusEntriesIter):
Next(status) : returns DboBaseObject
Class : DboWireBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
status: DboState &
NextBusEntry(status) : returns DboBusEntry
Class : DboWireBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboWireBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
pObject: DboBusEntry *&
END class DboWireBusEntriesIter(TBaseDboPageBusEntriesIter):
START class TBaseDboWirePortsIter(IterDefs):
GetType() : returns int
Class : TBaseDboWirePortsIter(IterDefs):
Parameters:

---

GetSource() : returns DboBaseObject
Class : TBaseDboWirePortsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWirePortsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWirePortsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboWirePortsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboWirePortsIter(IterDefs):
START class DboWirePortsIter(TBaseDboPagePortsIter):
Next(status) : returns DboBaseObject
Class : DboWirePortsIter(TBaseDboPagePortsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboWirePortsIter(TBaseDboPagePortsIter):
Parameters:
pObject: DboPort *&
NextPort(status) : returns DboPort
Class : DboWirePortsIter(TBaseDboPagePortsIter):
Parameters:
status: DboState &

---

END class DboWirePortsIter(TBaseDboPagePortsIter):
START class TBaseDboWireGlobalsIter(IterDefs):
GetType() : returns int
Class : TBaseDboWireGlobalsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboWireGlobalsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWireGlobalsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWireGlobalsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboWireGlobalsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboWireGlobalsIter(IterDefs):
START class DboWireGlobalsIter(TBaseDboPageGlobalsIter):
Next(status) : returns DboBaseObject
Class : DboWireGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboWireGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:

---

pObject: DboGlobal *&
NextGlobal(status) : returns DboGlobal
Class : DboWireGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
status: DboState &
END class DboWireGlobalsIter(TBaseDboPageGlobalsIter):
START class TBaseDboWireOffPageConnectorsIter(IterDefs):
GetType() : returns int
Class : TBaseDboWireOffPageConnectorsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboWireOffPageConnectorsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWireOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWireOffPageConnectorsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboWireOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboWireOffPageConnectorsIter(IterDefs):
START class DboWireOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Next(status) : returns DboBaseObject

---

Class : DboWireOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboWireOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
pObject: DboOffPageConnector *&
NextOffPageConnector(status) : returns DboOffPageConnector
Class : DboWireOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
status: DboState &
END class DboWireOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
START class TBaseDboWireConnectedWiresIter(IterDefs):
GetType() : returns int
Class : TBaseDboWireConnectedWiresIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboWireConnectedWiresIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboWireConnectedWiresIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboWireConnectedWiresIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboWireConnectedWiresIter(IterDefs):
Parameters:

---

status: DboState &
END class TBaseDboWireConnectedWiresIter(IterDefs):
START class DboWireConnectedWiresIter(TBaseDboSchematicNetWiresIter):
Next(status) : returns DboBaseObject
Class : DboWireConnectedWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboWireConnectedWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
pObject: DboWire *&
NextWire(status) : returns DboWire
Class : DboWireConnectedWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
END class DboWireConnectedWiresIter(TBaseDboSchematicNetWiresIter):
DboBaseObjectToDboAlias(x) : returns DboAlias
Parameters:
x: DboBaseObject *
START class DboAlias(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboAlias(DboBaseObject):
Parameters:
GetName(name) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
name: CString &
GetOwner() : returns DboWire
Class : DboAlias(DboBaseObject):

---

Parameters:
GetContainingLib() : returns DboLib
Class : DboAlias(DboBaseObject):
Parameters:
GetId(status) : returns unsigned long
Class : DboAlias(DboBaseObject):
Parameters:
status: DboState &
GetLocation(status) : returns CPoint
Class : DboAlias(DboBaseObject):
Parameters:
status: DboState &
GetRotation(status) : returns RotationT
Class : DboAlias(DboBaseObject):
Parameters:
status: DboState &
GetFont(status) : returns LOGFONT
Class : DboAlias(DboBaseObject):
Parameters:
status: DboState &
IsFontDefault(status) : returns int
Class : DboAlias(DboBaseObject):
Parameters:
status: DboState &
GetColor(status) : returns ColorT
Class : DboAlias(DboBaseObject):
Parameters:
status: DboState &
GetBoundingBox() : returns CRect
Class : DboAlias(DboBaseObject):
Parameters:

---

sGetName(obj, status) : returns CString
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationX(obj, status) : returns int
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLocationY(obj, status) : returns int
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetRotation(obj, status) : returns RotationT
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetFont(obj, status) : returns LOGFONT
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetColor(obj, status) : returns ColorT
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
IsBoundingBoxDirty() : returns int
Class : DboAlias(DboBaseObject):
Parameters:

---

IsBundleObject() : returns bool
Class : DboAlias(DboBaseObject):
Parameters:
ValidateNGName(OldName, NewName, status) : returns int
Class : DboAlias(DboBaseObject):
Parameters:
OldName: CString const &
NewName: CString const &
status: DboState &
SetName(name) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
name: CString &
SetLocation(location) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
location: CPoint
SetRotation(rotation) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
rotation: enum DboValue::RotationT
SetFont(font) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
font: LOGFONT &
SetColor(color) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
color: enum DboValue::ColorT
SetBoundingBox(boundingBox) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
boundingBox: CRect

---

SetOwnerBoundingBoxDirty(bSetting)
Class : DboAlias(DboBaseObject):
Parameters:
bSetting: int
sSetName(obj, name) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
name: CString &
sSetLocationX(obj, x) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
x: int
sSetLocationY(obj, y) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
y: int
sSetRotation(obj, rotation) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
rotation: enum DboValue::RotationT
sSetFont(obj, font) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *
font: LOGFONT &
sSetColor(obj, color) : returns DboState
Class : DboAlias(DboBaseObject):
Parameters:
obj: DboBaseObject *

---

color: enum DboValue::ColorT
SetBoundingBoxDirty(bSetting)
Class : DboAlias(DboBaseObject):
Parameters:
bSetting: int
END class DboAlias(DboBaseObject):
DboAlias_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboAlias_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboAlias_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboAlias_sGetRotation(obj, status) : returns RotationT
Parameters:
obj: DboBaseObject *
status: DboState &
DboAlias_sGetFont(obj, status) : returns LOGFONT
Parameters:
obj: DboBaseObject *
status: DboState &
DboAlias_sGetColor(obj, status) : returns ColorT
Parameters:
obj: DboBaseObject *
status: DboState &
DboAlias_sSetName(obj, name) : returns DboState