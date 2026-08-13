# Class: DboSymbolVectorVectorsIter

DboSymbolVector_sGetLocationX(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolVector_sGetLocationY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
START class DboSymbolVectorVectorsIter
NextVector(status) : returns DboVector
Class : DboSymbolVectorVectorsIter
Parameters:
status: DboState &
END class DboSymbolVectorVectorsIter
START class DboPinNumberEntry
END class DboPinNumberEntry
DboBaseObjectToDboDevice(x) : returns DboDevice
Parameters:
x: DboBaseObject *
START class DboDevice(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboDevice(DboBaseObject):
Parameters:
GetOwner() : returns DboPackage
Class : DboDevice(DboBaseObject):
Parameters:
GetCellName(name) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:

---

name: CString &
GetCell(status) : returns DboCell
Class : DboDevice(DboBaseObject):
Parameters:
status: DboState &
GetDesignator(designator) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
designator: CString &
GetPosition(status) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
status: DboState &
GetPinNumber(position, PinNumber) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
position: int
PinNumber: CString &
GetIsShared(position, status) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
position: int
status: DboState &
GetPinSwapId(position, status) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
position: int
status: DboState &
GetPinPosition(pinNumber, status) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
pinNumber: CString &
status: DboState &

---

GetPinCount(status) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
status: DboState &
sGetDesignator(obj, status) : returns CString
Class : DboDevice(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetSize(obj, status) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
obj: DboBaseObject *
status: DboState &
GetSize(status) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
status: DboState &
GetSemanticString(str)
Class : DboDevice(DboBaseObject):
Parameters:
str: CString &
GetContainingLib() : returns DboLib
Class : DboDevice(DboBaseObject):
Parameters:
IsEquivalent(pObj) : returns int
Class : DboDevice(DboBaseObject):
Parameters:
pObj: DboBaseObject *
GetParentObj() : returns DboBaseObject
Class : DboDevice(DboBaseObject):
Parameters:

---

MarkModified() : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
NewPinNumbersIter() : returns DboDevicePinNumbersIter
Class : DboDevice(DboBaseObject):
Parameters:
SetCell(cell) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
cell: DboCell *
SetDesignator(name) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
name: CString &
SetPinNumber(position, pinNumber) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
position: int
pinNumber: CString &
SetPinSwapId(position, nSwapId) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
position: int
nSwapId: int
NewPinNumber(pinNumber, position, isShared = 0, nSwapId = -1) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
pinNumber: CString &
position: int &
isShared: int
nSwapId: int
NewPinNumber(pinNumber, position, isShared = 0) : returns DboState

---

Class : DboDevice(DboBaseObject):
Parameters:
pinNumber: CString &
position: int &
isShared: int
NewPinNumber(pinNumber, position) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
pinNumber: CString &
position: int &
DeletePinNumber(position) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
position: int
DeletePinNumberAtPosition(position) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
position: int
SetIsShared(position, isShared) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
position: int
isShared: int
GeneratePinNumber(position, UniqueName) : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
position: int
UniqueName: CString &
Cleanup() : returns DboState
Class : DboDevice(DboBaseObject):
Parameters:
END class DboDevice(DboBaseObject):