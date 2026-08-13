# Class: CISPage(CISBase):

START class CISPage(CISBase):
MarkModified(MarkDesign = 1)
Class : CISPage(CISBase):
Parameters:
MarkDesign: int
MarkModified()
Class : CISPage(CISBase):
Parameters:
AddPartInst(pCISPartInst) : returns CISPartInst
Class : CISPage(CISBase):
Parameters:
pCISPartInst: CISPartInst *
AddPartInst(pPartInst) : returns CISPartInst
Class : CISPage(CISBase):
Parameters:
pPartInst: DboPartInst *
AddToDesignHeierarchy(pCISPartInst) : returns int
Class : CISPage(CISBase):
Parameters:

---

pCISPartInst: CISPartInst *
SavePage(pFile) : returns DboState
Class : CISPage(CISBase):
Parameters:
pFile: CFile *
Read(pFile) : returns DboState
Class : CISPage(CISBase):
Parameters:
pFile: CFile *
UpdateHeierarchy()
Class : CISPage(CISBase):
Parameters:
GetVariantPart(pPartInst) : returns CISPartInst
Class : CISPage(CISBase):
Parameters:
pPartInst: DboPartInst *
DetachPart(pCISPart)
Class : CISPage(CISBase):
Parameters:
pCISPart: CISVariantPartOBJ *
ApplyActiveVariantPropsToCaptureParts() : returns int
Class : CISPage(CISBase):
Parameters:
ApplyCoreDesignPropsToCaptureParts()
Class : CISPage(CISBase):
Parameters:
ApplyTitleBlockValue(VariantNameValue, bWysiwyg = 1)
Class : CISPage(CISBase):
Parameters:
VariantNameValue: CString const &
bWysiwyg: int

---

ApplyTitleBlockValue(VariantNameValue)
Class : CISPage(CISBase):
Parameters:
VariantNameValue: CString const &
RestoreTitleBlockValue()
Class : CISPage(CISBase):
Parameters:
RestoreCaptureProps()
Class : CISPage(CISBase):
Parameters:
RestoreCoreDesignCaptureProps()
Class : CISPage(CISBase):
Parameters:
GetTitleBlock(status) : returns DboTitleBlock
Class : CISPage(CISBase):
Parameters:
status: DboState &
GetTitleBlockId(status) : returns unsigned long
Class : CISPage(CISBase):
Parameters:
status: DboState &
ProcessPageEdit(pCISDesign, PageEditsArray, CheckAll)
Class : CISPage(CISBase):
Parameters:
pCISDesign: CISDesign *
PageEditsArray: CUIntArray const &
CheckAll: int
ProcessPageEdits(pCISDesign)
Class : CISPage(CISBase):
Parameters:
pCISDesign: CISDesign *
GetPart(index, LastReadInTime) : returns CISPartInst

---

Class : CISPage(CISBase):
Parameters:
index: int &
LastReadInTime: CTime const &
GetPart(index) : returns CISPartInst
Class : CISPage(CISBase):
Parameters:
index: int &
GetCISPartInst(pPartInst) : returns CISPartInst
Class : CISPage(CISBase):
Parameters:
pPartInst: DboPartInst *
DeleteVariant(VariantNames)
Class : CISPage(CISBase):
Parameters:
VariantNames: CSStringArray const &
RenameVariant(OldVariantNames, NewVariantNames)
Class : CISPage(CISBase):
Parameters:
OldVariantNames: CSStringArray const &
NewVariantNames: CSStringArray const &
SetName(Name)
Class : CISPage(CISBase):
Parameters:
Name: CString const &
GetName(Name)
Class : CISPage(CISBase):
Parameters:
Name: CString &
SetCaptureDboObject(pDboObject)
Class : CISPage(CISBase):
Parameters:
pDboObject: DboBaseObject *

---

GetCaptureDboObject() : returns DboBaseObject
Class : CISPage(CISBase):
Parameters:
IsPageOfId(id) : returns int
Class : CISPage(CISBase):
Parameters:
id: UINT
Delete()
Class : CISPage(CISBase):
Parameters:
GetDisplayedTitleBlockProps(TitleBlockMap) : returns int
Class : CISPage(CISBase):
Parameters:
TitleBlockMap: CMapStringToString &
GetTitleBlockInfo(PageNum) : returns int
Class : CISPage(CISBase):
Parameters:
PageNum: int &
END class CISPage(CISBase):
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