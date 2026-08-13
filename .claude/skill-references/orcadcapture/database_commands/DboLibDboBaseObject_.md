# Class: DboLib(DboBaseObject):

DboBaseObjectToDboLib(x) : returns DboLib
Parameters:
x: DboBaseObject *
START class DboLib(DboBaseObject):
TimeToString(time) : returns CString
Class : DboLib(DboBaseObject):
Parameters:
time: time_t
IsAutoSaving() : returns int
Class : DboLib(DboBaseObject):
Parameters:
IsAutoBackupOn() : returns int
Class : DboLib(DboBaseObject):
Parameters:
IsCheckOn() : returns int
Class : DboLib(DboBaseObject):
Parameters:
IsCorrectOn() : returns int
Class : DboLib(DboBaseObject):
Parameters:
GetObjectType() : returns ObjectTypeT
Class : DboLib(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboLib(DboBaseObject):
Parameters:
GetName(name) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
name: CString &

---

GetOldName(name) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
GetOwner() : returns DboSession
Class : DboLib(DboBaseObject):
Parameters:
GetModifyTime(status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
GetModifyTime(pObj, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboLibObject *
status: DboState &
GetCreateTime(status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
GetCreateTime(pObj, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboLibObject *
status: DboState &
IsModified(status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
IsModifiedSinceAutoSave(status) : returns int
Class : DboLib(DboBaseObject):
Parameters:

---

status: DboState &
IsModifiedSinceLastAutoBackup(status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
GetDefaultPageRec(status) : returns PageRec
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
IsPersistent(status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
IsPersistent(pObj, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboBaseObject *
status: DboState &
GetModifiedTime(objName, nType, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
objName: CString
nType: enum DboBaseObject::ObjectTypeT
status: DboState &
CacheIsOutOfDate(pObj, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboBaseObject *
status: DboState &
CacheIsOutOfDate(nType, SourceLibName, SourceName, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
nType: enum DboBaseObject::ObjectTypeT

---

SourceLibName: CString &
SourceName: CString &
status: DboState &
GetCachedTime(nType, SourceLibName, objName, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
nType: enum DboBaseObject::ObjectTypeT
SourceLibName: CString &
objName: CString
status: DboState &
IsObjectModified(pObj, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboBaseObject *
status: DboState &
sGetNormalizedName(name, NormalizedName, bMemorize = False) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
NormalizedName: CString &
bMemorize: bool
sGetNormalizedName(name, NormalizedName) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
NormalizedName: CString &
GetPart(name, status) : returns DboLibPart
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetCell(name, status) : returns DboCell
Class : DboLib(DboBaseObject):
Parameters:

---

name: CString &
status: DboState &
GetPartCreateTime(part, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
part: DboLibPart *
status: DboState &
GetPartModifyTime(part, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
part: DboLibPart *
status: DboState &
GetCellCreateTime(cell, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
cell: DboCell *
status: DboState &
GetCellModifyTime(cell, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
cell: DboCell *
status: DboState &
SymbolExists(name, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
IsSymbolInMemory(name, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetSymbol(name, status) : returns DboSymbol

---

Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetERCSymbol(Name, status) : returns DboERCSymbol
Class : DboLib(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
GetBookMarkSymbol(Name, status) : returns DboBookMarkSymbol
Class : DboLib(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
GetGlobalSymbol(Name, status) : returns DboGlobalSymbol
Class : DboLib(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
GetPortSymbol(Name, status) : returns DboPortSymbol
Class : DboLib(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
GetOffPageSymbol(Name, status) : returns DboOffPageSymbol
Class : DboLib(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
GetTitleBlockSymbol(name, status) : returns DboTitleBlockSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &

---

GetSymbolCreateTime(symbol, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
symbol: DboSymbol *
status: DboState &
GetSymbolModifyTime(symbol, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
symbol: DboSymbol *
status: DboState &
GetView(name, status) : returns DboView
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetSchematic(Name, status) : returns DboSchematic
Class : DboLib(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
GetExternalView(Name, status) : returns DboExternalView
Class : DboLib(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
GetViewCreateTime(view, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
view: DboView *
status: DboState &
GetViewModifyTime(view, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:

---

view: DboView *
status: DboState &
GetGraphicObject(name, status) : returns DboGraphicObject
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetGraphicObjectCreateTime(graphic, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
graphic: DboGraphicObject *
status: DboState &
GetGraphicObjectModifyTime(graphic, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
graphic: DboGraphicObject *
status: DboState &
PackageExists(name, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
IsPackageInMemory(name, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetPackage(name, status) : returns DboPackage
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetPackageCreateTime(pPackage, status) : returns time_t

---

Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
status: DboState &
GetPackageModifyTime(pPackage, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
status: DboState &
GetExportBlock(name, status) : returns DboExportBlock
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetExportBlockCreateTime(exportBlock, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
exportBlock: DboExportBlock *
status: DboState &
GetExportBlockModifyTime(exportBlock, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
exportBlock: DboExportBlock *
status: DboState &
GetDefaultPlacedInstIsPrimitive(status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
GetDefaultDrawnInstIsPrimitive(status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
ConvertRequired() : returns int

---

Class : DboLib(DboBaseObject):
Parameters:
GetTempViewName(pszFormatString, name)
Class : DboLib(DboBaseObject):
Parameters:
pszFormatString: char const *
name: CString &
GetTempPackageName(pszFormatString, name)
Class : DboLib(DboBaseObject):
Parameters:
pszFormatString: char const *
name: CString &
GetSourceLibName(objName, pCachedObj, libName) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
objName: CString &
pCachedObj: DboLibObject *
libName: CString &
GetCachedPart(SourceLibName, SourcePartName) : returns DboLibPart
Class : DboLib(DboBaseObject):
Parameters:
SourceLibName: CString &
SourcePartName: CString &
GetCachedCell(SourceLibName, SourceCellName) : returns DboCell
Class : DboLib(DboBaseObject):
Parameters:
SourceLibName: CString &
SourceCellName: CString &
GetCachedSymbol(SourceLibName, SourceSymbolName, type) : returns DboSymbol
Class : DboLib(DboBaseObject):
Parameters:
SourceLibName: CString &
SourceSymbolName: CString &
type: enum DboBaseObject::ObjectTypeT

---

GetCachedPackage(SourceLibName, SourcePackageName) : returns DboPackage
Class : DboLib(DboBaseObject):
Parameters:
SourceLibName: CString &
SourcePackageName: CString &
GetCachedGraphicObject(SourceLibName, SourceGraphicName, type) : returns DboGraphicObject
Class : DboLib(DboBaseObject):
Parameters:
SourceLibName: CString &
SourceGraphicName: CString &
type: enum DboBaseObject::ObjectTypeT
GetFont(nFontId) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
nFontId: int
GetFontId(font) : returns int
Class : DboLib(DboBaseObject):
Parameters:
font: LOGFONT &
GetDataRelease() : returns short
Class : DboLib(DboBaseObject):
Parameters:
GetDataVersion() : returns short
Class : DboLib(DboBaseObject):
Parameters:
GetSaveAsRelease() : returns short
Class : DboLib(DboBaseObject):
Parameters:
GetSaveAsVersion() : returns short
Class : DboLib(DboBaseObject):
Parameters:

---

GetDataFormatVersion(strVersion)
Class : DboLib(DboBaseObject):
Parameters:
strVersion: CString &
GetParentObj() : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
SetCorrectFlag(pCorrect)
Class : DboLib(DboBaseObject):
Parameters:
pCorrect: int
SetCheckFlag(pCheck)
Class : DboLib(DboBaseObject):
Parameters:
pCheck: int
MarkModified() : returns DboState
Class : DboLib(DboBaseObject):
MarkModified(pObj)
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboLibObject *
MarkModified(pPart)
Class : DboLib(DboBaseObject):
Parameters:
pPart: DboLibPart *
MarkModified(pCell)
Class : DboLib(DboBaseObject):
Parameters:
pCell: DboCell *
MarkModified(pPackage)
Class : DboLib(DboBaseObject):
Parameters:

---

pPackage: DboPackage *
MarkModified(pSymbol)
Class : DboLib(DboBaseObject):
Parameters:
pSymbol: DboSymbol *
MarkModified(pGraphic)
Class : DboLib(DboBaseObject):
Parameters:
pGraphic: DboGraphicObject *
MarkModified(pView)
Class : DboLib(DboBaseObject):
Parameters:
pView: DboView *
MarkModified(pBlock)
Class : DboLib(DboBaseObject):
Parameters:
pBlock: DboExportBlock *
MarkModified(strName, pDir)
Class : DboLib(DboBaseObject):
Parameters:
strName: CString &
pDir: DboDirectory *
ClearModified()
Class : DboLib(DboBaseObject):
ClearModified(pObj)
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboLibObject *
ClearModifiedAll(pDboPackage)
Class : DboLib(DboBaseObject):
Parameters:
pDboPackage: DboPackage *

---

NewCachesIter(mode = ALL) : returns DboLibCachesIter
Class : DboLib(DboBaseObject):
Parameters:
mode: enum IterDefs::IterModeT
NewCachesIter() : returns DboLibCachesIter
Class : DboLib(DboBaseObject):
Parameters:
NewChangedObjectsIter(status) : returns DboLibChangedObjectsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewUnusedCacheEntriesIter(status) : returns DboLibUnusedCacheEntriesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewPartsIter(status) : returns DboLibPartsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewPartNamesIter(status) : returns DboLibPartNamesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewCellsIter(status) : returns DboLibCellsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewCellNamesIter(status) : returns DboLibCellNamesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &

---

NewSymbolsIter(status, mode = ALL) : returns DboLibSymbolsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewSymbolsIter(status) : returns DboLibSymbolsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewSymbolNamesIter(status) : returns DboLibSymbolNamesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewViewsIter(status, mode = ALL) : returns DboLibViewsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewViewsIter(status) : returns DboLibViewsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewViewNamesIter(status) : returns DboLibViewNamesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewGraphicObjectsIter(status) : returns DboLibGraphicsIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewGraphicNamesIter(status) : returns DboLibGraphicNamesIter
Class : DboLib(DboBaseObject):
Parameters:

---

status: DboState &
NewPackagesIter(status) : returns DboLibPackagesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewPackageNamesIter(status, mode = ALL) : returns DboLibPackageNamesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPackageNamesIter(status) : returns DboLibPackageNamesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewPackageAliasesIter(name, status) : returns DboLibPackageAliasesIter
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewExportBlocksIter(status) : returns DboLibExportBlocksIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
NewExportBlockNamesIter(status) : returns DboLibExportBlockNamesIter
Class : DboLib(DboBaseObject):
Parameters:
status: DboState &
SetFont(font) : returns int
Class : DboLib(DboBaseObject):
Parameters:
font: LOGFONT &
FixupMismatchedLibPartLookupNames() : returns DboState

---

Class : DboLib(DboBaseObject):
Parameters:
SetIsAutoSaving(bAutoSaving = 1)
Class : DboLib(DboBaseObject):
Parameters:
bAutoSaving: int
SetIsAutoSaving()
Class : DboLib(DboBaseObject):
Parameters:
SetIsBundleSaveInProgress(bFlag = True)
Class : DboLib(DboBaseObject):
Parameters:
bFlag: bool
SetIsBundleSaveInProgress()
Class : DboLib(DboBaseObject):
Parameters:
SetIsAutoBackupOn(bAutoBackup = 1)
Class : DboLib(DboBaseObject):
Parameters:
bAutoBackup: int
SetIsAutoBackupOn()
Class : DboLib(DboBaseObject):
Parameters:
UpdateCache(sourceLibName, sourceObjName, nObjType, bUpdate = 1) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
sourceLibName: CString &
sourceObjName: CString &
nObjType: enum DboBaseObject::ObjectTypeT
bUpdate: int
UpdateCache(sourceLibName, sourceObjName, nObjType) : returns DboState
Class : DboLib(DboBaseObject):

---

Parameters:
sourceLibName: CString &
sourceObjName: CString &
nObjType: enum DboBaseObject::ObjectTypeT
ReplaceCache(OldPackageOrSymbolName, OldLibName, NewName, NewLibName,
Class : DboLib(DboBaseObject):
bUpdateCache = 0, bPreserverefDes = 0) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
OldPackageOrSymbolName: CString
OldLibName: CString
NewName: CString
NewLibName: CString
bUpdateCache: int
bPreserverefDes: int
ReplaceCache(OldPackageOrSymbolName, OldLibName, NewName, NewLibName,
Class : DboLib(DboBaseObject):
bUpdateCache = 0) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
OldPackageOrSymbolName: CString
OldLibName: CString
NewName: CString
NewLibName: CString
bUpdateCache: int
ReplaceCache(OldPackageOrSymbolName, OldLibName, NewName, NewLibName) : returns
DboState
Class : DboLib(DboBaseObject):
Parameters:
OldPackageOrSymbolName: CString
OldLibName: CString
NewName: CString
NewLibName: CString
NewUntitledName(name)
Class : DboLib(DboBaseObject):
Parameters:

---

name: CString &
AbortTransactions() : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
ExplicitlyRemovePartDirName(PackageNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
PackageNameToBeRemoved: CString
SavePart(part) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
part: DboLibPart *
SavePackageAll(pPackage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
CopyCacheFromFile(pLibFile, status) : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pLibFile: CFile *
status: DboState &
GetPinShapeSymbol(name, status) : returns DboPinShapeSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetUserStorage(name, status) : returns IStorage
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
GetDefaultFont(nFontType, status) : returns LOGFONT

---

Class : DboLib(DboBaseObject):
Parameters:
nFontType: enum DboLib::DefaultFontType
status: DboState &
GetPartFieldMapping(nNum, field) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
nNum: int
field: CString &
sGetName(obj, status) : returns CString
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetModifyTime(obj, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetCreateTime(obj, status) : returns time_t
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPlacedInstIsPrimitive(obj, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultDrawnInstIsPrimitive(obj, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetDefaultPinNameFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPinNumberFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPartReferenceFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultNoConnectFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultERCFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultBookMarkFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPowerFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:

---

obj: DboBaseObject *
status: DboState &
sGetDefaultOffPageConnectorFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPortFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPartValueFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPropertyFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultDrawnInstNameFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultAliasFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultCommentFont(obj, status) : returns LOGFONT

---

Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultTitleBlockFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultBorderFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultNetNameFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultStimulusSymbolFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPSpiceSourceSymbolFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultPSpiceSimulationDirectiveSymbolFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetDefaultPSpiceABMSymbolFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultParameterFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultOptimizerFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDefaultGraphicObjectFont(obj, status) : returns LOGFONT
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetTempName(pszName, pDir) : returns CString
Class : DboLib(DboBaseObject):
Parameters:
pszName: char const *
pDir: DboDirectory *
sGetTempName(pszName, pDir, nLength) : returns CString
Class : DboLib(DboBaseObject):
Parameters:
pszName: char const *
pDir: DboDirectory *
nLength: int
GetLibStoragePtr() : returns IStorage
Class : DboLib(DboBaseObject):

---

Parameters:
SizeOfLibTitle() : returns int
Class : DboLib(DboBaseObject):
LibTitle() : returns char
Class : DboLib(DboBaseObject):
GetStringPtrFromIndex(nIndex, status) : returns CString
Class : DboLib(DboBaseObject):
Parameters:
nIndex: int
status: DboState &
GetIndexForString(str, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
str: CString const &
status: DboState &
GetEffectivePropValueChoices(name, choices) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
name: CString const &
choices: CStringList &
sGetTimeFormat(obj, status) : returns CString
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
SetUpRevDialogBit()
Class : DboLib(DboBaseObject):
Parameters:
ClearUpRevDialogBit()
Class : DboLib(DboBaseObject):
Parameters:

---

IsUpRevDialogBitSet() : returns int
Class : DboLib(DboBaseObject):
Parameters:
sSplitName(pszName, BaseName, Uniquifier, Extension)
Class : DboLib(DboBaseObject):
Parameters:
pszName: char const *
BaseName: CString &
Uniquifier: CString &
Extension: CString &
DeleteLibStoragePtr()
Class : DboLib(DboBaseObject):
Parameters:
sEquivalentNames(name1, name2, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
name1: CString &
name2: CString &
status: DboState &
sGetNormalizedObjectName(name, NormalizedName) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
NormalizedName: CString &
sGetUnNormalizedObjectName(normalizeName, name) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
normalizeName: CString &
name: CString &
AddStringToStringTable(str, status) : returns CString
Class : DboLib(DboBaseObject):
Parameters:
str: CString const &
status: DboState &

---

RegenerateMissingCell(pDev, strLibName, cellName, status) : returns DboCell
Class : DboLib(DboBaseObject):
Parameters:
pDev: DboDevice *
strLibName: CString
cellName: CString
status: DboState &
sSetTimeFormat(obj, format) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
obj: DboBaseObject *
format: CString &
NewPackage(name, status) : returns DboPackage
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewCell(name, status) : returns DboCell
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewPart(name, status) : returns DboLibPart
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
SkipSymbolOnFile(pFile, status, otType = NULL_OBJECT)
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
otType: enum DboBaseObject::ObjectTypeT

---

SkipSymbolOnFile(pFile, status)
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
SkipGraphicObjectOnFile(pFile, status, otType = NULL_OBJECT)
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
otType: enum DboBaseObject::ObjectTypeT
SkipGraphicObjectOnFile(pFile, status)
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
SkipObjectOnFile(pFile, status)
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
AutoSave(path) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
path: CString &
AutoBackup(pathname) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pathname: CString &
SaveAsRequired(nRelease, nVersion) : returns int
Class : DboLib(DboBaseObject):
Parameters:
nRelease: short &
nVersion: short &

---

SetLibStoragePtr(pShareStorage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pShareStorage: IStorage *
ClearSaveFlag(pPackage)
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
RenameObject(pObj, newName) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboBaseObject *
newName: CString &
RemoveBundles()
Class : DboLib(DboBaseObject):
Parameters:
IsBundleUsed(bundleName, SourceLibName) : returns int
Class : DboLib(DboBaseObject):
Parameters:
bundleName: CString
SourceLibName: CString
OnChangeBundleDefinition() : returns int
Class : DboLib(DboBaseObject):
Parameters:
SaveObject(pObj) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pObj: DboBaseObject *
CleanupCache() : returns DboState
Class : DboLib(DboBaseObject):
Parameters:

---

DeletePart(part) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
part: DboLibPart *
RemovePart(part) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
part: DboLibPart *
CopyPart(part, newName, status) : returns DboLibPart
Class : DboLib(DboBaseObject):
Parameters:
part: DboLibPart *
newName: CString &
status: DboState &
SaveCell(cell) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
cell: DboCell *
DeleteCell(cell) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
cell: DboCell *
RemoveCell(cell) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
cell: DboCell *
CopyCell(cell, newName, status) : returns DboCell
Class : DboLib(DboBaseObject):
Parameters:
cell: DboCell *
newName: CString &
status: DboState &
CopyLibObject(LibObje, newName, status) : returns DboLibObject

---

Class : DboLib(DboBaseObject):
Parameters:
LibObje: DboLibObject *
newName: CString &
status: DboState &
DeleteLibObject(libObj) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
libObj: DboLibObject *
CopySymbolFromFile(pFile, status, otType = NULL_OBJECT, bDefaultName = 0) : returns
DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
otType: enum DboBaseObject::ObjectTypeT
bDefaultName: int
CopySymbolFromFile(pFile, status, otType = NULL_OBJECT) : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
otType: enum DboBaseObject::ObjectTypeT
CopySymbolFromFile(pFile, status) : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
CopyGraphicObjectFromFile(pFile, status, otType = NULL_OBJECT, bDefaultName = 0) : returns
DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
otType: enum DboBaseObject::ObjectTypeT

---

bDefaultName: int
CopyGraphicObjectFromFile(pFile, status, otType = NULL_OBJECT) : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
otType: enum DboBaseObject::ObjectTypeT
CopyGraphicObjectFromFile(pFile, status) : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
CopyObjectFromFile(pFile, status, bCopyName = 1) : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
bCopyName: int
CopyObjectFromFile(pFile, status) : returns DboBaseObject
Class : DboLib(DboBaseObject):
Parameters:
pFile: CFile *
status: DboState &
CopyPackageAllToCache(source, SourceLibName, SourcePackageName, status) : returns
DboPackage
Class : DboLib(DboBaseObject):
Parameters:
source: DboBaseObject *
SourceLibName: CString &
SourcePackageName: CString &
status: DboState &
NewERCSymbol(name, status) : returns DboERCSymbol
Class : DboLib(DboBaseObject):
Parameters:

---

name: CString &
status: DboState &
NewBookMarkSymbol(name, status) : returns DboBookMarkSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewGlobalSymbol(name, status) : returns DboGlobalSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewPortSymbol(name, status) : returns DboPortSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewPinShapeSymbol(name, status) : returns DboPinShapeSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewOffPageSymbol(name, status) : returns DboOffPageSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewTitleBlockSymbol(name, status) : returns DboTitleBlockSymbol
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
SaveSymbol(symbol) : returns DboState

---

Class : DboLib(DboBaseObject):
Parameters:
symbol: DboSymbol *
SaveERCSymbol(pSymbol) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pSymbol: DboERCSymbol *
SaveBookMarkSymbol(pSymbol) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pSymbol: DboBookMarkSymbol *
SaveGlobalSymbol(_global) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
global: DboGlobalSymbol *
SavePortSymbol(port) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
port: DboPortSymbol *
SavePinShapeSymbol(pinShape) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pinShape: DboPinShapeSymbol *
SaveOffPageSymbol(offpage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
offpage: DboOffPageSymbol *
SaveTitleBlockSymbol(titleblock) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
titleblock: DboTitleBlockSymbol *
DeleteSymbol(symbol) : returns DboState

---

Class : DboLib(DboBaseObject):
Parameters:
symbol: DboSymbol *
RemoveSymbol(symbol) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
symbol: DboSymbol *
CopySymbol(symbol, newName, status) : returns DboSymbol
Class : DboLib(DboBaseObject):
Parameters:
symbol: DboSymbol *
newName: CString &
status: DboState &
NewSchematic(name, status) : returns DboSchematic
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
NewExternalView(name, type, FileName, status) : returns DboExternalView
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
type: CString &
FileName: CString &
status: DboState &
SaveView(view) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
view: DboView *
SaveSchematic(schematic) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
schematic: DboSchematic *

---

SaveExternalView(view) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
view: DboExternalView *
DeleteView(view) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
view: DboView *
RemoveView(view) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
view: DboView *
CopyView(view, newName, status) : returns DboView
Class : DboLib(DboBaseObject):
Parameters:
view: DboView *
newName: CString &
status: DboState &
NewGraphicObject(name, status) : returns DboGraphicObject
Class : DboLib(DboBaseObject):
Parameters:
name: CString &
status: DboState &
SaveGraphicObject(graphic) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
graphic: DboGraphicObject *
DeleteGraphicObject(graphic) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
graphic: DboGraphicObject *
RemoveGraphicObject(graphic) : returns DboState
Class : DboLib(DboBaseObject):

---

Parameters:
graphic: DboGraphicObject *
CopyGraphicObject(graphic, newName, status) : returns DboGraphicObject
Class : DboLib(DboBaseObject):
Parameters:
graphic: DboGraphicObject *
newName: CString &
status: DboState &
NewPackageAlias(pPackage, alias) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
alias: CString &
DeletePackageAlias(pPackage, alias) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
alias: CString &
DeletePackageAlias(strPackageName, alias) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
strPackageName: CString &
alias: CString &
SavePackage(pPackage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
DeletePackage(pPackage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
DeletePackage(name) : returns DboState
Class : DboLib(DboBaseObject):

---

Parameters:
name: CString &
RemovePackage(pPackage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
CopyPackage(pPackage, newName, status) : returns DboPackage
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
newName: CString &
status: DboState &
CopyPackageAll(pPackage, newName, status) : returns DboPackage
Class : DboLib(DboBaseObject):
Parameters:
pPackage: DboPackage *
newName: CString &
status: DboState &
ExplicitlyRemoveViewDirName(PackageNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
PackageNameToBeRemoved: CString
ExplicitlyRemovePartsDirName(PartNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
PartNameToBeRemoved: CString
ExplicitlyRemoveCellDirName(CellNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
CellNameToBeRemoved: CString
ExplicitlyRemoveSymbolDirName(SymbolNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:

---

SymbolNameToBeRemoved: CString
ExplicitlyRemoveGraphicDirName(SymbolNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
SymbolNameToBeRemoved: CString
ExplicitlyRemoveExportBlockDirName(SymbolNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
SymbolNameToBeRemoved: CString
ExplicitlyRemoveAliasName(AliasNameToBeRemoved) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
AliasNameToBeRemoved: CString
ExplicitlyAddPackageDirName(packageName) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
packageName: char const *
ExplicitlyAddPartDirName(partDir) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
partDir: char const *
ExplicitlyAddCellDirName(cellDir) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
cellDir: char const *
GetOrStorageStream(designName, storageName, arg2, arg3) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
designName: char const *
storageName: char const *
arg3: std::vector< std::string > &
arg4: std::vector< std::string > &

---

RemoveOrStorageStream(designName, storageName, arg2) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
designName: char const *
storageName: char const *
arg3: std::vector< std::string > &
RenameOrStorageStream(designName, storageName, streamName) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
designName: char const *
storageName: char const *
streamName: std::vector< std::string > &
ReadForExistenceOfBundleMapData(pLib, pDsnStorage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pLib: DboLib *
pDsnStorage: IStorage *
ReadForExistenceOfBundleMapData(pDes, pDsnStorage) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
pDes: DboDesign *
pDsnStorage: IStorage *
SetBit(bit, bOn) : returns bool
Class : DboLib(DboBaseObject):
Parameters:
bit: int
bOn: bool
ReplaceSourceLibName(objName, pCachedObj, libName, newLibName) : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
objName: CString &
pCachedObj: DboLibObject *
libName: CString &
newLibName: CString &

---

CorrectCacheEntry() : returns DboState
Class : DboLib(DboBaseObject):
Parameters:
IsOccRetainAndRemapMode() : returns bool
Class : DboLib(DboBaseObject):
Parameters:
SetDataRelease(pRelease)
Class : DboLib(DboBaseObject):
Parameters:
pRelease: short
SetDataVersion(pVersion)
Class : DboLib(DboBaseObject):
Parameters:
pVersion: short
IsBitSet(bit) : returns bool
Class : DboLib(DboBaseObject):
Parameters:
bit: int
IsRemoveBundleSelected() : returns int
Class : DboLib(DboBaseObject):
Parameters:
isBundleTemplateExists() : returns bool
Class : DboLib(DboBaseObject):
Parameters:
GetBundleTemplateMap() : returns DboBundleTemplateMap
Class : DboLib(DboBaseObject):
Parameters:
GetBundleDef(bundleName, srcLibName = "", owner = None) : returns DboBundle
Class : DboLib(DboBaseObject):
Parameters:
bundleName: CString
srcLibName: CString

---

owner: DboBaseObject *
GetBundleDef(bundleName, srcLibName = "") : returns DboBundle
Class : DboLib(DboBaseObject):
Parameters:
bundleName: CString
srcLibName: CString
GetBundleDef(bundleName) : returns DboBundle
Class : DboLib(DboBaseObject):
Parameters:
bundleName: CString
IsUnnamedBundle(bundleName, pObj, pScope = "") : returns bool
Class : DboLib(DboBaseObject):
Parameters:
bundleName: CString
pObj: DboBaseObject *
pScope: CString
IsUnnamedBundle(bundleName, pObj) : returns bool
Class : DboLib(DboBaseObject):
Parameters:
bundleName: CString
pObj: DboBaseObject *
GetBundleTemplateMapForObject(pObject) : returns DboBundleTemplateMap
Class : DboLib(DboBaseObject):
Parameters:
pObject: DboBaseObject *
GetBitFlag() : returns int
Class : DboLib(DboBaseObject):
Parameters:
IsCacheTimeSameAsSource(nType, SourceLibName, SourceName, status) : returns int
Class : DboLib(DboBaseObject):
Parameters:
nType: enum DboBaseObject::ObjectTypeT
SourceLibName: CString &

---

SourceName: CString &
status: DboState &
END class DboLib(DboBaseObject):
sGetNormalizedName(name, NormalizedName, bMemorize = False) : returns DboState
Parameters:
name: CString &
NormalizedName: CString &
bMemorize: bool
DboLib_sGetNormalizedName(name, NormalizedName) : returns DboState
Parameters:
name: CString &
NormalizedName: CString &
DboLib_sGetName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetModifyTime(obj, status) : returns time_t
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetCreateTime(obj, status) : returns time_t
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultPlacedInstIsPrimitive(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLib_sGetDefaultDrawnInstIsPrimitive(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &