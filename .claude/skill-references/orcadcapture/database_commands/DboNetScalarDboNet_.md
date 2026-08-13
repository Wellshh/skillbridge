# Class: DboNetScalar(DboNet):

DboNet_sGetNetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboNet_sGetId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetToDboNetScalar(x) : returns DboNetScalar
Parameters:
x: DboNet *
START class DboNetScalar(DboNet):
GetObjectType() : returns ObjectTypeT
Class : DboNetScalar(DboNet):
Parameters:
GetBundleOwnerForBus() : returns CString
Class : DboNetScalar(DboNet):
Parameters:
END class DboNetScalar(DboNet):
DboNetToDboNetBus(x) : returns DboNetBus
Parameters:
x: DboNet *
START class DboNetBus(DboNet):
GetObjectType() : returns ObjectTypeT
Class : DboNetBus(DboNet):
Parameters:
GetWidth(status) : returns int
Class : DboNetBus(DboNet):
Parameters:
status: DboState &

---

GetMember(nPos, status) : returns DboNet
Class : DboNetBus(DboNet):
Parameters:
nPos: int
status: DboState &
GetPosition(pNetMember) : returns int
Class : DboNetBus(DboNet):
Parameters:
pNetMember: DboNet *
HasMember(pNet) : returns int
Class : DboNetBus(DboNet):
Parameters:
pNet: DboNet *
IsExpanded() : returns int
Class : DboNetBus(DboNet):
Parameters:
IsBundle() : returns int
Class : DboNetBus(DboNet):
Parameters:
SetIsBundle(isSetBundle) : returns int
Class : DboNetBus(DboNet):
Parameters:
isSetBundle: int
GetBundleOwner(BundleOwner) : returns int
Class : DboNetBus(DboNet):
Parameters:
BundleOwner: CString &
IsBundleObject() : returns bool
Class : DboNetBus(DboNet):
Parameters:
NewMembersIter(status, mode = ALL) : returns DboNetBusMembersIter

---

Class : DboNetBus(DboNet):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewMembersIter(status) : returns DboNetBusMembersIter
Class : DboNetBus(DboNet):
Parameters:
status: DboState &
RemoveMember(nPos) : returns DboState
Class : DboNetBus(DboNet):
Parameters:
nPos: int
END class DboNetBus(DboNet):
DboEffectivePropsIterToDboNetEffectivePropsIter(x) : returns DboNetEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboNetEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboNetEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboNetEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &

---

END class DboNetEffectivePropsIter(DboEffectivePropsIter):
START class TBaseDboNetWiresIter(IterDefs):
GetType() : returns int
Class : TBaseDboNetWiresIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboNetWiresIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboNetWiresIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboNetWiresIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboNetWiresIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboNetWiresIter(IterDefs):
START class DboNetWiresIter(TBaseDboSchematicNetWiresIter):
NextWire(status) : returns DboWire
Class : DboNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:

---

status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
pObject: DboWire *&
END class DboNetWiresIter(TBaseDboSchematicNetWiresIter):
START class TBaseDboNetPortInstsIter(IterDefs):
GetType() : returns int
Class : TBaseDboNetPortInstsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboNetPortInstsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboNetPortInstsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboNetPortInstsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboNetPortInstsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboNetPortInstsIter(IterDefs):
START class DboNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
NextPortInst(status) : returns DboPortInst

---

Class : DboNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
Parameters:
pObject: DboPortInst *&
END class DboNetPortInstsIter(TBaseDboSchematicNetPortInstsIter):
START class TBaseDboNetBusEntriesIter(IterDefs):
GetType() : returns int
Class : TBaseDboNetBusEntriesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboNetBusEntriesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboNetBusEntriesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboNetBusEntriesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboNetBusEntriesIter(IterDefs):
Parameters:

---

status: DboState &
END class TBaseDboNetBusEntriesIter(IterDefs):
START class DboNetBusEntriesIter(TBaseDboPageBusEntriesIter):
NextBusEntry(status) : returns DboBusEntry
Class : DboNetBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboNetBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboNetBusEntriesIter(TBaseDboPageBusEntriesIter):
Parameters:
pObject: DboBusEntry *&
END class DboNetBusEntriesIter(TBaseDboPageBusEntriesIter):
START class TBaseDboNetPortsIter(IterDefs):
GetType() : returns int
Class : TBaseDboNetPortsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboNetPortsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboNetPortsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboNetPortsIter(IterDefs):

---

Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboNetPortsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboNetPortsIter(IterDefs):
START class DboNetPortsIter(TBaseDboPagePortsIter):
NextPort(status) : returns DboPort
Class : DboNetPortsIter(TBaseDboPagePortsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboNetPortsIter(TBaseDboPagePortsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboNetPortsIter(TBaseDboPagePortsIter):
Parameters:
pObject: DboPort *&
END class DboNetPortsIter(TBaseDboPagePortsIter):
START class TBaseDboNetGlobalsIter(IterDefs):
GetType() : returns int
Class : TBaseDboNetGlobalsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboNetGlobalsIter(IterDefs):
Parameters:

---

Next(status) : returns DboBaseObject
Class : TBaseDboNetGlobalsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboNetGlobalsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboNetGlobalsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboNetGlobalsIter(IterDefs):
START class DboNetGlobalsIter(TBaseDboPageGlobalsIter):
NextGlobal(status) : returns DboGlobal
Class : DboNetGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboNetGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboNetGlobalsIter(TBaseDboPageGlobalsIter):
Parameters:
pObject: DboGlobal *&
END class DboNetGlobalsIter(TBaseDboPageGlobalsIter):
START class TBaseDboNetOffPageConnectorsIter(IterDefs):
GetType() : returns int

---

Class : TBaseDboNetOffPageConnectorsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboNetOffPageConnectorsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboNetOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboNetOffPageConnectorsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboNetOffPageConnectorsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboNetOffPageConnectorsIter(IterDefs):
START class DboNetOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
NextOffPageConnector(status) : returns DboOffPageConnector
Class : DboNetOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboNetOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboNetOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
Parameters:

---

pObject: DboOffPageConnector *&
END class DboNetOffPageConnectorsIter(TBaseDboPageOffPageConnectorsIter):
START class TBaseDboNetBusMembersIter(IterDefs):
GetType() : returns int
Class : TBaseDboNetBusMembersIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboNetBusMembersIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboNetBusMembersIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboNetBusMembersIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboNetBusMembersIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboNetBusMembersIter(IterDefs):
START class DboNetBusMembersIter(TBaseDboSchematicNetNetsIter):
NextMember(status) : returns DboNet
Class : DboNetBusMembersIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject

---

Class : DboNetBusMembersIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboNetBusMembersIter(TBaseDboSchematicNetNetsIter):
Parameters:
pObject: DboNet *&
END class DboNetBusMembersIter(TBaseDboSchematicNetNetsIter):
START class DboNetAliasesIter
NextAlias(nxtAlias) : returns DboState
Class : DboNetAliasesIter
Parameters:
nxtAlias: CString &
END class DboNetAliasesIter
START class DboOffPageConnectorOccurrence(DboOccurrence):
GetObjectType() : returns ObjectTypeT
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
SetId(nId) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
nId: unsigned long
GetId(status) : returns unsigned long
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetSchematic(status) : returns DboSchematic
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
status: DboState &

---

SetOffPageConnectorId(nOffPageId) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
nOffPageId: unsigned long
GetOffPageConnectorId(status) : returns unsigned long
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetSchematicPath(name) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString &
GetPathName(name, chSeparator = '/') : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetPathName(name) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString &
GetRefPathName(name, chSeparator = '/') : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetRefPathName(name) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):

---

Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
SetEffectivePropStringValueForIref(name, value) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
SetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
nNameID: UINT
value: CString const &
DeleteEffectiveProp(name) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString const &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
status: DboState &

---

GetEffectivePropValueExists(name, bExists) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString const &
bExists: int &
sGetPathName(obj, status) : returns CString
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSchematicPath(obj, status) : returns CString
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetId(obj, status) : returns int
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetName(obj, status) : returns CString
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
GetInstance(status) : returns DboBaseObject
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetName(name) : returns DboState
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString &

---

SetOccName(name)
Class : DboOffPageConnectorOccurrence(DboOccurrence):
Parameters:
name: CString const &
END class DboOffPageConnectorOccurrence(DboOccurrence):
DboOffPageConnectorOccurrence_sGetPathName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboOffPageConnectorOccurrence_sGetSchematicPath(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboOffPageConnectorOccurrence_sGetId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboOffPageConnectorOccurrence_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
START class DboOffPageConnectorOccurrenceArray
END class DboOffPageConnectorOccurrenceArray
START class DboOffPageConnectorOccurrenceEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboOffPageConnectorOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &

---

bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboOffPageConnectorOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboOffPageConnectorOccurrenceEffectivePropsIter(DboEffectivePropsIter):
START class DboPathMgr
sInit()
Class : DboPathMgr
sExit()
Class : DboPathMgr
sLookupPath(pPath, bMemorize = False) : returns DboState
Class : DboPathMgr
Parameters:
pPath: char const *
bMemorize: bool
sLookupPath(pPath) : returns DboState
Class : DboPathMgr
Parameters:
pPath: char const *
sGetAllPaths() : returns PathsMapT
Class : DboPathMgr
sClearPathHistory(pPath = None)
Class : DboPathMgr
Parameters:
pPath: char const *

---

sClearPathHistory()
Class : DboPathMgr
sSetPathLookupTimeout(pTimeOut)
Class : DboPathMgr
Parameters:
pTimeOut: unsigned long
sGetPathLookupTimeout() : returns unsigned long
Class : DboPathMgr
sSetExitWaitTimeout(pTimeOut)
Class : DboPathMgr
Parameters:
pTimeOut: unsigned long
sGetFullPath(pPath) : returns std::string
Class : DboPathMgr
Parameters:
pPath: char const *
sIsReadOnly(pPath) : returns bool
Class : DboPathMgr
Parameters:
pPath: char const *
sForgetReadOnlyAttribute(pPath = None)
Class : DboPathMgr
Parameters:
pPath: char const *
sForgetReadOnlyAttribute()
Class : DboPathMgr
sDumpToSessionLog(pPath = None)
Class : DboPathMgr
Parameters:
pPath: char const *
sDumpToSessionLog()

---

Class : DboPathMgr
sSetLegacySaveAs(bVal)
Class : DboPathMgr
Parameters:
bVal: int
sGetLegacySaveAs() : returns int
Class : DboPathMgr
END class DboPathMgr
DboPathMgr_sInit()
DboPathMgr_sExit()
sLookupPath(pPath, bMemorize = False) : returns DboState
Parameters:
pPath: char const *
bMemorize: bool
DboPathMgr_sLookupPath(pPath) : returns DboState
Parameters:
pPath: char const *
DboPathMgr_sGetAllPaths() : returns PathsMapT
sClearPathHistory(pPath = None)
Parameters:
pPath: char const *
DboPathMgr_sClearPathHistory()
DboPathMgr_sSetPathLookupTimeout(pTimeOut)
Parameters:
pTimeOut: unsigned long
DboPathMgr_sGetPathLookupTimeout() : returns unsigned long
DboPathMgr_sSetExitWaitTimeout(pTimeOut)