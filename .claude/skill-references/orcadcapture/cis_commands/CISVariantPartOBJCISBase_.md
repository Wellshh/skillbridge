# Class: CISVariantPartOBJ(CISBase):

START class CISVariantPartOBJ(CISBase):
DeleteOccurStatus(PartId, strVariantName)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PartId: UINT
strVariantName: CString
Delete()
Class : CISVariantPartOBJ(CISBase):
Parameters:
Old()
Class : CISVariantPartOBJ(CISBase):

---

Parameters:
New()
Class : CISVariantPartOBJ(CISBase):
Parameters:
DeleteVariant(VariantName = CString(""))
Class : CISVariantPartOBJ(CISBase):
Parameters:
VariantName: CString const &
DeleteVariant()
Class : CISVariantPartOBJ(CISBase):
Parameters:
RenameVariant(OldVariantname, NewVariantName)
Class : CISVariantPartOBJ(CISBase):
Parameters:
OldVariantname: CString const &
NewVariantName: CString const &
SetVariantProperty(PropertyName, PropertyValue, VariantName = CString(""))
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropertyName: CString const &
PropertyValue: CString const &
VariantName: CString const &
SetVariantProperty(PropertyName, PropertyValue)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropertyName: CString const &
PropertyValue: CString const &
SetVariantProperty(pPropArray, VariantName = CString(""))
Class : CISVariantPartOBJ(CISBase):
Parameters:
pPropArray: QPropertyArray *&
VariantName: CString const &

---

SetVariantProperty(pPropArray)
Class : CISVariantPartOBJ(CISBase):
Parameters:
pPropArray: QPropertyArray *&
DeleteVariantProperty(PropertyName, VariantName)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropertyName: CString const &
VariantName: CString const &
SetOwningDesign(pDesign)
Class : CISVariantPartOBJ(CISBase):
Parameters:
pDesign: CISDesign *
GetOwningDesign() : returns CISDesign
Class : CISVariantPartOBJ(CISBase):
Parameters:
SetProp(PropName, PropContents, CreatePropIfNotPresent = 1,
Class : CISVariantPartOBJ(CISBase):
CheckForActiveVariant = 1)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropName: CString const &
PropContents: CString const &
CreatePropIfNotPresent: int
CheckForActiveVariant: int
SetProp(PropName, PropContents, CreatePropIfNotPresent = 1)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropName: CString const &
PropContents: CString const &
CreatePropIfNotPresent: int
SetProp(PropName, PropContents)
Class : CISVariantPartOBJ(CISBase):
Parameters:

---

PropName: CString const &
PropContents: CString const &
GetVariantProperty(PropertyName, PropValue, VariantName = CString("")) : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropertyName: CString const &
PropValue: CString &
VariantName: CString const &
GetVariantProperty(PropertyName, PropValue) : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropertyName: CString const &
PropValue: CString &
GetVariantProperty(VariantName = CString("")) : returns QPropertyArray
Class : CISVariantPartOBJ(CISBase):
Parameters:
VariantName: CString const &
GetVariantProperty() : returns QPropertyArray
Class : CISVariantPartOBJ(CISBase):
Parameters:
GetPartProps(PartPropsGetPartProps, CheckForActiveVariant = 1) : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
PartPropsGetPartProps: CPartProp &
CheckForActiveVariant: int
GetPartProps(PartPropsGetPartProps) : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
PartPropsGetPartProps: CPartProp &
GetPartProp(PropName) : returns CString
Class : CISVariantPartOBJ(CISBase):
Parameters:
PropName: CString const &

---

HasActiveVariantproperty(ActiveVariant = CString("")) : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
ActiveVariant: CString &
HasActiveVariantproperty() : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
GetStuffed() : returns UINT
Class : CISVariantPartOBJ(CISBase):
Parameters:
SetStuffed(b)
Class : CISVariantPartOBJ(CISBase):
Parameters:
b: UINT
ApplyActiveVariantPropsToCaptureParts() : returns int
Class : CISVariantPartOBJ(CISBase):
ApplyActiveVariantPropsToCaptureParts(pPropertyArray) : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
pPropertyArray: QPropertyArray *
ApplyActiveVariantPropsToCapturePartsEx() : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
RestoreCapturePropsEx()
Class : CISVariantPartOBJ(CISBase):
Parameters:
ApplyCoreDesignPropsToCaptureParts()
Class : CISVariantPartOBJ(CISBase):
Parameters:
RestoreCoreDesignCaptureProps()

---

Class : CISVariantPartOBJ(CISBase):
Parameters:
GetLastUpdatedTime() : returns CTime
Class : CISVariantPartOBJ(CISBase):
Parameters:
SetUpdatedTime()
Class : CISVariantPartOBJ(CISBase):
Parameters:
TempStatus()
Class : CISVariantPartOBJ(CISBase):
Parameters:
UndoTempStatus()
Class : CISVariantPartOBJ(CISBase):
Parameters:
IsTempStatus() : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
IsNew() : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
GetPartRefDes() : returns CRefDes
Class : CISVariantPartOBJ(CISBase):
Parameters:
GetPartRef() : returns CString
Class : CISVariantPartOBJ(CISBase):
Parameters:
HasPartRefChanged() : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
SetCaptureDboObject(pDboObject)

---

Class : CISVariantPartOBJ(CISBase):
Parameters:
pDboObject: DboBaseObject *
GetCaptureDboObject() : returns DboBaseObject
Class : CISVariantPartOBJ(CISBase):
Parameters:
GetRefDesString(RefDesStr)
Class : CISVariantPartOBJ(CISBase):
Parameters:
RefDesStr: CString &
CanTransferFootprintProperty(FootprintFieldName, FootprintFieldValue, PartRef,
CoreFootprintValue,
Class : CISVariantPartOBJ(CISBase):
rVariantName) : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
FootprintFieldName: CString const &
FootprintFieldValue: CString const &
PartRef: CString &
CoreFootprintValue: CString &
rVariantName: CString &
SaveCaptureProperties()
Class : CISVariantPartOBJ(CISBase):
Parameters:
RestoreCaptureProps(pPropertyArray)
Class : CISVariantPartOBJ(CISBase):
Parameters:
pPropertyArray: QPropertyArray *
RestoreCaptureProps()
Class : CISVariantPartOBJ(CISBase):
Parameters:
GetCaptureObjectId() : returns int
Class : CISVariantPartOBJ(CISBase):

---

Parameters:
SetStuff(flag)
Class : CISVariantPartOBJ(CISBase):
Parameters:
flag: UINT
GetStuff() : returns UINT
Class : CISVariantPartOBJ(CISBase):
Parameters:
SetPartStatus(l_strStatus, SetCore = 0)
Class : CISVariantPartOBJ(CISBase):
Parameters:
l_strStatus: CString &
SetCore: int
SetPartStatus(l_strStatus)
Class : CISVariantPartOBJ(CISBase):
Parameters:
l_strStatus: CString &
GetPartStatus() : returns CString
Class : CISVariantPartOBJ(CISBase):
Parameters:
GetOccStatus(PartId, Status, VariantName = "")
Class : CISVariantPartOBJ(CISBase):
Parameters:
PartId: UINT
Status: CString &
VariantName: CString
GetOccStatus(PartId, Status)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PartId: UINT
Status: CString &
SetOccStatus(PartId, Status)

---

Class : CISVariantPartOBJ(CISBase):
Parameters:
PartId: UINT
Status: CString
SetDbName(PartId, TableName)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PartId: UINT
TableName: CString
GetDbName(PartId, TableName, VariantName)
Class : CISVariantPartOBJ(CISBase):
Parameters:
PartId: UINT
TableName: CString &
VariantName: CString
IsActiveVariant() : returns int
Class : CISVariantPartOBJ(CISBase):
Parameters:
END class CISVariantPartOBJ(CISBase):
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