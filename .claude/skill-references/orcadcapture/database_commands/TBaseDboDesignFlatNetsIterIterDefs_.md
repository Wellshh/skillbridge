# Class: TBaseDboDesignFlatNetsIter(IterDefs):

START class TBaseDboDesignFlatNetsIter(IterDefs):
GetType() : returns int
Class : TBaseDboDesignFlatNetsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboDesignFlatNetsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboDesignFlatNetsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboDesignFlatNetsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboDesignFlatNetsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboDesignFlatNetsIter(IterDefs):
START class DboDesignFlatNetsIter(TBaseDboDesignFlatNetsIter):
NextFlatNet(status) : returns DboFlatNet
Class : DboDesignFlatNetsIter(TBaseDboDesignFlatNetsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboDesignFlatNetsIter(TBaseDboDesignFlatNetsIter):
Parameters:
status: DboState &

---

GetKey(pObject) : returns std::string
Class : DboDesignFlatNetsIter(TBaseDboDesignFlatNetsIter):
Parameters:
pObject: DboFlatNet *&
END class DboDesignFlatNetsIter(TBaseDboDesignFlatNetsIter):
START class TBaseDboDesignGlobalsIter(IterDefs):
GetType() : returns int
Class : TBaseDboDesignGlobalsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboDesignGlobalsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboDesignGlobalsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboDesignGlobalsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboDesignGlobalsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboDesignGlobalsIter(IterDefs):
START class DboDesignGlobalsIter(TBaseDboDesignFlatNetsIter):
NextGlobal(status) : returns DboFlatNet
Class : DboDesignGlobalsIter(TBaseDboDesignFlatNetsIter):

---

Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboDesignGlobalsIter(TBaseDboDesignFlatNetsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboDesignGlobalsIter(TBaseDboDesignFlatNetsIter):
Parameters:
pObject: DboFlatNet *&
END class DboDesignGlobalsIter(TBaseDboDesignFlatNetsIter):
DboLibCachesIterToDboDesignCachesIter(x) : returns DboDesignCachesIter
Parameters:
x: DboLibCachesIter *
START class DboDesignCachesIter(DboLibCachesIter):
NextDesignCache(status) : returns DboBaseObject
Class : DboDesignCachesIter(DboLibCachesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboDesignCachesIter(DboLibCachesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboDesignCachesIter(DboLibCachesIter):
Parameters:
pObject: DboBaseObject *&
END class DboDesignCachesIter(DboLibCachesIter):
START class DboAnnotateRange

---

GetRefdesPrefix() : returns CString
Class : DboAnnotateRange
Parameters:
GetStartIndex() : returns int
Class : DboAnnotateRange
Parameters:
GetLastIndex() : returns int
Class : DboAnnotateRange
Parameters:
SetRefDesPrefix(refdesprfx)
Class : DboAnnotateRange
Parameters:
refdesprfx: CString
SetStartIndex(sIndex)
Class : DboAnnotateRange
Parameters:
sIndex: int
SetLastIndex(lIndex)
Class : DboAnnotateRange
Parameters:
lIndex: int
END class DboAnnotateRange
START class DboAnnotateControl
GetPagePath() : returns CString
Class : DboAnnotateControl
Parameters:
GetSchName() : returns CString
Class : DboAnnotateControl
Parameters:
GetNumRange() : returns int

---

Class : DboAnnotateControl
Parameters:
GetRangeAt(pos) : returns DboAnnotateRange
Class : DboAnnotateControl
Parameters:
pos: int
END class DboAnnotateControl
START class DboModifiedFlatNetsIter
NextId(pFlatNetId, pFlatNetStatus) : returns DboState
Class : DboModifiedFlatNetsIter
Parameters:
pFlatNetId: unsigned long &
pFlatNetStatus: int &
END class DboModifiedFlatNetsIter
START class DboInstOccMapper
GetOccurrences() : returns std::vector<(p.DboOccurrence)>
Class : DboInstOccMapper
Parameters:
GetOccurrencesCount() : returns int
Class : DboInstOccMapper
Parameters:
GetOccurrencesAtPos(pos) : returns DboOccurrence
Class : DboInstOccMapper
Parameters:
pos: int
GetOccurrenceFromParent(pParent) : returns DboOccurrence
Class : DboInstOccMapper
Parameters:
pParent: DboInstOccurrence *

---

END class DboInstOccMapper
DboBaseObjectToDboOccurrence(x) : returns DboOccurrence
Parameters:
x: DboBaseObject *
START class DboOccurrence(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboOccurrence(DboBaseObject):
Parameters:
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
nNameID: UINT
value: CString &
GetEffectivePropStringValue(name, value) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
value: CString &
GetEffectivePropStringValueNC(name, value) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
value: CString &
GetSchematic(status) : returns DboSchematic
Class : DboOccurrence(DboBaseObject):
Parameters:
status: DboState &
GetPathName(name, chSeparator = '/') : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString &
chSeparator: char

---

GetPathName(name) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString &
GetRefPathName(name, chSeparator = '/') : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString &
chSeparator: char
GetRefPathName(name) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString &
GetIdPathName(name, chSeparator = '/') : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString &
chSeparator: char
GetIdPathName(name) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString &
GetId(status) : returns unsigned long
Class : DboOccurrence(DboBaseObject):
Parameters:
status: DboState &
GetParent() : returns DboBaseObject
Class : DboOccurrence(DboBaseObject):
Parameters:
GetOwner() : returns DboDesign
Class : DboOccurrence(DboBaseObject):
Parameters:

---

GetContainingLib() : returns DboLib
Class : DboOccurrence(DboBaseObject):
Parameters:
GetDepth(status) : returns int
Class : DboOccurrence(DboBaseObject):
Parameters:
status: DboState &
GetBackannotation(name, status) : returns DboUserProp
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
status: DboState &
GetBackannotatedStringValue(name, value) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
value: CString &
HasPropertyThatExists(status) : returns int
Class : DboOccurrence(DboBaseObject):
Parameters:
status: DboState &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
GetOccProp(name, status) : returns DbBaseProp
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
status: DboState &

---

GetInstance(status) : returns DboBaseObject
Class : DboOccurrence(DboBaseObject):
Parameters:
status: DboState &
GetCanonicalName(bVHDL) : returns CString
Class : DboOccurrence(DboBaseObject):
Parameters:
bVHDL: int
GetDesignTransactionCount() : returns int
Class : DboOccurrence(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboOccurrence(DboBaseObject):
Parameters:
NewOccurrenceEdit() : returns int
Class : DboOccurrence(DboBaseObject):
Parameters:
DeleteUserProp(name) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
SetUserPropStringValue(name, value) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
DeleteUserPropValue(name) : returns DboState
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
MakeVHDL(conName)

---

Class : DboOccurrence(DboBaseObject):
Parameters:
conName: CString &
SetDesignTransactionCount(nCount)
Class : DboOccurrence(DboBaseObject):
Parameters:
nCount: int
NewUserProp(name, status) : returns DboUserProp
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
status: DboState &
NewUserProp(name, value, status) : returns DboUserProp
Class : DboOccurrence(DboBaseObject):
Parameters:
name: CString const &
value: CString const &
status: DboState &
END class DboOccurrence(DboBaseObject):
START class DboOccurrenceArray
END class DboOccurrenceArray
DboOccurrenceToDboPortOccurrence(x) : returns DboPortOccurrence
Parameters:
x: DboOccurrence *
START class DboPortOccurrence(DboOccurrence):
GetObjectType() : returns ObjectTypeT
Class : DboPortOccurrence(DboOccurrence):
Parameters:
GetId(status) : returns unsigned long
Class : DboPortOccurrence(DboOccurrence):

---

Parameters:
status: DboState &
GetSchematic(status) : returns DboSchematic
Class : DboPortOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPathName(name, chSeparator = '/') : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetPathName(name) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString &
GetRefPathName(name, chSeparator = '/') : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetRefPathName(name) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString &
GetName(name) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString &
GetPathNameNumber(name, chSeparator = '.') : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char

---

GetPathNameNumber(name) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString &
GetPortInst(status) : returns DboPortInst
Class : DboPortOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPort(status) : returns DboSchematicPort
Class : DboPortOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPortInstPinID() : returns unsigned short
Class : DboPortOccurrence(DboOccurrence):
Parameters:
GetSchematicPortName() : returns CString
Class : DboPortOccurrence(DboOccurrence):
Parameters:
IsOrphanPort() : returns int
Class : DboPortOccurrence(DboOccurrence):
Parameters:
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
GetEffectivePropValueExists(name, bExists) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString const &

---

bExists: int &
sGetPathName(obj, status) : returns CString
Class : DboPortOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetId(obj, status) : returns int
Class : DboPortOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
GetInstance(status) : returns DboBaseObject
Class : DboPortOccurrence(DboOccurrence):
Parameters:
status: DboState &
FindInstance(status) : returns DboBaseObject
Class : DboPortOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetFlatNet() : returns DboFlatNet
Class : DboPortOccurrence(DboOccurrence):
Parameters:
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboPortOccurrence(DboOccurrence):
Parameters:
status: DboState &
SetId(nId) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
nId: unsigned long
MorphPortOccurrence(pPartInst) : returns DboPortOccurrence
Class : DboPortOccurrence(DboOccurrence):

---

Parameters:
pPartInst: DboPortInst *
MorphPortOccurrence(pPort, pPortInst) : returns DboPortOccurrence
Class : DboPortOccurrence(DboOccurrence):
Parameters:
pPort: DboSchematicPort *
pPortInst: DboPortInst *
SetSchematicPortName(pSchematicPortName) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
pSchematicPortName: char const *
SetPortInstPinID(nPinID) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
nPinID: unsigned short
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
SetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
nNameID: UINT
value: CString const &
DeleteEffectiveProp(name) : returns DboState
Class : DboPortOccurrence(DboOccurrence):

---

Parameters:
name: CString const &
SetEffectivePropStringValueForIref(name, value) : returns DboState
Class : DboPortOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
ProcessFlatNetForPortOccurrence()
Class : DboPortOccurrence(DboOccurrence):
Parameters:
END class DboPortOccurrence(DboOccurrence):
DboPortOccurrence_sGetPathName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortOccurrence_sGetId(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
START class DboPortOccurrenceArray
END class DboPortOccurrenceArray
DboPortOccurrenceToDboPortBusMemberOccurrence(x) : returns DboPortBusMemberOccurrence
Parameters:
x: DboPortOccurrence *
START class DboPortBusMemberOccurrence(DboPortOccurrence):
GetObjectType() : returns ObjectTypeT
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
GetPort(status) : returns DboSchematicPort

---

Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
status: DboState &
GetPortInst(status) : returns DboPortInst
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
status: DboState &
GetPathName(name, chSeparator = '/') : returns DboState
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
name: CString &
chSeparator: char
GetPathName(name) : returns DboState
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
name: CString &
GetRefPathName(name, chSeparator = '/') : returns DboState
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
name: CString &
chSeparator: char
GetRefPathName(name) : returns DboState
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
name: CString &
GetMemberName(name) : returns DboState
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
name: CString &
sGetMemberName(obj, status) : returns CString
Class : DboPortBusMemberOccurrence(DboPortOccurrence):
Parameters:
obj: DboBaseObject *

---

status: DboState &
END class DboPortBusMemberOccurrence(DboPortOccurrence):
DboPortBusMemberOccurrence_sGetMemberName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboEffectivePropsIterToDboPortOccurrenceEffectivePropsIter(x) : returns
DboPortOccurrenceEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboPortOccurrenceEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboPortOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboPortOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboPortOccurrenceEffectivePropsIter(DboEffectivePropsIter):
START class DboDirectoryRec
END class DboDirectoryRec
START class DboDirectoryEntry

---

END class DboDirectoryEntry
START class DboDirectory
GetSaveTime() : returns time_t
Class : DboDirectory
Parameters:
GetEntry(name, status, bCaseInsensitive = 0) : returns DboDirectoryEntry
Class : DboDirectory
Parameters:
name: char const *
status: DboState &
bCaseInsensitive: int
GetEntry(name, status) : returns DboDirectoryEntry
Class : DboDirectory
Parameters:
name: char const *
status: DboState &
GetObject(name, status) : returns DboBaseObject
Class : DboDirectory
Parameters:
name: char const *
status: DboState &
GetCreateTime(name, status) : returns FILETIME
Class : DboDirectory
Parameters:
name: char const *
status: DboState &
GetModifyTime(name, status) : returns FILETIME
Class : DboDirectory
Parameters:
name: char const *
status: DboState &

---

IsInMemory(name, status) : returns int
Class : DboDirectory
Parameters:
name: char const *
status: DboState &
IsAnyEntryModified() : returns int
Class : DboDirectory
Parameters:
IsModified(name) : returns int
Class : DboDirectory
Parameters:
name: char const *
IsSaved(name) : returns int
Class : DboDirectory
Parameters:
name: char const *
NewEntriesIter(status) : returns DboDirectoryEntriesIter
Class : DboDirectory
Parameters:
status: DboState &
NewObjectsIter(status) : returns DboDirectoryObjectsIter
Class : DboDirectory
Parameters:
status: DboState &
MarkModified(name) : returns DboState
Class : DboDirectory
Parameters:
name: char const *
MarkToBeSaved(name) : returns DboState
Class : DboDirectory
Parameters:
name: char const *

---

MarkSaved(name) : returns DboState
Class : DboDirectory
Parameters:
name: char const *
MarkToBeDeleted(name) : returns DboState
Class : DboDirectory
Parameters:
name: char const *
ClearObject(name) : returns DboState
Class : DboDirectory
Parameters:
name: char const *
ClearModified(name) : returns DboState
Class : DboDirectory
Parameters:
name: char const *
END class DboDirectory
START class DboDirectoryEntriesIter
NextEntry(status) : returns DboDirectoryEntry
Class : DboDirectoryEntriesIter
Parameters:
status: DboState &
END class DboDirectoryEntriesIter
START class DboDirectoryObjectsIter
NextObject(status) : returns DboBaseObject
Class : DboDirectoryObjectsIter
Parameters:
status: DboState &
END class DboDirectoryObjectsIter