# Class: CISBase

START class CISBase
Delete()
Class : CISBase
Parameters:
UnDelete()
Class : CISBase
Parameters:

---

IsDeleted() : returns int
Class : CISBase
Parameters:
GetCaptureObjectId() : returns int
Class : CISBase
Parameters:
SetOwner(pOwner)
Class : CISBase
Parameters:
pOwner: CISBase *
GetOwner() : returns CISBase
Class : CISBase
Parameters:
MarkModified(MarkDesign = 1)
Class : CISBase
Parameters:
MarkDesign: int
MarkModified()
Class : CISBase
Parameters:
SetParent(pParent)
Class : CISBase
Parameters:
pParent: CISBase *
GetParent() : returns CISBase
Class : CISBase
Parameters:
GetPartProps(PartProps, CheckForActiveVariant = 1) : returns int
Class : CISBase
Parameters:
PartProps: CPartProp &

---

CheckForActiveVariant: int
GetPartProps(PartProps) : returns int
Class : CISBase
Parameters:
PartProps: CPartProp &
GetCoreDesignProp(PropName) : returns CString
Class : CISBase
Parameters:
PropName: CString const &
GetDisplayProp(PropName) : returns DboDisplayProp
Class : CISBase
Parameters:
PropName: CString const
MakePropInvisible(propName) : returns int
Class : CISBase
Parameters:
propName: CString const &
CloneDisplayPropPosition(pDisplayPropToClone, NewPosition) : returns int
Class : CISBase
Parameters:
pDisplayPropToClone: DboDisplayProp *
NewPosition: CPoint &
CloneDisplayProp(pDisplayPropToClone, PropName, pNewDisplayProp) : returns int
Class : CISBase
Parameters:
pDisplayPropToClone: DboDisplayProp *
PropName: CString const &
pNewDisplayProp: DboDisplayProp *
MakePropVisible(propName) : returns int
Class : CISBase
Parameters:
propName: CString const &

---

DeleteUserProp(PropName) : returns int
Class : CISBase
Parameters:
PropName: CString const &
RenameUserProp(OldPropName, NewPropName) : returns int
Class : CISBase
Parameters:
OldPropName: CString const &
NewPropName: CString const &
SetProp(PropName, PropContents, CreatePropIfNotPresent = 1,
Class : CISBase
CheckForActiveVariant = 1)
Class : CISBase
Parameters:
PropName: CString const &
PropContents: CString const &
CreatePropIfNotPresent: int
CheckForActiveVariant: int
SetProp(PropName, PropContents, CreatePropIfNotPresent = 1)
Class : CISBase
Parameters:
PropName: CString const &
PropContents: CString const &
CreatePropIfNotPresent: int
SetProp(PropName, PropContents)
Class : CISBase
Parameters:
PropName: CString const &
PropContents: CString const &
SetPropEx(PropName, PropContents)
Class : CISBase
Parameters:
PropName: CString const &
PropContents: CString const &

---

UserPropExists(PropName) : returns int
Class : CISBase
Parameters:
PropName: CString const &
IsDbProp(PropName) : returns int
Class : CISBase
Parameters:
PropName: CString const &
PropEmpty(propName) : returns int
Class : CISBase
Parameters:
propName: CString const &
GetPartValue() : returns CString
Class : CISBase
Parameters:
PropExists(PropName) : returns int
Class : CISBase
Parameters:
PropName: CString const &
SetCaptureDboObject(pDboObject)
Class : CISBase
Parameters:
pDboObject: DboBaseObject *
GetCaptureDboObject() : returns DboBaseObject
Class : CISBase
Parameters:
DbPropExists(PropName) : returns int
Class : CISBase
Parameters:
PropName: CString const &
PropExistsOnObject(PropName) : returns int
Class : CISBase

---

Parameters:
PropName: CString const &
END class CISBase
START class CBOMODBCDataCacheItem
END class CBOMODBCDataCacheItem
START class CISDesignDataCacheScope
GetCISInstOccurrenceCopy(pDboInstOcc) : returns CISInstOccurrence
Class : CISDesignDataCacheScope
Parameters:
pDboInstOcc: DboInstOccurrence *
SetCISInstOccurrenceCopy(pDboInstOcc, pCISInstOcc) : returns CISInstOccurrence
Class : CISDesignDataCacheScope
Parameters:
pDboInstOcc: DboInstOccurrence *
pCISInstOcc: CISInstOccurrence *
GetDesignIds(pDesignIds) : returns bool
Class : CISDesignDataCacheScope
Parameters:
pDesignIds: CUIntArray &
AddDesignId(pDesignId)
Class : CISDesignDataCacheScope
Parameters:
pDesignId: unsigned long
SetDesignIdsFilled()
Class : CISDesignDataCacheScope
Parameters:
SetDeleteDbCacheFun(aPf)
Class : CISDesignDataCacheScope
Parameters:
aPf: PFN_DeleteDBCacheItem