# Class: DboTitleBlock(DboGraphicInstance,DboInstOccMapper):

Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlockSymbol_sGetPageSize(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlockSymbol_sGetPageCreateDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlockSymbol_sGetPageModifyDate(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboGraphicInstanceToDboTitleBlock(x) : returns DboTitleBlock
Parameters:
x: DboGraphicInstance *
DboInstOccMapperToDboTitleBlock(x) : returns DboTitleBlock
Parameters:
x: DboInstOccMapper *
START class DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
IsBoundingBoxDirty() : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
GetBoundingBox() : returns CRect
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
GetSymbol(status) : returns DboSymbol
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:

---

status: DboState &
GetSourceSymbolName(name) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString &
GetSourceLibName(name) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString &
GetDesignName(name) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString &
GetDesignFileName(name) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString &
GetDesignCreateDate(status) : returns time_t
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetDesignModifyDate(status) : returns time_t
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetDesignCreateTime(time) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
time: CString &
GetDesignModifyTime(time) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:

---

time: CString &
GetPageCount(status) : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetSchematicCreateDate(status) : returns time_t
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetSchematicModifyDate(status) : returns time_t
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetSchematicCreateTime(time) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
time: CString &
GetSchematicModifyTime(time) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
time: CString &
GetPageNumber(status) : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetPageCreateDate(status) : returns time_t
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
status: DboState &
GetPageModifyDate(status) : returns time_t
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:

---

status: DboState &
GetPageCreateTime(time) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
time: CString &
GetPageModifyTime(time) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
time: CString &
GetPageSize(size) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
size: CString &
GetKeepInLowerRightCorner(arg0) : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
arg2: DboState &
GetEffectivePropValueChoices(name, choices) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString const &
choices: CStringList &
GetObjectOccurrence(pParentSchematicOcc) : returns DboOccurrence
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
pParentSchematicOcc: DboInstOccurrence *
GetObjectOccurrences(occArr, pDesign, status, bOnlyCurrent = False)
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
bOnlyCurrent: bool

---

GetObjectOccurrences(occArr, pDesign, status)
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
occArr: DboOccurrenceArray &
pDesign: DboDesign *
status: DboState &
GetNextNewVariantProp(strName, strVal, bNewFound) : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
strName: CString &
strVal: CString &
bNewFound: int &
IsVariantPropMapEmpty() : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
GetVariantProp(strName, strVal) : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
strName: CString const &
strVal: CString &
sGetDesignName(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDesignFileName(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDesignCreateDate(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:

---

obj: DboBaseObject *
status: DboState &
sGetDesignModifyDate(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSchematicCreateDate(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSchematicModifyDate(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageCreateDate(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageModifyDate(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDesignCreateTime(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetDesignModifyTime(obj, status) : returns CString

---

Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageCreateTime(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageModifyTime(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSchematicCreateTime(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSchematicModifyTime(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageCount(obj, status) : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageSize(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetSchematicName(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageNumber(obj, status) : returns int
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSourceLibName(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSourceSymbolName(obj, status) : returns CString
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
obj: DboBaseObject *
status: DboState &
SetBoundingBoxDirty(bSetting)
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
bSetting: int
SetBoundingBox(boundingBox) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
boundingBox: CRect
SetPageCount(nPageCount) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
nPageCount: int

---

GetSchematicName(name) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
name: CString &
SetPageNumber(nPageNumber) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
nPageNumber: int
SetKeepInLowerRightCorner(bLR) : returns DboState
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
bLR: int
AddVariantProp(strName, strVal)
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
strName: CString const &
strVal: CString const &
ClearVariantMap(bFlag = 1)
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
bFlag: int
ClearVariantMap()
Class : DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
Parameters:
END class DboTitleBlock(DboGraphicInstance,DboInstOccMapper):
DboTitleBlock_sGetDesignName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetDesignFileName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *