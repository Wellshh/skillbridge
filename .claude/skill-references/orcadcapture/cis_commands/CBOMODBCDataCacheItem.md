# Class: CBOMODBCDataCacheItem

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

---

GetDbCacheItem(key) : returns CBOMODBCDataCacheItem
Class : CISDesignDataCacheScope
Parameters:
key: CString const &
SetDbCacheItem(key, aCacheItem)
Class : CISDesignDataCacheScope
Parameters:
key: CString const &
aCacheItem: CBOMODBCDataCacheItem *
sGetEnableCache() : returns int
Class : CISDesignDataCacheScope
END class CISDesignDataCacheScope
CISDesignDataCacheScope_sGetEnableCache() : returns int
START class CISDesign(CISBase):
IsDeletedOccurrence(pDboInstOccurrence, partinst, pDesign) : returns int
Class : CISDesign(CISBase):
Parameters:
pDboInstOccurrence: DboInstOccurrence *
partinst: DboPartInst *
pDesign: DboDesign *
SetDesign(pDesign)
Class : CISDesign(CISBase):
Parameters:
pDesign: DboDesign *
GetVariantCount() : returns int
Class : CISDesign(CISBase):
Parameters:
SetActiveVariant(variantName)
Class : CISDesign(CISBase):
Parameters:

---

variantName: CString const &
GetActiveVariant(variantName)
Class : CISDesign(CISBase):
Parameters:
variantName: CString &
SetParentName(arg0)
Class : CISDesign(CISBase):
Parameters:
arg2: CString const &
GetParentName(arg0)
Class : CISDesign(CISBase):
Parameters:
arg2: CString &
SetActiveBomVariantName(arg0)
Class : CISDesign(CISBase):
Parameters:
arg2: CString const &
GetActiveBomVariantName(arg0)
Class : CISDesign(CISBase):
Parameters:
arg2: CString &
NGetActiveVariants(variantNames)
Class : CISDesign(CISBase):
Parameters:
variantNames: CStringArray &
NSetActiveVariants(variantNames)
Class : CISDesign(CISBase):
Parameters:
variantNames: CStringArray const &
GetDesignIds(DesignIds)
Class : CISDesign(CISBase):
Parameters:

---

DesignIds: CUIntArray &
GetPartOccForID(ID) : returns CISInstOccurrence
Class : CISDesign(CISBase):
Parameters:
ID: UINT
GetAmbiIds(BomName, m_AmbiPartIds)
Class : CISDesign(CISBase):
Parameters:
BomName: CString
m_AmbiPartIds: CMapStringToPtr &
LoadAmbiguousPartsMap(szrgBomName)
Class : CISDesign(CISBase):
Parameters:
szrgBomName: CStringArray &
LoadAmbiguousPartsMap(m_AmbiguousPartsMap, m_designpartsarray, CurrentItem,
Class : CISDesign(CISBase):
bflag = 1)
Class : CISDesign(CISBase):
Parameters:
m_AmbiguousPartsMap: CMapStringToPtr &
m_designpartsarray: CUIntArray &
CurrentItem: CString
bflag: int
LoadAmbiguousPartsMap(m_AmbiguousPartsMap, m_designpartsarray, CurrentItem)
Class : CISDesign(CISBase):
Parameters:
m_AmbiguousPartsMap: CMapStringToPtr &
m_designpartsarray: CUIntArray &
CurrentItem: CString
FindInt(Array, ElementToFind) : returns int
Class : CISDesign(CISBase):
Parameters:
Array: CUIntArray const &
ElementToFind: UINT

---

CompareArray(FirstArray, SecondArray, l_OutputArray)
Class : CISDesign(CISBase):
Parameters:
FirstArray: CUIntArray &
SecondArray: CUIntArray &
l_OutputArray: CUIntArray &
CleanAmbiIds(keyToBeDeleted = "")
Class : CISDesign(CISBase):
Parameters:
keyToBeDeleted: CString
CleanAmbiIds()
Class : CISDesign(CISBase):
Parameters:
DeleteRemovedParts()
Class : CISDesign(CISBase):
Parameters:
GetDesign() : returns DboDesign
Class : CISDesign(CISBase):
Parameters:
GetDesignName(DesignName)
Class : CISDesign(CISBase):
Parameters:
DesignName: CString &
Read() : returns DboState
Class : CISDesign(CISBase):
Parameters:
InitDesign(pLibStorage) : returns DboState
Class : CISDesign(CISBase):
Parameters:
pLibStorage: IStorage *
Save() : returns DboState

---

Class : CISDesign(CISBase):
Parameters:
SetModified(Mod)
Class : CISDesign(CISBase):
Parameters:
Mod: int
IsModified(Mod) : returns int
Class : CISDesign(CISBase):
Parameters:
Mod: int
GetVariantNames(VariantNames, bVariantMode = 0)
Class : CISDesign(CISBase):
Parameters:
VariantNames: CSStringArray &
bVariantMode: int
GetVariantNames(VariantNames)
Class : CISDesign(CISBase):
Parameters:
VariantNames: CSStringArray &
AddVariant(NewVariantNames)
Class : CISDesign(CISBase):
Parameters:
NewVariantNames: CSStringArray const &
DeleteVariant(VariantNames)
Class : CISDesign(CISBase):
Parameters:
VariantNames: CSStringArray const &
RenameVariant(OldVariantNames, NewVariantNames)
Class : CISDesign(CISBase):
Parameters:
OldVariantNames: CSStringArray const &
NewVariantNames: CSStringArray const &

---

MarkModified(MarkDesign = 1)
Class : CISDesign(CISBase):
Parameters:
MarkDesign: int
MarkModified()
Class : CISDesign(CISBase):
Parameters:
SetProperty(pCISPartInst, PropertyName, PropertyValue)
Class : CISDesign(CISBase):
Parameters:
pCISPartInst: CISVariantPartOBJ *
PropertyName: CString const &
PropertyValue: CString const &
AddToDesignHeierarchy(pCISPartInst) : returns CISSchematic
Class : CISDesign(CISBase):
Parameters:
pCISPartInst: CISVariantPartOBJ *
RemoveCISSchematic(pDboSchematic)
Class : CISDesign(CISBase):
Parameters:
pDboSchematic: DboSchematic *
AddCISSchematic(pDboSchematic) : returns CISSchematic
Class : CISDesign(CISBase):
Parameters:
pDboSchematic: DboSchematic *
GetCISSchematic(pDboSchematic) : returns CISSchematic
Class : CISDesign(CISBase):
Parameters:
pDboSchematic: DboSchematic *
UpdateHeierarchy()
Class : CISDesign(CISBase):
Parameters:

---

ApplyActiveVariantPropsToCaptureParts(PageId = 0, bWysiwygVariant = 0) : returns int
Class : CISDesign(CISBase):
Parameters:
PageId: UINT
bWysiwygVariant: int
ApplyActiveVariantPropsToCaptureParts(PageId = 0) : returns int
Class : CISDesign(CISBase):
Parameters:
PageId: UINT
ApplyActiveVariantPropsToCaptureParts() : returns int
Class : CISDesign(CISBase):
Parameters:
RestoreCaptureProps(PageId = 0, bWysiwygVariant = 0)
Class : CISDesign(CISBase):
Parameters:
PageId: UINT
bWysiwygVariant: int
RestoreCaptureProps(PageId = 0)
Class : CISDesign(CISBase):
Parameters:
PageId: UINT
RestoreCaptureProps()
Class : CISDesign(CISBase):
Parameters:
GetTitleBlockPropertyVale(VariantNameString)
Class : CISDesign(CISBase):
Parameters:
VariantNameString: CString &
DesignEdit()
Class : CISDesign(CISBase):
Parameters:
RenameScheamtic(OldName, NewName)

---

Class : CISDesign(CISBase):
Parameters:
OldName: CString const &
NewName: CString const &
RenameScheamticPage(OldName, NewName)
Class : CISDesign(CISBase):
Parameters:
OldName: CString const &
NewName: CString const &
PageEdit(pageinfo)
Class : CISDesign(CISBase):
Parameters:
pageinfo: UINT
UpdateCache()
Class : CISDesign(CISBase):
Parameters:
EditAllPages()
Class : CISDesign(CISBase):
Parameters:
GetSchematic(index) : returns CISSchematic
Class : CISDesign(CISBase):
Parameters:
index: int &
GetInstOccurrence(pOcc) : returns CISInstOccurrence
Class : CISDesign(CISBase):
Parameters:
pOcc: DboInstOccurrence *
GetCoreDesignString(CoreDesign)
Class : CISDesign(CISBase):
Parameters:
CoreDesign: CString &
SetNotStuffedString(NotStuffedString)

---

Class : CISDesign(CISBase):
Parameters:
NotStuffedString: CString const &
SetPartNumberPropertyName(PartNumberName)
Class : CISDesign(CISBase):
Parameters:
PartNumberName: CString const &
GetBOMFilesCount() : returns UINT
Class : CISDesign(CISBase):
Parameters:
SetBOMFilesCount(FilesCount)
Class : CISDesign(CISBase):
Parameters:
FilesCount: UINT
GetVRTFilesCount() : returns UINT
Class : CISDesign(CISBase):
Parameters:
SetVRTFilesCount(FilesCount)
Class : CISDesign(CISBase):
Parameters:
FilesCount: UINT
IsComplexDesign() : returns int
Class : CISDesign(CISBase):
Parameters:
AddPart(OCCCount)
Class : CISDesign(CISBase):
Parameters:
OCCCount: int
DeletePart(OCCCount)
Class : CISDesign(CISBase):
Parameters:
OCCCount: int

---

UpdatePart(OldCCCount, NewOCCCount)
Class : CISDesign(CISBase):
Parameters:
OldCCCount: int
NewOCCCount: int
HasOccurrenceCountChanged() : returns int
Class : CISDesign(CISBase):
Parameters:
SetOccurrenceCountChanged(OCCCountChanged)
Class : CISDesign(CISBase):
Parameters:
OCCCountChanged: int
HasHierarchicalBlcoks() : returns int
Class : CISDesign(CISBase):
Parameters:
SetHierarchicalBlcoks(b)
Class : CISDesign(CISBase):
Parameters:
b: int
HasHierarchicalBlocksChanged() : returns int
Class : CISDesign(CISBase):
Parameters:
HierarchicalBlocksChanged()
Class : CISDesign(CISBase):
Parameters:
HierarchicalBlocksEdits()
Class : CISDesign(CISBase):
Parameters:
HasPartRefChanged() : returns int
Class : CISDesign(CISBase):
Parameters:

---

SetPartRefChanged(PartRefChanged)
Class : CISDesign(CISBase):
Parameters:
PartRefChanged: int
ResetPartListFlags()
Class : CISDesign(CISBase):
Parameters:
ProcessDirtyDesign()
Class : CISDesign(CISBase):
Parameters:
ResetDirtyFlags()
Class : CISDesign(CISBase):
Parameters:
RebuildList() : returns int
Class : CISDesign(CISBase):
Parameters:
SetRebuildFlag(Rebuild)
Class : CISDesign(CISBase):
Parameters:
Rebuild: int
SetPartEdits()
Class : CISDesign(CISBase):
Parameters:
SetLinkDataBaseFlag(bFlag)
Class : CISDesign(CISBase):
Parameters:
bFlag: int
GetLinkDataBaseFlag() : returns int
Class : CISDesign(CISBase):
Parameters:

---

SetSchematicModified(bSchFlag)
Class : CISDesign(CISBase):
Parameters:
bSchFlag: int
IsSchematicModified() : returns int
Class : CISDesign(CISBase):
Parameters:
IsDesignOld() : returns int
Class : CISDesign(CISBase):
Parameters:
SetOldDesignUpdated(l_bDesign)
Class : CISDesign(CISBase):
Parameters:
l_bDesign: int
IsPartManagerActive() : returns int
Class : CISDesign(CISBase):
Parameters:
SetPartManagerActive(l_bActive)
Class : CISDesign(CISBase):
Parameters:
l_bActive: int
SetCaptureDboObject(pDboObject)
Class : CISDesign(CISBase):
Parameters:
pDboObject: DboBaseObject *
GetCaptureDboObject() : returns DboBaseObject
Class : CISDesign(CISBase):
Parameters:
GetGroupsContainer() : returns CVariant
Class : CISDesign(CISBase):
Parameters:

---

GetBOMVariantContainer() : returns CNewBOm
Class : CISDesign(CISBase):
Parameters:
SetForceSkipProcessDirtyDesign(value) : returns int
Class : CISDesign(CISBase):
Parameters:
value: int
GetCommonParts(SrcArray)
Class : CISDesign(CISBase):
Parameters:
SrcArray: CUIntArray &
IsDesignModified() : returns int
Class : CISDesign(CISBase):
Parameters:
GetDataCacheScope() : returns CISDesignDataCacheScope
Class : CISDesign(CISBase):
Parameters:
GetDatefromRegionalSettings(DateString)
Class : CISDesign(CISBase):
Parameters:
DateString: CString &
GetSelectedVariant() : returns CString
Class : CISDesign(CISBase):
Parameters:
SetSelectedVariant(variantName)
Class : CISDesign(CISBase):
Parameters:
variantName: CString &
GetTitleBlockValue(Prop) : returns CString
Class : CISDesign(CISBase):
Parameters:
Prop: CString &

---

InitTitleBlockInfo()
Class : CISDesign(CISBase):
Parameters:
GetDisplayedTitleBlockProp(TitleBlockArray)
Class : CISDesign(CISBase):
Parameters:
TitleBlockArray: CStringArray &
GetCisInstOccrIds(ID, CisPartIDArray)
Class : CISDesign(CISBase):
Parameters:
ID: long
CisPartIDArray: CUIntArray &
SetPageEdit()
Class : CISDesign(CISBase):
Parameters:
GetCISOccurrence(pOcc) : returns CISInstOccurrence
Class : CISDesign(CISBase):
Parameters:
pOcc: DboInstOccurrence *
GetPartInstForID(ID) : returns CISPartInst
Class : CISDesign(CISBase):
Parameters:
ID: long
GetPartNumberPropertyName() : returns CString
Class : CISDesign(CISBase):
Parameters:
CheckForExternalDesignSchematic()
Class : CISDesign(CISBase):
Parameters:
END class CISDesign(CISBase):