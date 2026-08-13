# Class: DboDefinition

START class DboDefinition
END class DboDefinition
START class DboPointerException
what() : returns char
Class : DboPointerException
Parameters:
END class DboPointerException
START class DboNullPointerException(DboPointerException):
what() : returns char
Class : DboNullPointerException(DboPointerException):
Parameters:
END class DboNullPointerException(DboPointerException):
START class DboInvalidPointerAccessException(DboPointerException):
what() : returns char
Class : DboInvalidPointerAccessException(DboPointerException):

---

Parameters:
END class DboInvalidPointerAccessException(DboPointerException):
START class DboInvalidDeleteException(DboPointerException):
what() : returns char
Class : DboInvalidDeleteException(DboPointerException):
Parameters:
END class DboInvalidDeleteException(DboPointerException):
START class DboBaseObject
IsPtrDeleted(pPtr) : returns bool
Class : DboBaseObject
Parameters:
pPtr: void *
IsBitmaskAllowed(pBitmask) : returns int
Class : DboBaseObject
Parameters:
pBitmask: enum DboBaseObject::BitmaskT
GetMask() : returns MaskT
Class : DboBaseObject
Parameters:
GetBitmask(pBitmask) : returns int
Class : DboBaseObject
Parameters:
pBitmask: enum DboBaseObject::BitmaskT
GetObjectType() : returns ObjectTypeT
Class : DboBaseObject
Parameters:
GetTypeString(strType) : returns DboState
Class : DboBaseObject
Parameters:

---

strType: CString &
IsEquivalent(pObj) : returns int
Class : DboBaseObject
Parameters:
pObj: DboBaseObject *
GetBoundingBox() : returns CRect
Class : DboBaseObject
Parameters:
GetDBProp(name, status) : returns DBProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
GetDBProp(nNameID, status) : returns DBProp
Class : DboBaseObject
Parameters:
nNameID: UINT
status: DboState &
GetDBPropNC(name, status) : returns DBProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
GetDBPropValue(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: DboValue &
GetDBPropValue(nNameID, value) : returns DboState
Class : DboBaseObject
Parameters:
nNameID: UINT
value: DboValue &

---

GetUserPropsPermitted(status) : returns int
Class : DboBaseObject
Parameters:
status: DboState &
GetUserPropsCount(status) : returns int
Class : DboBaseObject
Parameters:
status: DboState &
GetUserProp(nNameID, status) : returns DboUserProp
Class : DboBaseObject
Parameters:
nNameID: UINT
status: DboState &
GetUserProp(name, status) : returns DboUserProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
GetUserPropNC(name, status) : returns DboUserProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
GetUserPropStringValue(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: CString &
GetUserPropStringValueNC(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: CString &

---

GetEffectivePropStringValueNC(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: CString &
GetEffectivePropStringValue(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: CString &
GetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboBaseObject
Parameters:
nNameID: UINT
value: CString &
GetSession(status) : returns DboSession
Class : DboBaseObject
Parameters:
status: DboState &
GetContainingLib() : returns DboLib
Class : DboBaseObject
Parameters:
GetDisplayProp(name, status) : returns DboDisplayProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
GetDisplayPropEx(name, status) : returns DboDisplayProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &

---

GetDisplayPropsPermitted(status) : returns int
Class : DboBaseObject
Parameters:
status: DboState &
GetName(name) : returns DboState
Class : DboBaseObject
Parameters:
name: CString &
EffectivePropsMatch(strFindWhat, bMatchCase, PatternMatcher = DboPatternMatch) : returns int
Class : DboBaseObject
Parameters:
strFindWhat: CString const &
bMatchCase: int
PatternMatcher: TPatternMatch
EffectivePropsMatch(strFindWhat, bMatchCase) : returns int
Class : DboBaseObject
Parameters:
strFindWhat: CString const &
bMatchCase: int
EffectivePropNameMatch(strFindPropName, strFindPropValue, bMatchCase, PatternMatcher =
DboPatternMatch) : returns int
Class : DboBaseObject
Parameters:
strFindPropName: CString const &
strFindPropValue: CString const &
bMatchCase: int
PatternMatcher: TPatternMatch
EffectivePropNameMatch(strFindPropName, strFindPropValue, bMatchCase) : returns int
Class : DboBaseObject
Parameters:
strFindPropName: CString const &
strFindPropValue: CString const &
bMatchCase: int
GetId(status) : returns unsigned long

---

Class : DboBaseObject
Parameters:
status: DboState &
sGetDBProp(nObjType, nNameID, status) : returns DBProp
Class : DboBaseObject
Parameters:
nObjType: enum DboBaseObject::ObjectTypeT
nNameID: UINT
status: DboState &
sGetDBProp(nObjType, csName, status) : returns DBProp
Class : DboBaseObject
Parameters:
nObjType: enum DboBaseObject::ObjectTypeT
csName: CString const &
status: DboState &
GetObjectOccurrence(pParentSchematicOcc) : returns DboOccurrence
Class : DboBaseObject
Parameters:
pParentSchematicOcc: DboInstOccurrence *
GetObjectOccurrence(DWID) : returns DboOccurrence
Class : DboBaseObject
Parameters:
DWID: DboDesignOccurrenceId const &
GetOpenDesigns(designs, status)
Class : DboBaseObject
Parameters:
designs: DboDesignList &
status: DboState &
HasPropertyThatExists(status) : returns int
Class : DboBaseObject
Parameters:
status: DboState &
GetEffectivePropValueChoices(name, choices) : returns DboState

---

Class : DboBaseObject
Parameters:
name: CString const &
choices: CStringList &
GetEffectivePropValueExists(name, bExists) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
bExists: int &
GetEffectivePropValueType(name, nType, bEditable, bDeletable) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
GetObjectOccurrences(occArr, pDesign, status, bOnlyCurrent = False)
Class : DboBaseObject
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool
GetObjectOccurrences(occArr, pDesign, status)
Class : DboBaseObject
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
GetBaseProp(nNameID, status) : returns DbBaseProp
Class : DboBaseObject
Parameters:
nNameID: UINT
status: DboState &

---

GetBaseProp(name, status) : returns DbBaseProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
GetBasePropNC(name, status) : returns DbBaseProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
GetSemanticString(str)
Class : DboBaseObject
Parameters:
str: CString &
GetSemanticID() : returns int
Class : DboBaseObject
Parameters:
GetPaint() : returns int
Class : DboBaseObject
Parameters:
GetDBPropFromObject(strName, status) : returns DBProp
Class : DboBaseObject
Parameters:
strName: CString const &
status: DboState &
GetRefCount() : returns int
Class : DboBaseObject
Parameters:
IsCurrent() : returns int
Class : DboBaseObject
Parameters:
GetTransactionCount() : returns int

---

Class : DboBaseObject
Parameters:
GetPrevState() : returns DboBaseObject
Class : DboBaseObject
Parameters:
GetNextState() : returns DboBaseObject
Class : DboBaseObject
Parameters:
GetCurrentObject(nTransCount) : returns DboBaseObject
Class : DboBaseObject
Parameters:
nTransCount: int
IsOccModified() : returns int
Class : DboBaseObject
Parameters:
GetVariantProp(strName, strVal) : returns int
Class : DboBaseObject
Parameters:
strName: CString const &
strVal: CString &
GetNextNewVariantProp(strName, strVal, bNewFound) : returns int
Class : DboBaseObject
Parameters:
strName: CString &
strVal: CString &
bNewFound: int &
IsVariantPropMapEmpty() : returns int
Class : DboBaseObject
Parameters:
GetBundleTemplateMap() : returns DboBundleTemplateMap
Class : DboBaseObject
Parameters:

---

isBundleTemplateExists() : returns bool
Class : DboBaseObject
Parameters:
IsBundleObject() : returns bool
Class : DboBaseObject
Parameters:
UpdateBundleOwner(BundleOwnerName, srcLib = "")
Class : DboBaseObject
Parameters:
BundleOwnerName: CString
srcLib: CString
UpdateBundleOwner(BundleOwnerName)
Class : DboBaseObject
Parameters:
BundleOwnerName: CString
MakeBundle(sOwner, sSourceLib, flag)
Class : DboBaseObject
Parameters:
sOwner: CString
sSourceLib: CString
flag: int
SetBundleOwner(bOwnerName, srcLib = "") : returns DboState
Class : DboBaseObject
Parameters:
bOwnerName: CString
srcLib: CString
SetBundleOwner(bOwnerName) : returns DboState
Class : DboBaseObject
Parameters:
bOwnerName: CString
GetBundleOwner() : returns DboBundle
Class : DboBaseObject

---

Parameters:
GetBundleOwnerPropName(propName, sourceLibName) : returns DboState
Class : DboBaseObject
Parameters:
propName: CString &
sourceLibName: CString &
GetBundleOwnerPropValue(propName, sourceLibName) : returns DboState
Class : DboBaseObject
Parameters:
propName: CString &
sourceLibName: CString &
StatefulCreate() : returns DboBaseObject
Class : DboBaseObject
Parameters:
MarkModified() : returns DboState
Class : DboBaseObject
Parameters:
NewDBPropsIter(status) : returns DboDBPropsIter
Class : DboBaseObject
Parameters:
status: DboState &
NewEffectivePropsIter(status) : returns DboEffectivePropsIter
Class : DboBaseObject
Parameters:
status: DboState &
NewDisplayPropsIter(status) : returns DboDisplayPropsIter
Class : DboBaseObject
Parameters:
status: DboState &
NewUserPropsIter(status) : returns DboUserPropsIter
Class : DboBaseObject
Parameters:

---

status: DboState &
SetMask(pMask)
Class : DboBaseObject
Parameters:
pMask: MaskT
SetBitmask(pBitmask)
Class : DboBaseObject
Parameters:
pBitmask: enum DboBaseObject::BitmaskT
UnsetBitmask(pBitmask)
Class : DboBaseObject
Parameters:
pBitmask: enum DboBaseObject::BitmaskT
SetName(name) : returns DboState
Class : DboBaseObject
Parameters:
name: CString &
SetObjectType(arg0) : returns DboState
Class : DboBaseObject
Parameters:
arg2: enum DboBaseObject::ObjectTypeT
DeleteUserProp(name) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
DeleteUserProps() : returns DboState
Class : DboBaseObject
Parameters:
DeleteEffectiveProp(name) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &

---

DeleteDBProp(name) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
SetPaint(bPaint = 1)
Class : DboBaseObject
Parameters:
bPaint: int
SetPaint()
Class : DboBaseObject
Parameters:
RemovePropsFromObject()
Class : DboBaseObject
Parameters:
Increment()
Class : DboBaseObject
Parameters:
Decrement()
Class : DboBaseObject
Parameters:
SetCurrent(bVal)
Class : DboBaseObject
Parameters:
bVal: int
ResetObject()
Class : DboBaseObject
Parameters:
SetTransactionCount(count)
Class : DboBaseObject
Parameters:
count: int

---

SetOccsModified(bMod)
Class : DboBaseObject
Parameters:
bMod: int
AddVariantProp(strName, strVal)
Class : DboBaseObject
Parameters:
strName: CString const &
strVal: CString const &
ClearVariantMap(bFlag = 1)
Class : DboBaseObject
Parameters:
bFlag: int
ClearVariantMap()
Class : DboBaseObject
Parameters:
SetUserPropStringValue(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: CString const &
SetEffectivePropStringValue(nNameID, value) : returns DboState
Class : DboBaseObject
Parameters:
nNameID: UINT
value: CString &
SetEffectivePropStringValue(name, value, bNewVersion = 0) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: CString const &
bNewVersion: int

---

SetEffectivePropStringValue(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: CString const &
NewDisplayProp(status, arg1, arg2, arg3, arg4, arg5) : returns DboDisplayProp
Class : DboBaseObject
Parameters:
status: DboState &
arg3: CString &
arg4: CPoint
arg5: enum DboValue::RotationT
arg6: LOGFONT &
arg7: enum DboValue::ColorT
NewUserProp(name, status) : returns DboUserProp
Class : DboBaseObject
Parameters:
name: CString const &
status: DboState &
NewUserProp(name, value, status) : returns DboUserProp
Class : DboBaseObject
Parameters:
name: CString const &
value: CString const &
status: DboState &
SetDBPropValue(name, value) : returns DboState
Class : DboBaseObject
Parameters:
name: CString const &
value: DboValue &
SetDBPropValue(nNameID, value) : returns DboState
Class : DboBaseObject
Parameters:
nNameID: UINT
value: DboValue &

---

DeleteDisplayProp(arg0) : returns DboState
Class : DboBaseObject
Parameters:
arg2: DboDisplayProp *
IsObjLocked() : returns int
Class : DboBaseObject
Parameters:
AddLockingInfo(propName, lLock, preTriggerName, postTrigerName)
Class : DboBaseObject
Parameters:
propName: CString
lLock: MaskT
preTriggerName: CString
postTrigerName: CString
IsPropertyLockable(propName) : returns bool
Class : DboBaseObject
Parameters:
propName: CString
CopyExtensions(srcExtn)
Class : DboBaseObject
Parameters:
srcExtn: DboExtensionTableHandle
GetAttributeLockingInfo(propName, lLock, preTrigger, postTrigger) : returns bool
Class : DboBaseObject
Parameters:
propName: CString
lLock: MaskT &
preTrigger: CString &
postTrigger: CString &
IsPropertyLockedForEditing(propName) : returns bool
Class : DboBaseObject
Parameters:
propName: CString

---

AddPropertyToPropertyBag(BagType, pBagName, pName, pValue)
Class : DboBaseObject
Parameters:
BagType: enum DboBaseObject::eBagType
pBagName: char const *
pName: char const *
pValue: char const *
GetPropertyBag(BagType) : returns PropBagT
Class : DboBaseObject
Parameters:
BagType: enum DboBaseObject::eBagType
RemoveBundleProperties()
Class : DboBaseObject
Parameters:
END class DboBaseObject
DboBaseObject_IsPtrDeleted(pPtr) : returns bool
Parameters:
pPtr: void *
sGetDBProp(nObjType, nNameID, status) : returns DBProp
Parameters:
nObjType: enum DboBaseObject::ObjectTypeT
nNameID: UINT
status: DboState &
DboBaseObject_sGetDBProp(nObjType, csName, status) : returns DBProp
Parameters:
nObjType: enum DboBaseObject::ObjectTypeT
csName: CString const &
status: DboState &
START class DboDBPropsIter
NextDBProp(status) : returns DBProp
Class : DboDBPropsIter

---

Parameters:
status: DboState &
Next(status) : returns DBProp
Class : DboDBPropsIter
Parameters:
status: DboState &
END class DboDBPropsIter
START class DboUserPropsIter
NextUserProp(status) : returns DboUserProp
Class : DboUserPropsIter
Parameters:
status: DboState &
Next(status) : returns DboUserProp
Class : DboUserPropsIter
Parameters:
status: DboState &
END class DboUserPropsIter
START class DboEffectivePropsIter
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboEffectivePropsIter
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboEffectivePropsIter
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &

---

bEditable: int &
bDeletable: int &
NextEffectiveProp(prop) : returns DboState
Class : DboEffectivePropsIter
Parameters:
prop: DbBaseProp *&
END class DboEffectivePropsIter
START class TBaseDboDisplayPropsIter(IterDefs):
GetType() : returns int
Class : TBaseDboDisplayPropsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboDisplayPropsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboDisplayPropsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboDisplayPropsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboDisplayPropsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboDisplayPropsIter(IterDefs):
START class DboDisplayPropsIter(TBaseDboDisplayPropsIter):

---

NextProp(status) : returns DboDisplayProp
Class : DboDisplayPropsIter(TBaseDboDisplayPropsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboDisplayPropsIter(TBaseDboDisplayPropsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboDisplayPropsIter(TBaseDboDisplayPropsIter):
Parameters:
pObject: DboDisplayProp *&
END class DboDisplayPropsIter(TBaseDboDisplayPropsIter):
DboBaseObjectToDboDeletedObject(x) : returns DboDeletedObject
Parameters:
x: DboBaseObject *
START class DboDeletedObject(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboDeletedObject(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboDeletedObject(DboBaseObject):
Parameters:
END class DboDeletedObject(DboBaseObject):
START class DboSession
CallTclAttributeTrigger(pObj, triggerName, propName, propVal)
Class : DboSession
Parameters:
pObj: DboBaseObject *
triggerName: CString

---

propName: char const *
propVal: char const *
GetDataVersion() : returns short
Class : DboSession
Parameters:
GetDesignDataVersion() : returns short
Class : DboSession
Parameters:
GetDataRelease() : returns short
Class : DboSession
Parameters:
GetInterfaceVersion() : returns short
Class : DboSession
Parameters:
GetDesign(Name, status) : returns DboDesign
Class : DboSession
Parameters:
Name: CString &
status: DboState &
GetDesignAndSchematics(Name, status) : returns DboDesign
Class : DboSession
Parameters:
Name: CString &
status: DboState &
GetOpenDesign(Name, status) : returns DboDesign
Class : DboSession
Parameters:
Name: CString &
status: DboState &
GetOpenDesigns(designs, status)
Class : DboSession
Parameters:

---

designs: DboDesignList &
status: DboState &
GetLib(Name, status) : returns DboLib
Class : DboSession
Parameters:
Name: CString &
status: DboState &
GetLibAndSchematics(Name, status) : returns DboLib
Class : DboSession
Parameters:
Name: CString &
status: DboState &
GetOpenLib(Name, status) : returns DboLib
Class : DboSession
Parameters:
Name: CString &
status: DboState &
IsLibPersistent(lib, status) : returns int
Class : DboSession
Parameters:
lib: DboLib *
status: DboState &
IsDesignPersistent(design, status) : returns int
Class : DboSession
Parameters:
design: DboDesign *
status: DboState &
GetOccByCanonicalName(strName, nType) : returns DboOccurrence
Class : DboSession
Parameters:
strName: CString const &
nType: int
GetStringPtrFromIndex(nIndex, status) : returns CString

---

Class : DboSession
Parameters:
nIndex: int
status: DboState &
GetIndexForString(str, status) : returns int
Class : DboSession
Parameters:
str: CString const &
status: DboState &
GetActiveDesign() : returns DboDesign
Class : DboSession
Parameters:
GetFlatNetNamingStrategy() : returns FlatNetNamingStrategyT
Class : DboSession
Parameters:
IsFlatNetModificationRegistrationActive() : returns bool
Class : DboSession
Parameters:
IsObjLocked() : returns int
Class : DboSession
Parameters:
NewDesignsIter(status) : returns DboSessionDesignsIter
Class : DboSession
Parameters:
status: DboState &
NewLibsIter(status) : returns DboSessionLibsIter
Class : DboSession
Parameters:
status: DboState &
SetFlatNetNamingStrategy(pStrategy)
Class : DboSession
Parameters:

---

pStrategy: enum FlatNetNamingStrategyT
CreateLib(Name, status) : returns DboLib
Class : DboSession
Parameters:
Name: CString &
status: DboState &
SaveLib(lib) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
SaveLibAs(lib, name, Replace = 0) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
name: CString &
Replace: int
SaveLibAs(lib, name) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
name: CString &
SaveLibAs(lib, nRelease, nVersion, name, Replace = 0) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
nRelease: short
nVersion: short
name: CString &
Replace: int
SaveLibAs(lib, nRelease, nVersion, name) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
nRelease: short

---

nVersion: short
name: CString &
CreateDesign(status, Name, RootName, RootType = SCHEMATIC) : returns DboDesign
Class : DboSession
Parameters:
status: DboState &
Name: CString &
RootName: CString &
RootType: enum DboBaseObject::ObjectTypeT
CreateDesign(status, Name, RootName) : returns DboDesign
Class : DboSession
Parameters:
status: DboState &
Name: CString &
RootName: CString &
CreateDesign(Name, status) : returns DboDesign
Class : DboSession
Parameters:
Name: CString &
status: DboState &
MarkAllLibForSave(lib) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
CopyLibAll(lib, name) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
name: CString &
SaveDesign(design) : returns DboState
Class : DboSession
Parameters:
design: DboDesign *

---

SaveDesignAs(design, name, Replace = 0) : returns DboState
Class : DboSession
Parameters:
design: DboDesign *
name: CString &
Replace: int
SaveDesignAs(design, name) : returns DboState
Class : DboSession
Parameters:
design: DboDesign *
name: CString &
SaveDesignAs(design, nRelease, nVersion, name, Replace = 0) : returns DboState
Class : DboSession
Parameters:
design: DboDesign *
nRelease: short
nVersion: short
name: CString &
Replace: int
SaveDesignAs(design, nRelease, nVersion, name) : returns DboState
Class : DboSession
Parameters:
design: DboDesign *
nRelease: short
nVersion: short
name: CString &
RemoveLib(lib) : returns DboState
Class : DboSession
Parameters:
lib: DboLib *
RemoveDesign(design) : returns DboState
Class : DboSession
Parameters:
design: DboDesign *

---

FindExternalDesignsToBeRemoved(pDsn, pDesList) : returns bool
Class : DboSession
Parameters:
pDsn: DboDesign *
pDesList: std::vector< DboDesign * > &
END class DboSession
DboSession_CallTclAttributeTrigger(pObj, triggerName, propName, propVal)
Parameters:
pObj: DboBaseObject *
triggerName: CString
propName: char const *
propVal: char const *
START class TBaseDboSessionLibsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSessionLibsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSessionLibsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSessionLibsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSessionLibsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSessionLibsIter(IterDefs):
Parameters:
status: DboState &

---

END class TBaseDboSessionLibsIter(IterDefs):
START class DboSessionLibsIter(TBaseDboSessionLibsIter):
NextLib(status) : returns DboLib
Class : DboSessionLibsIter(TBaseDboSessionLibsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSessionLibsIter(TBaseDboSessionLibsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboSessionLibsIter(TBaseDboSessionLibsIter):
Parameters:
pObject: DboLib *&
END class DboSessionLibsIter(TBaseDboSessionLibsIter):
START class TBaseDboSessionDesignsIter(IterDefs):
GetType() : returns int
Class : TBaseDboSessionDesignsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboSessionDesignsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboSessionDesignsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboSessionDesignsIter(IterDefs):
Parameters:

---

flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboSessionDesignsIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboSessionDesignsIter(IterDefs):
START class DboSessionDesignsIter(TBaseDboSessionDesignsIter):
NextDesign(status) : returns DboDesign
Class : DboSessionDesignsIter(TBaseDboSessionDesignsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSessionDesignsIter(TBaseDboSessionDesignsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboSessionDesignsIter(TBaseDboSessionDesignsIter):
Parameters:
pObject: DboDesign *&
END class DboSessionDesignsIter(TBaseDboSessionDesignsIter):
START class DbBaseProp
GetName(Name) : returns DboState
Class : DbBaseProp
Parameters:
Name: CString &
GetType(status) : returns ValueType
Class : DbBaseProp
Parameters:
status: DboState &

---

GetStringValue(obj, Value, bFromProp = 0) : returns DboState
Class : DbBaseProp
Parameters:
obj: DboBaseObject *
Value: CString &
bFromProp: int
GetStringValue(obj, Value) : returns DboState
Class : DbBaseProp
Parameters:
obj: DboBaseObject *
Value: CString &
IsEditable() : returns int
Class : DbBaseProp
Parameters:
IsDeletable() : returns int
Class : DbBaseProp
Parameters:
IsCurrent() : returns int
Class : DbBaseProp
Parameters:
GetTransactionCount() : returns int
Class : DbBaseProp
Parameters:
GetPrevState() : returns DbBaseProp
Class : DbBaseProp
Parameters:
GetNextState() : returns DbBaseProp
Class : DbBaseProp
Parameters:
GetCurrentObject() : returns DbBaseProp
Class : DbBaseProp

---

Parameters:
SetCurrent(bVal)
Class : DbBaseProp
Parameters:
bVal: int
ResetObject()
Class : DbBaseProp
Parameters:
SetTransactionCount(count)
Class : DbBaseProp
Parameters:
count: int
END class DbBaseProp
DbBasePropToDbDelProp(x) : returns DbDelProp
Parameters:
x: DbBaseProp *
START class DbDelProp(DbBaseProp):
GetName(Name) : returns DboState
Class : DbDelProp(DbBaseProp):
Parameters:
Name: CString &
GetStringValue(obj, Value, bFromProp = 0) : returns DboState
Class : DbDelProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
Value: CString &
bFromProp: int
GetStringValue(obj, Value) : returns DboState
Class : DbDelProp(DbBaseProp):
Parameters:
obj: DboBaseObject *

---

Value: CString &
GetType(status) : returns ValueType
Class : DbDelProp(DbBaseProp):
Parameters:
status: DboState &
IsEditable() : returns int
Class : DbDelProp(DbBaseProp):
Parameters:
IsDeletable() : returns int
Class : DbDelProp(DbBaseProp):
Parameters:
END class DbDelProp(DbBaseProp):
DbBasePropToDboUserProp(x) : returns DboUserProp
Parameters:
x: DbBaseProp *
START class DboUserProp(DbBaseProp):
GetOwner() : returns DboBaseObject
Class : DboUserProp(DbBaseProp):
Parameters:
GetName(name) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
name: CString &
GetStringValue(value, bFromProp, bSetFlag) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
value: CString &
bFromProp: int
bSetFlag: int
GetStringValue(value, bFromProp = 0) : returns DboState

---

Class : DboUserProp(DbBaseProp):
Parameters:
value: CString &
bFromProp: int
GetStringValue(value) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
value: CString &
GetStringValue(obj, Value, bFromProp = 0) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
Value: CString &
bFromProp: int
GetStringValue(obj, Value) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
Value: CString &
GetType(status) : returns ValueType
Class : DboUserProp(DbBaseProp):
Parameters:
status: DboState &
IsEditable() : returns int
Class : DboUserProp(DbBaseProp):
Parameters:
GetNext() : returns DboUserProp
Class : DboUserProp(DbBaseProp):
Parameters:
IsDeletable() : returns int
Class : DboUserProp(DbBaseProp):
IsDeletable() : returns int

---

Class : DboUserProp(DbBaseProp):
Parameters:
SetValue(val, bFromProp = 0) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
val: DboValue &
bFromProp: int
SetValue(val) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
val: DboValue &
SetStringValue(val, bFromProp = 0) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
val: CString const &
bFromProp: int
SetStringValue(val) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
val: CString const &
ShadowSetStringValue(val) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
val: CString const &
DeleteValue() : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
SetName(name) : returns DboState
Class : DboUserProp(DbBaseProp):
Parameters:
name: CString &
END class DboUserProp(DbBaseProp):