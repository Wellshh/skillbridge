# Class: CISSchematic(CISBase):

CISDesign_IsDeletedOccurrence(pDboInstOccurrence, partinst, pDesign) : returns int
Parameters:
pDboInstOccurrence: DboInstOccurrence *
partinst: DboPartInst *
pDesign: DboDesign *
CISDesign_FindInt(Array, ElementToFind) : returns int
Parameters:
Array: CUIntArray const &
ElementToFind: UINT
CISDesign_SetNotStuffedString(NotStuffedString)
Parameters:
NotStuffedString: CString const &
CISDesign_SetPartNumberPropertyName(PartNumberName)
Parameters:
PartNumberName: CString const &
START class CISSchematic(CISBase):
AddToDesignHeierarchy(pCISPartInst) : returns CISPage
Class : CISSchematic(CISBase):
Parameters:
pCISPartInst: CISVariantPartOBJ *
Save(pLibStorage) : returns DboState
Class : CISSchematic(CISBase):
Parameters:
pLibStorage: IStorage *
Read(pLibStorage) : returns DboState
Class : CISSchematic(CISBase):
Parameters:
pLibStorage: IStorage *
MarkModified(MarkDesign = 1)
Class : CISSchematic(CISBase):
Parameters:
MarkDesign: int

---

MarkModified()
Class : CISSchematic(CISBase):
Parameters:
UpdateHeierarchy()
Class : CISSchematic(CISBase):
Parameters:
GetVariantPart(pPartInst) : returns CISPartInst
Class : CISSchematic(CISBase):
Parameters:
pPartInst: DboPartInst *
ApplyActiveVariantPropsToCaptureParts(PageId = 0) : returns int
Class : CISSchematic(CISBase):
Parameters:
PageId: UINT
ApplyActiveVariantPropsToCaptureParts() : returns int
Class : CISSchematic(CISBase):
Parameters:
ApplyCoreDesignPropsToCaptureParts(PageId = 0) : returns int
Class : CISSchematic(CISBase):
Parameters:
PageId: UINT
ApplyCoreDesignPropsToCaptureParts() : returns int
Class : CISSchematic(CISBase):
Parameters:
ApplyTitleBlockValue(VariantNameString, PageId = 0, bWysiwyg = 1) : returns int
Class : CISSchematic(CISBase):
Parameters:
VariantNameString: CString const &
PageId: UINT
bWysiwyg: int
ApplyTitleBlockValue(VariantNameString, PageId = 0) : returns int

---

Class : CISSchematic(CISBase):
Parameters:
VariantNameString: CString const &
PageId: UINT
ApplyTitleBlockValue(VariantNameString) : returns int
Class : CISSchematic(CISBase):
Parameters:
VariantNameString: CString const &
RestoreTitleBlockValue(PageId = 0) : returns int
Class : CISSchematic(CISBase):
Parameters:
PageId: UINT
RestoreTitleBlockValue() : returns int
Class : CISSchematic(CISBase):
Parameters:
RestoreCaptureProps(PageId = 0) : returns int
Class : CISSchematic(CISBase):
Parameters:
PageId: UINT
RestoreCaptureProps() : returns int
Class : CISSchematic(CISBase):
Parameters:
RestoreCoreDesignCaptureProps(PageId = 0) : returns int
Class : CISSchematic(CISBase):
Parameters:
PageId: UINT
RestoreCoreDesignCaptureProps() : returns int
Class : CISSchematic(CISBase):
Parameters:
ProcessDesignEdit(PageEditsArray)
Class : CISSchematic(CISBase):
Parameters:

---

PageEditsArray: CUIntArray &
ProcessPageEdit(pCISDesign, PageEditsArray, CheckAll)
Class : CISSchematic(CISBase):
Parameters:
pCISDesign: CISDesign *
PageEditsArray: CUIntArray const &
CheckAll: int
RefreshPages(PageEditsArray)
Class : CISSchematic(CISBase):
Parameters:
PageEditsArray: CUIntArray &
RenameScheamticPage(OldName, NewName)
Class : CISSchematic(CISBase):
Parameters:
OldName: CString const &
NewName: CString const &
SetName(Name)
Class : CISSchematic(CISBase):
Parameters:
Name: CString const &
GetName(Name)
Class : CISSchematic(CISBase):
Parameters:
Name: CString &
SetCaptureDboObject(pDboObject)
Class : CISSchematic(CISBase):
Parameters:
pDboObject: DboBaseObject *
GetCaptureDboObject() : returns DboBaseObject
Class : CISSchematic(CISBase):
Parameters:
GetPage(index) : returns CISPage

---

Class : CISSchematic(CISBase):
Parameters:
index: int &
GetPage(DboPageName) : returns CISPage
Class : CISSchematic(CISBase):
Parameters:
DboPageName: CString const &
GetCISPartInst(pPartInst) : returns CISPartInst
Class : CISSchematic(CISBase):
Parameters:
pPartInst: DboPartInst *
DeleteVariant(VariantNames)
Class : CISSchematic(CISBase):
Parameters:
VariantNames: CSStringArray const &
RenameVariant(OldVariantNames, NewVariantNames)
Class : CISSchematic(CISBase):
Parameters:
OldVariantNames: CSStringArray const &
NewVariantNames: CSStringArray const &
Delete()
Class : CISSchematic(CISBase):
Parameters:
GetDisplayedTitleBlockProps(TitleBlockMap)
Class : CISSchematic(CISBase):
Parameters:
TitleBlockMap: CMapStringToString &
GetFromOccurrenceMap(nId) : returns CISInstOccurrence
Class : CISSchematic(CISBase):
Parameters:
nId: unsigned long
AddToOccurrenceMap(pInstOcc)

---

Class : CISSchematic(CISBase):
Parameters:
pInstOcc: CISInstOccurrence *
DetachPart(pCISInstOcc)
Class : CISSchematic(CISBase):
Parameters:
pCISInstOcc: CISVariantPartOBJ *
ReadFromExtension(arg0)
Class : CISSchematic(CISBase):
Parameters:
arg2: DboInstOccurrence *
END class CISSchematic(CISBase):
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