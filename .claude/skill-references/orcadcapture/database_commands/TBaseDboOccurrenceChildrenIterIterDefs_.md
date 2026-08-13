# Class: TBaseDboOccurrenceChildrenIter(IterDefs):

START class TBaseDboOccurrenceChildrenIter(IterDefs):
GetType() : returns int
Class : TBaseDboOccurrenceChildrenIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboOccurrenceChildrenIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboOccurrenceChildrenIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboOccurrenceChildrenIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboOccurrenceChildrenIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboOccurrenceChildrenIter(IterDefs):
START class DboOccurrenceChildrenIter(TBaseDboOccurrenceChildrenIter):
NextOccurrence(status) : returns DboOccurrence
Class : DboOccurrenceChildrenIter(TBaseDboOccurrenceChildrenIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboOccurrenceChildrenIter(TBaseDboOccurrenceChildrenIter):
Parameters:
status: DboState &

---

GetKey(pObject) : returns unsigned long
Class : DboOccurrenceChildrenIter(TBaseDboOccurrenceChildrenIter):
Parameters:
pObject: DboOccurrence *&
END class DboOccurrenceChildrenIter(TBaseDboOccurrenceChildrenIter):
DboEffectivePropsIterToDboInstOccurrenceEffectivePropsIter(x) : returns
DboInstOccurrenceEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboInstOccurrenceEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboInstOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboInstOccurrenceEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboInstOccurrenceEffectivePropsIter(DboEffectivePropsIter):
DboOccurrenceToDboNetOccurrence(x) : returns DboNetOccurrence
Parameters:
x: DboOccurrence *
START class DboNetOccurrence(DboOccurrence):

---

GetObjectType() : returns ObjectTypeT
Class : DboNetOccurrence(DboOccurrence):
Parameters:
GetSchematic(status) : returns DboSchematic
Class : DboNetOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetPathName(name, chSeparator = '/') : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetPathName(name) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString &
GetRefPathName(name, chSeparator = '/') : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString &
chSeparator: char
GetRefPathName(name) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString &
GetNetName(name) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString &
GetNet(status) : returns DboSchematicNet
Class : DboNetOccurrence(DboOccurrence):
Parameters:
status: DboState &

---

GetDeletedNet(status) : returns DboSchematicNet
Class : DboNetOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetFlatNet(status) : returns DboFlatNet
Class : DboNetOccurrence(DboOccurrence):
Parameters:
status: DboState &
GetCanonicalName(bVHDL) : returns CString
Class : DboNetOccurrence(DboOccurrence):
Parameters:
bVHDL: int
GetCanonicalName(bVHDL, nToolId, strName) : returns CString
Class : DboNetOccurrence(DboOccurrence):
Parameters:
bVHDL: int
nToolId: int
strName: CString &
GetSchematicNetId(status) : returns unsigned long
Class : DboNetOccurrence(DboOccurrence):
Parameters:
status: DboState &
sGetPathName(obj, status) : returns CString
Class : DboNetOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetNetName(obj, status) : returns CString
Class : DboNetOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetId(obj, status) : returns int
Class : DboNetOccurrence(DboOccurrence):
Parameters:
obj: DboBaseObject *
status: DboState &
GetEffectivePropValueExists(name, bExists) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString const &
bExists: int &
GetInstance(status) : returns DboBaseObject
Class : DboNetOccurrence(DboOccurrence):
Parameters:
status: DboState &
EffectivePropsMatch(strFindWhat, bMatchCase, PatternMatcher = DboPatternMatch) : returns int
Class : DboNetOccurrence(DboOccurrence):
Parameters:
strFindWhat: CString const &
bMatchCase: int
PatternMatcher: TPatternMatch
EffectivePropsMatch(strFindWhat, bMatchCase) : returns int
Class : DboNetOccurrence(DboOccurrence):
Parameters:
strFindWhat: CString const &
bMatchCase: int
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboNetOccurrence(DboOccurrence):
Parameters:
status: DboState &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &

---

bNewVersion: int
SetEffectivePropStringValue(name, value) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString const &
value: CString const &
GetAttributeLockingInfo(propName, lLock, preTrigger, postTrigger) : returns bool
Class : DboNetOccurrence(DboOccurrence):
Parameters:
propName: CString
lLock: MaskT &
preTrigger: CString &
postTrigger: CString &
DeleteEffectiveProp(name) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
name: CString const &
SetSchematicNetId(newNetId) : returns DboState
Class : DboNetOccurrence(DboOccurrence):
Parameters:
newNetId: unsigned long
END class DboNetOccurrence(DboOccurrence):
DboNetOccurrence_sGetPathName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetOccurrence_sGetNetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboNetOccurrence_sGetId(obj, status) : returns int
Parameters: