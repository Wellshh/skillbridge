# Class: DboLibPart(DboSymbol):

DboSymbolToDboLibPart(x) : returns DboLibPart
Parameters:
x: DboSymbol *
START class DboLibPart(DboSymbol):
GetPin(name, status) : returns DboSymbolPin
Class : DboLibPart(DboSymbol):
Parameters:
name: CString &
status: DboState &
GetPin(position, status) : returns DboSymbolPin
Class : DboLibPart(DboSymbol):
Parameters:
position: unsigned int
status: DboState &
GetReference(name) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
name: CString &
GetPartValue(value) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
value: CString &
GetContents(status) : returns DboView
Class : DboLibPart(DboSymbol):
Parameters:
status: DboState &
GetContentsViewType(status) : returns ViewTypeT
Class : DboLibPart(DboSymbol):
Parameters:
status: DboState &
GetContentsViewName(name) : returns DboState

---

Class : DboLibPart(DboSymbol):
Parameters:
name: CString &
GetContentsLibName(name) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
name: CString &
GetPinNumbersAreVisible(status) : returns int
Class : DboLibPart(DboSymbol):
Parameters:
status: DboState &
GetPinNamesAreVisible(status) : returns int
Class : DboLibPart(DboSymbol):
Parameters:
status: DboState &
GetPinNamesAreRotated(status) : returns int
Class : DboLibPart(DboSymbol):
Parameters:
status: DboState &
GetReferenceDesignator(refDes) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
refDes: CString &
GetPackagePtr() : returns DboPackage
Class : DboLibPart(DboSymbol):
Parameters:
GetCellPtr() : returns DboCell
Class : DboLibPart(DboSymbol):
Parameters:
sGetPinNumbersAreVisible(obj, status) : returns int
Class : DboLibPart(DboSymbol):
Parameters:

---

obj: DboBaseObject *
status: DboState &
sGetPinNamesAreRotated(obj, status) : returns int
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinNamesAreVisible(obj, status) : returns int
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPinCount(obj, status) : returns int
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetReference(obj, status) : returns CString
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetReferenceDesignator(obj, status) : returns CString
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPartValue(obj, status) : returns CString
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsLibName(obj, status) : returns CString

---

Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
IsEquivalent(pObj) : returns int
Class : DboLibPart(DboSymbol):
Parameters:
pObj: DboBaseObject *
GetSemanticString(str)
Class : DboLibPart(DboSymbol):
Parameters:
str: CString &
sGetContentsViewName(obj, status) : returns CString
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetContentsViewType(obj, status) : returns ViewTypeT
Class : DboLibPart(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
MarkModified() : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
NewLPinsIter(status, mode = ALL) : returns DboLibPartPinsIter
Class : DboLibPart(DboSymbol):
Parameters:
status: DboState &
mode: enum IterDefs::IterModeT
NewLPinsIter(status) : returns DboLibPartPinsIter
Class : DboLibPart(DboSymbol):
Parameters:

---

status: DboState &
SetContentsViewType(viewType) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
viewType: enum DboValue::ViewTypeT
SetContentsViewName(viewName) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
viewName: CString &
SetContentsLibName(libName) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
libName: CString &
SetReference(name) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
name: CString &
SetPartValue(name) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
name: CString &
SetPinNumbersAreVisible(bVal) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
bVal: int
SetPinNamesAreVisible(bVal) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:
bVal: int
SetPinNamesAreRotated(bVal) : returns DboState
Class : DboLibPart(DboSymbol):
Parameters:

---

bVal: int
SetCellPtr(pCell)
Class : DboLibPart(DboSymbol):
Parameters:
pCell: DboCell *
SetPackagePtr(pPkg)
Class : DboLibPart(DboSymbol):
Parameters:
pPkg: DboPackage *
GetSuffix() : returns CString
Class : DboLibPart(DboSymbol):
Parameters:
END class DboLibPart(DboSymbol):
DboLibPart_sGetPinNumbersAreVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetPinNamesAreRotated(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetPinNamesAreVisible(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetPinCount(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetReference(obj, status) : returns CString
Parameters: