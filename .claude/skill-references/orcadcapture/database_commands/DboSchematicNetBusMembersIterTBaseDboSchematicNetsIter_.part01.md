<!--
source: database_commands/DboSchematicNetBusMembersIterTBaseDboSchematicNetsIter_.md
part: 1/2
-->

# Class: DboSchematicNetBusMembersIter(TBaseDboSchematicNetsIter):

START class DboSchematicNetBusMembersIter(TBaseDboSchematicNetsIter):
NextMember(status) : returns DboSchematicNet
Class : DboSchematicNetBusMembersIter(TBaseDboSchematicNetsIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboSchematicNetBusMembersIter(TBaseDboSchematicNetsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboSchematicNetBusMembersIter(TBaseDboSchematicNetsIter):
Parameters:
pObject: DboSchematicNet *&
END class DboSchematicNetBusMembersIter(TBaseDboSchematicNetsIter):
DboEffectivePropsIterToDboSchematicNetEffectivePropsIter(x) : returns
DboSchematicNetEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboSchematicNetEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboSchematicNetEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboSchematicNetEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &

---

bEditable: int &
bDeletable: int &
END class DboSchematicNetEffectivePropsIter(DboEffectivePropsIter):
START class STATE_DATA
END class STATE_DATA
START class COrOccTransactions
END class COrOccTransactions
START class ACTIVATE_DATA
END class ACTIVATE_DATA
START class connectivityGridCell
END class connectivityGridCell
START class objectHotspot
END class objectHotspot
GetActivateData(data)
Parameters:
data: ACTIVATE_DATA *
DboBaseObjectToDboPage(x) : returns DboPage
Parameters:
x: DboBaseObject *
START class DboPage(DboBaseObject):
PointOnHotSpot(location) : returns int
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint

---

GetObjectType() : returns ObjectTypeT
Class : DboPage(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboPage(DboBaseObject):
Parameters:
GetName(name) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
name: CString &
GetOwner() : returns DboSchematic
Class : DboPage(DboBaseObject):
Parameters:
GetPageNumber(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetModifyTime(status) : returns time_t
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetCreateTime(status) : returns time_t
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetPartInstCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetPartInstCount() : returns int
Class : DboPage(DboBaseObject):
Parameters:

---

GetWireCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetBusEntryCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetPortCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetGlobalCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetOffPageConnectorCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetOffPageConnectorFromID(nID) : returns DboOffPageConnector
Class : DboPage(DboBaseObject):
Parameters:
nID: unsigned long
GetCommentGraphicCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetPartInstFromSch(name, status) : returns DboPartInst
Class : DboPage(DboBaseObject):
Parameters:
name: CString const &

---

status: DboState &
GetPartInst(name, status) : returns DboPartInst
Class : DboPage(DboBaseObject):
Parameters:
name: CString const &
status: DboState &
GetPartInst(id, status) : returns DboPartInst
Class : DboPage(DboBaseObject):
Parameters:
id: unsigned long
status: DboState &
GetWire(id, status) : returns DboWire
Class : DboPage(DboBaseObject):
Parameters:
id: unsigned long
status: DboState &
GetWire(location, status) : returns DboWire
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &
GetFirstWireEndPoint(location, status) : returns DboWire
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &
GetWireAtJunction(location, status) : returns DboWire
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &
GetBusEntry(location, status) : returns DboBusEntry
Class : DboPage(DboBaseObject):

---

Parameters:
location: CPoint
status: DboState &
GetPortInst(location, status) : returns DboPortInst
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &
GetGraphicInst(status, id, nType = NULL_OBJECT) : returns DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
id: unsigned long
nType: enum DboBaseObject::ObjectTypeT
GetGraphicInst(status, id) : returns DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
id: unsigned long
GetTitleBlock(id, status) : returns DboTitleBlock
Class : DboPage(DboBaseObject):
Parameters:
id: unsigned long
status: DboState &
GetPort(name, status) : returns DboPort
Class : DboPage(DboBaseObject):
Parameters:
name: CString &
status: DboState &
IsConnectionPoint(location, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &

---

GetConnectionCount(location, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &
GetDocUnits(bDrawableSize = 0) : returns CSize
Class : DboPage(DboBaseObject):
Parameters:
bDrawableSize: int
GetDocUnits() : returns CSize
Class : DboPage(DboBaseObject):
Parameters:
GetDocUnitsPerInch() : returns double
Class : DboPage(DboBaseObject):
Parameters:
GetPhysicalGranularity() : returns double
Class : DboPage(DboBaseObject):
Parameters:
GetPinToPinScaleFactor() : returns double
Class : DboPage(DboBaseObject):
Parameters:
GetPageWidth() : returns long
Class : DboPage(DboBaseObject):
Parameters:
GetPageHeight() : returns long
Class : DboPage(DboBaseObject):
Parameters:
GetPinToPin() : returns long
Class : DboPage(DboBaseObject):
Parameters:

---

GetIsMetric() : returns int
Class : DboPage(DboBaseObject):
Parameters:
GetPageSizeInfo(nPageWidth, nPageHeight, nPinToPin, bIsMetric)
Class : DboPage(DboBaseObject):
Parameters:
nPageWidth: long &
nPageHeight: long &
nPinToPin: long &
bIsMetric: int &
GetBorderDisplayed(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetBorderPrinted(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetGridRefDisplayed(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetGridRefPrinted(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetTitleBlockDisplayed(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetTitleBlockPrinted(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
GetANSIGridRefs(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetSizeName(size) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
size: CString &
GetSize(status) : returns CSize
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetOuterBorderMargin(status) : returns CPoint
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetOuterBorderLineStyle(status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetOuterBorderLineWidth(status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetOuterBorderIsVisible(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetInnerBorderMargin(status) : returns CPoint
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
GetInnerBorderLineStyle(status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetInnerBorderLineWidth(status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetInnerBorderIsVisible(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetColor(status) : returns ColorT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetLabelFont(font) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
font: LOGFONT &
GetLabelColor(status) : returns ColorT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetHorizontalLabelCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetHorizontalLabelWidth(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
GetHorizontalLabelIsChar(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetHorizontalLabelIsVisible(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetHorizontalLabelIsAscending(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetHorizontalSeparatorLineStyle(status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetHorizontalSeparatorLineWidth(status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetVerticalLabelCount(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetVerticalLabelWidth(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetVerticalLabelIsChar(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
GetVerticalLabelIsVisible(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetVerticalLabelIsAscending(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetVerticalSeparatorLineStyle(status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetVerticalSeparatorLineWidth(status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
GetUserStorage(name, status) : returns IStorage
Class : DboPage(DboBaseObject):
Parameters:
name: CString &
status: DboState &
IsPersistent(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
IsModified(status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
IsLocked(status) : returns int
Class : DboPage(DboBaseObject):

---

Parameters:
status: DboState &
sGetPageNumber(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetModifyTime(obj, status) : returns time_t
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetCreateTime(obj, status) : returns time_t
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetName(obj, status) : returns CString
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSizeName(obj, status) : returns CString
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSizeX(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSizeY(obj, status) : returns int

---

Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetOuterBorderMarginX(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetOuterBorderMarginY(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetOuterBorderLineStyle(obj, status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetOuterBorderLineWidth(obj, status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetOuterBorderIsVisible(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetInnerBorderMarginX(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &

---

sGetInnerBorderMarginY(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetInnerBorderLineStyle(obj, status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetInnerBorderLineWidth(obj, status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetInnerBorderIsVisible(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetColor(obj, status) : returns ColorT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetLabelColor(obj, status) : returns ColorT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHorizontalLabelCount(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:

---

obj: DboBaseObject *
status: DboState &
sGetHorizontalLabelIsChar(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHorizontalLabelIsVisible(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHorizontalLabelIsAscending(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHorizontalSeparatorLineStyle(obj, status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetHorizontalSeparatorLineWidth(obj, status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetVerticalLabelCount(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetVerticalLabelIsChar(obj, status) : returns int

---

Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetVerticalLabelIsVisible(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetVerticalLabelIsAscending(obj, status) : returns int
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetVerticalSeparatorLineStyle(obj, status) : returns LineStyleT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetVerticalSeparatorLineWidth(obj, status) : returns LineWidthT
Class : DboPage(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetNet(pObj, status) : returns DboNet
Class : DboPage(DboBaseObject):
Parameters:
pObj: DboBaseObject *
status: DboState &
GetNet(name, status) : returns DboNet
Class : DboPage(DboBaseObject):
Parameters:
name: CString &
status: DboState &

---

GetNet(id, status) : returns DboNet
Class : DboPage(DboBaseObject):
Parameters:
id: unsigned long
status: DboState &
GetConnection(location) : returns DboConnection
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
IsValidNetName(csNetName) : returns int
Class : DboPage(DboBaseObject):
Parameters:
csNetName: CString &
IsTransactionInProgress() : returns int
Class : DboPage(DboBaseObject):
Parameters:
PartAlreadyExistsWithName(UniqueNm) : returns int
Class : DboPage(DboBaseObject):
Parameters:
UniqueNm: CString
GetWiresList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetPortsList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetERCsList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetBookMarksList() : returns DboPtrArray
Class : DboPage(DboBaseObject):

---

Parameters:
GetGlobalsList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetOffPageConnectorsList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetBusEntriesList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetCommentGraphicsList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetTitleBlocksList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetCustomItemsList() : returns DboPtrArray
Class : DboPage(DboBaseObject):
Parameters:
GetPartInstList() : returns DboMapNameAndIdToPartInst
Class : DboPage(DboBaseObject):
Parameters:
GetTransactionCount() : returns int
Class : DboPage(DboBaseObject):
Parameters:
GetLabelState(label) : returns int
Class : DboPage(DboBaseObject):
Parameters:
label: char *
GetLabelArray(label)

---

Class : DboPage(DboBaseObject):
Parameters:
label: char [][50]
NotifyChangingInstId(oldId, inst)
Class : DboPage(DboBaseObject):
Parameters:
oldId: unsigned long
inst: DboPartInst *
NotifyChangingInstName(oldname, inst)
Class : DboPage(DboBaseObject):
Parameters:
oldname: CString const &
inst: DboPartInst *
GetParentObj() : returns DboBaseObject
Class : DboPage(DboBaseObject):
Parameters:
MarkModified() : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
NewPartInstsIter(status) : returns DboPagePartInstsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewWiresIter(status, mode = TOP) : returns DboPageWiresIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewWiresIter(status) : returns DboPageWiresIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &

---

NewPortsIter(status, mode = TOP) : returns DboPagePortsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewPortsIter(status) : returns DboPagePortsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewGlobalsIter(status) : returns DboPageGlobalsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewOffPageConnectorsIter(status, mode = TOP) : returns DboPageOffPageConnectorsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewOffPageConnectorsIter(status) : returns DboPageOffPageConnectorsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewCommentGraphicsIter(status) : returns DboPageCommentGraphicsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewBusEntriesIter(status) : returns DboPageBusEntriesIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewTitleBlocksIter(status) : returns DboPageTitleBlocksIter
Class : DboPage(DboBaseObject):
Parameters:

---

status: DboState &
NewERCsIter(status) : returns DboPageERCsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewBookMarksIter(status) : returns DboPageBookMarksIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
NewObjectsAtPointIter(location, status) : returns DboPageObjectsAtPointIter
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
status: DboState &
NewWiresInAreaIter(area, status) : returns DboWiresInAreaIter
Class : DboPage(DboBaseObject):
Parameters:
area: CRect
status: DboState &
NewWiresAtPointIter(pt, status) : returns DboWiresAtPointIter
Class : DboPage(DboBaseObject):
Parameters:
pt: CPoint
status: DboState &
NewEditsIter(status, bOccurrenceEdits = 0) : returns DboPageEditsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
bOccurrenceEdits: int
NewEditsIter(status) : returns DboPageEditsIter
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &

---

GetUnNamedBundleList(UnNamedBundleList) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
UnNamedBundleList: CStringList &
DeleteJunction(location) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
SetPageWidth(nPageWidth)
Class : DboPage(DboBaseObject):
Parameters:
nPageWidth: long
SetPageHeight(nPageHeight)
Class : DboPage(DboBaseObject):
Parameters:
nPageHeight: long
SetPinToPin(nPinToPin)
Class : DboPage(DboBaseObject):
Parameters:
nPinToPin: long
SetIsMetric(bIsMetric)
Class : DboPage(DboBaseObject):
Parameters:
bIsMetric: int
SetPageSizeInfo(nPageWidth, nPageHeight, nPinToPin, bIsMetric)
Class : DboPage(DboBaseObject):
Parameters:
nPageWidth: long
nPageHeight: long
nPinToPin: long
bIsMetric: int
SetBorderDisplayed(bVal) : returns DboState

---

Class : DboPage(DboBaseObject):
Parameters:
bVal: int
SetBorderPrinted(bVal) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bVal: int
SetGridRefDisplayed(bVal) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bVal: int
SetGridRefPrinted(bVal) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bVal: int
SetTitleBlockDisplayed(bVal) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bVal: int
SetTitleBlockPrinted(bVal) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bVal: int
SetANSIGridRefs(bVal) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bVal: int
SetSizeName(name) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
name: CString &
SetSize(size) : returns DboState

---

Class : DboPage(DboBaseObject):
Parameters:
size: CSize
SetOuterBorderMargin(location) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
SetOuterBorderLineStyle(lineStyle) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
lineStyle: enum DboValue::LineStyleT
SetOuterBorderLineWidth(lineWidth) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
lineWidth: enum DboValue::LineWidthT
SetOuterBorderIsVisible(bval) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetInnerBorderMargin(location) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
location: CPoint
SetInnerBorderLineStyle(lineStyle) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
lineStyle: enum DboValue::LineStyleT
SetInnerBorderLineWidth(lineWidth) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
lineWidth: enum DboValue::LineWidthT
SetInnerBorderIsVisible(bval) : returns DboState

---

Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetColor(color) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
color: enum DboValue::ColorT
SetLabelFont(font) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
font: LOGFONT &
SetLabelColor(color) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
color: enum DboValue::ColorT
SetHorizontalLabelCount(count) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
count: int
SetHorizontalLabelWidth(nWidth) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
nWidth: int
SetHorizontalLabelIsChar(bval) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetHorizontalLabelIsVisible(bval) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetHorizontalLabelIsAscending(bval) : returns DboState

---

Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetHorizontalSeparatorLineStyle(lineStyle) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
lineStyle: enum DboValue::LineStyleT
SetHorizontalSeparatorLineWidth(lineWidth) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
lineWidth: enum DboValue::LineWidthT
SetVerticalLabelCount(count) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
count: int
SetVerticalLabelWidth(nWidth) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
nWidth: int
SetVerticalLabelIsChar(bval) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetVerticalLabelIsVisible(bval) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetVerticalLabelIsAscending(bval) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
bval: int
SetVerticalSeparatorLineStyle(lineStyle) : returns DboState

---

Class : DboPage(DboBaseObject):
Parameters:
lineStyle: enum DboValue::LineStyleT
SetVerticalSeparatorLineWidth(lineWidth) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
lineWidth: enum DboValue::LineWidthT
NewNetScalar() : returns DboNetScalar
Class : DboPage(DboBaseObject):
Parameters:
NewNetBus(bIsBundle = 0) : returns DboNetBus
Class : DboPage(DboBaseObject):
Parameters:
bIsBundle: int
NewNetBus() : returns DboNetBus
Class : DboPage(DboBaseObject):
Parameters:
UpdatePageState()
Class : DboPage(DboBaseObject):
Parameters:
RestorePrevState(bRedo)
Class : DboPage(DboBaseObject):
Parameters:
bRedo: int
UpdateRedoState()
Class : DboPage(DboBaseObject):
Parameters:
InitUndoRedoData()
Class : DboPage(DboBaseObject):
Parameters:
ClearUndoRedoData()

---

Class : DboPage(DboBaseObject):
Parameters:
ClearUndoRedoInfo(bRedo)
Class : DboPage(DboBaseObject):
Parameters:
bRedo: int
DeleteDeletedObject(pObject)
Class : DboPage(DboBaseObject):
Parameters:
pObject: DboDeletedObject *
NewDeletedObject() : returns DboDeletedObject
Class : DboPage(DboBaseObject):
Parameters:
SetLabelState(label)
Class : DboPage(DboBaseObject):
Parameters:
label: char *
DeleteLabelState(label) : returns int
Class : DboPage(DboBaseObject):
Parameters:
label: char *
CreateLog() : returns int
Class : DboPage(DboBaseObject):
Parameters:
CloseLog()
Class : DboPage(DboBaseObject):
Parameters:
DumpObjectMap(bRedo)
Class : DboPage(DboBaseObject):
Parameters:
bRedo: int

---

StartTransaction(type = EDIT_T) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
type: enum DboPage::TransactionType
StartTransaction() : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
CopyToFile(pFile) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pFile: CFile *
CopyFromFile(pFile, bCopyName = 1) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pFile: CFile *
bCopyName: int
CopyFromFile(pFile) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
pFile: CFile *
Copy(source) : returns DboState
Class : DboPage(DboBaseObject):
Parameters:
source: DboBaseObject *
NewPlacedInst(Name, PackageName, part, device, status, bNewVersion = 0) : returns
DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
Name: CString &
PackageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
bNewVersion: int

---

NewPlacedInst(Name, PackageName, part, device, status) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
Name: CString &
PackageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
NewPlacedInst(status, Name, PackageName, part, device, location,
Class : DboPage(DboBaseObject):
rotation = NOROTATION, mirror = 0, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
nID = 0) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
PackageName: CString &
part: DboLibPart *
device: DboDevice *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
color: enum DboValue::ColorT
nID: unsigned long
NewPlacedInst(status, Name, PackageName, part, device, location,
Class : DboPage(DboBaseObject):
rotation = NOROTATION, mirror = 0, color = DEFAULT_OBJECT_COLOR) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
PackageName: CString &
part: DboLibPart *
device: DboDevice *
location: CPoint
rotation: enum DboValue::RotationT

---

mirror: int
color: enum DboValue::ColorT
NewPlacedInst(status, Name, PackageName, part, device, location,
Class : DboPage(DboBaseObject):
rotation = NOROTATION, mirror = 0) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
PackageName: CString &
part: DboLibPart *
device: DboDevice *
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
NewPlacedInst(status, Name, PackageName, part, device, location,
Class : DboPage(DboBaseObject):
rotation = NOROTATION) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
PackageName: CString &
part: DboLibPart *
device: DboDevice *
location: CPoint
rotation: enum DboValue::RotationT
NewPlacedInst(status, Name, PackageName, part, device, location) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
PackageName: CString &
part: DboLibPart *
device: DboDevice *
location: CPoint

---

NewPlacedInst(pSource, status, ptOffset = CPoint(0,0), bNewVersion = 0) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboPlacedInst *
status: DboState &
ptOffset: CPoint const
bNewVersion: int
NewPlacedInst(pSource, status, ptOffset = CPoint(0,0)) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboPlacedInst *
status: DboState &
ptOffset: CPoint const
NewPlacedInst(pSource, status) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboPlacedInst *
status: DboState &
NewPlacedInst(pSource, status, ptOffset = CPoint(0,0)) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboTemplatePartInst *
status: DboState &
ptOffset: CPoint const
NewPlacedInst(pSource, status) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboTemplatePartInst *
status: DboState &
ReplaceInst(pOldInst, packageName, part, device, status, bUpdate = 0,
Class : DboPage(DboBaseObject):
bNewVersion = 0) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboPlacedInst *

---

packageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
bUpdate: int
bNewVersion: int
ReplaceInst(pOldInst, packageName, part, device, status, bUpdate = 0) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboPlacedInst *
packageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
bUpdate: int
ReplaceInst(pOldInst, packageName, part, device, status) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboPlacedInst *
packageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
ReplaceInst(pOldInst, packageName, part, device, status, bUpdate,
Class : DboPage(DboBaseObject):
bNewVersion, bPreserverefDes, bDeleteOldInst = 1,
Class : DboPage(DboBaseObject):
updateDPfromLib = 0) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboPlacedInst *
packageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
bUpdate: int
bNewVersion: int

---

bPreserverefDes: int
bDeleteOldInst: int
updateDPfromLib: int
ReplaceInst(pOldInst, packageName, part, device, status, bUpdate,
Class : DboPage(DboBaseObject):
bNewVersion, bPreserverefDes, bDeleteOldInst = 1) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboPlacedInst *
packageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
bUpdate: int
bNewVersion: int
bPreserverefDes: int
bDeleteOldInst: int
ReplaceInst(pOldInst, packageName, part, device, status, bUpdate,
Class : DboPage(DboBaseObject):
bNewVersion, bPreserverefDes) : returns DboPlacedInst
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboPlacedInst *
packageName: CString &
part: DboLibPart *
device: DboDevice *
status: DboState &
bUpdate: int
bNewVersion: int
bPreserverefDes: int
ReplaceGraphicInst(pOldInst, pNewSymbol, packageName, status, bUpdate = 0) : returns
DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboGraphicInstance *
pNewSymbol: DboBaseObject *
packageName: CString &

---

status: DboState &
bUpdate: int
ReplaceGraphicInst(pOldInst, pNewSymbol, packageName, status) : returns DboGraphicInstance
Class : DboPage(DboBaseObject):
Parameters:
pOldInst: DboGraphicInstance *
pNewSymbol: DboBaseObject *
packageName: CString &
status: DboState &
NewDrawnInst(Name, status, nId = 0) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
nId: unsigned long
NewDrawnInst(Name, status) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
Name: CString &
status: DboState &
NewDrawnInst(pSource, status, bNewVersion = 0) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboDrawnInst *
status: DboState &
bNewVersion: int
NewDrawnInst(pSource, status) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
pSource: DboDrawnInst *
status: DboState &
NewDrawnInst(status, Name, boundingBox, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0, color = DEFAULT_OBJECT_COLOR,

---

Class : DboPage(DboBaseObject):
isBunndleBlock = False, isUnNamedBundle = False) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
boundingBox: CRect
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
color: enum DboValue::ColorT
isBunndleBlock: bool
isUnNamedBundle: bool
NewDrawnInst(status, Name, boundingBox, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0, color = DEFAULT_OBJECT_COLOR,
Class : DboPage(DboBaseObject):
isBunndleBlock = False) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
boundingBox: CRect
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
color: enum DboValue::ColorT
isBunndleBlock: bool
NewDrawnInst(status, Name, boundingBox, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0, color = DEFAULT_OBJECT_COLOR) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
boundingBox: CRect
location: CPoint
rotation: enum DboValue::RotationT

---

mirror: int
color: enum DboValue::ColorT
NewDrawnInst(status, Name, boundingBox, location, rotation = NOROTATION,
Class : DboPage(DboBaseObject):
mirror = 0) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
boundingBox: CRect
location: CPoint
rotation: enum DboValue::RotationT
mirror: int
NewDrawnInst(status, Name, boundingBox, location, rotation = NOROTATION) : returns
DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
boundingBox: CRect
location: CPoint
rotation: enum DboValue::RotationT
NewDrawnInst(status, Name, boundingBox, location) : returns DboDrawnInst
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
Name: CString &
boundingBox: CRect
location: CPoint
NewWireScalar(status, start, end, color = DEFAULT_OBJECT_COLOR, bNewVersion = 0,
Class : DboPage(DboBaseObject):
style = DEFAULT_LINE_STYLE, width = DEFAULT_LINE_WIDTH) : returns DboWireScalar
Class : DboPage(DboBaseObject):
Parameters:
status: DboState &
start: CPoint

---

end: CPoint