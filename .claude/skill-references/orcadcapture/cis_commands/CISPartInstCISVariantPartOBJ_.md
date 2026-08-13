# Class: CISPartInst(CISVariantPartOBJ):

START class CISPartInst(CISVariantPartOBJ):
SetVariantProperty(PropertyName, PropertyValue, VariantName)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PropertyName: CString const &
PropertyValue: CString const &
VariantName: CString const &
SetVariantProperty(pPropArray, VariantName = CString(""))
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pPropArray: QPropertyArray *&
VariantName: CString const &
SetVariantProperty(pPropArray)

---

Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pPropArray: QPropertyArray *&
GetPartRefPrefix() : returns CString
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetPartRef() : returns CString
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetPartRefDes() : returns CRefDes
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetEffectiveRefDes(EffectiveRefDes)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
EffectiveRefDes: CString &
Save(pFile) : returns DboState
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pFile: CFile *
Read(pFile) : returns DboState
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pFile: CFile *
DeleteUserProp(PropName) : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PropName: CString const &
MakePropInvisible(propName) : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
propName: CString const &

---

MakePropVisible(propName) : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
propName: CString const &
SetProp(PropName, PropContents, CreatePropIfNotPresent = 1,
Class : CISPartInst(CISVariantPartOBJ):
CheckForActiveVariant = 1)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PropName: CString const &
PropContents: CString const &
CreatePropIfNotPresent: int
CheckForActiveVariant: int
SetProp(PropName, PropContents, CreatePropIfNotPresent = 1)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PropName: CString const &
PropContents: CString const &
CreatePropIfNotPresent: int
SetProp(PropName, PropContents)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PropName: CString const &
PropContents: CString const &
RenameUserProp(OldPropName, NewPropName) : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
OldPropName: CString const &
NewPropName: CString const &
GetOccurrencesList(PtrArray)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PtrArray: CPtrArray &

---

GetOccurrencesList()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetOccurrences() : returns CPtrArray
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
SetCaptureDboObject(pDboObject)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pDboObject: DboBaseObject *
GetCaptureDboObject() : returns DboBaseObject
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
ReplacePartInst(PkgName, pLibPart, pDevice, LaunchedFromPartMgr, bPreserveRef = 0) : returns
DboPlacedInst
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PkgName: CString &
pLibPart: DboLibPart *
pDevice: DboDevice *
LaunchedFromPartMgr: int
bPreserveRef: int
ReplacePartInst(PkgName, pLibPart, pDevice, LaunchedFromPartMgr) : returns DboPlacedInst
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PkgName: CString &
pLibPart: DboLibPart *
pDevice: DboDevice *
LaunchedFromPartMgr: int
ShadowoutPartInst() : returns DboState
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
SetOwningDesign(pDesign)

---

Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pDesign: CISDesign *
CleanUpDeletedOCCurrences()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
Delete()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetOCCCount() : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetDeletedOCCCount() : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetOwniningPageID() : returns UINT
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetCoreDesignProp(PropName) : returns CString
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PropName: CString const &
RestoreCaptureProps(pPropertyArray)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pPropertyArray: QPropertyArray *
RestoreCaptureProps()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
MarkEdit()
Class : CISPartInst(CISVariantPartOBJ):

---

Parameters:
IsExternal() : returns bool
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
IsLinkable() : returns bool
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
AddOccIdToSelection(nId)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
nId: UINT
SetLinkAlways()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetLinkAlways() : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
IsOccIdInSelection(nId) : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
nId: UINT
SetLinked(bVal)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
bVal: int
GetLinked() : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
ResetLinkSetting()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:

---

DeleteVariant(VariantName = CString(""))
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
VariantName: CString const &
DeleteVariant()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
SetStuff(flag)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
flag: UINT
ApplyActiveVariantPropsToCaptureParts(pPropertyArray) : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pPropertyArray: QPropertyArray *
SetPropEx(PropName, PropContents)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
PropName: CString const &
PropContents: CString const &
ApplyActiveVariantPropsToCapturePartsEx() : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
StuffOcc(OccId, bStuff = 0)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
OccId: UINT
bStuff: int
StuffOcc(OccId)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
OccId: UINT

---

ResetVariantSettings()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
RestoreCapturePropsEx()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
IncrOCount()
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
GetOCount() : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
DetachPart(pCISInstOcc)
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
pCISInstOcc: CISVariantPartOBJ *
HasActiveVariantpropertyForOcc(arg0) : returns int
Class : CISPartInst(CISVariantPartOBJ):
Parameters:
arg2: CISInstOccurrence *
END class CISPartInst(CISVariantPartOBJ):
START class CISInstOccurrence(CISVariantPartOBJ):
PropsDiffer(pCISOcc1, pCISOcc2, FieldNames) : returns int
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pCISOcc1: CISInstOccurrence *
pCISOcc2: CISInstOccurrence *
FieldNames: CStringArray const &
GetPartProp(PropName) : returns CString
Class : CISInstOccurrence(CISVariantPartOBJ):