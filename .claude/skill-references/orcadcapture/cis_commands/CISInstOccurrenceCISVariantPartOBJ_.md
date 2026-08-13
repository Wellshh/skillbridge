# Class: CISInstOccurrence(CISVariantPartOBJ):

START class CISInstOccurrence(CISVariantPartOBJ):
PropsDiffer(pCISOcc1, pCISOcc2, FieldNames) : returns int
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pCISOcc1: CISInstOccurrence *
pCISOcc2: CISInstOccurrence *
FieldNames: CStringArray const &
GetPartProp(PropName) : returns CString
Class : CISInstOccurrence(CISVariantPartOBJ):

---

Parameters:
PropName: CString const &
GetPartProps(PartProps, CheckForActiveVariant = 1) : returns int
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
PartProps: CPartProp &
CheckForActiveVariant: int
GetPartProps(PartProps) : returns int
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
PartProps: CPartProp &
GetPartRefDes() : returns CRefDes
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
GetPartRefPrefix() : returns CString
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
GetPartRef() : returns CString
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
SetOwningCISPartInst(pCISPartInst)
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pCISPartInst: CISPartInst *
GetOwningCISPartInst() : returns CISPartInst
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
GetStuffed() : returns UINT
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
SetCaptureDboObject(pDboObject)

---

Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pDboObject: DboBaseObject *
GetCaptureDboObject() : returns DboBaseObject
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
SaveFile(pFile) : returns DboState
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pFile: CFile *
ReadFile(pFile) : returns DboState
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pFile: CFile *
Save() : returns DboState
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
Read() : returns DboState
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
SetPropEx(PropName, PropContents)
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
PropName: CString const &
PropContents: CString const &
HasActiveVariantproperty(ActiveVariant = CString("")) : returns int
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
ActiveVariant: CString &
HasActiveVariantproperty() : returns int
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:

---

ReadFromExtension(pVariantName, pPropName, pPropValue)
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pVariantName: CString const &
pPropName: CString const &
pPropValue: CString const &
sAddPropToPropArray(pArray, pPropName, pPropValue, pInstOcc)
Class : CISInstOccurrence(CISVariantPartOBJ):
Parameters:
pArray: QPropertyArray *
pPropName: CString const &
pPropValue: CString const &
pInstOcc: CISInstOccurrence *
END class CISInstOccurrence(CISVariantPartOBJ):
CISInstOccurrence_PropsDiffer(pCISOcc1, pCISOcc2, FieldNames) : returns int
Parameters:
pCISOcc1: CISInstOccurrence *
pCISOcc2: CISInstOccurrence *
FieldNames: CStringArray const &
CISInstOccurrence_sAddPropToPropArray(pArray, pPropName, pPropValue, pInstOcc)
Parameters:
pArray: QPropertyArray *
pPropName: CString const &
pPropValue: CString const &
pInstOcc: CISInstOccurrence *
START class StatusInfo
END class StatusInfo
START class CAmbiguousParts
DeleteAmbiguousMapForBOM(BOMName) : returns int
Class : CAmbiguousParts
Parameters: