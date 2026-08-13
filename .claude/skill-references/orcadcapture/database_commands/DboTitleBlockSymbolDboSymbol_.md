# Class: DboTitleBlockSymbol(DboSymbol):

x: DboSymbol *
START class DboTitleBlockSymbol(DboSymbol):
sGetPageCount(obj, status) : returns CString
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageNumber(obj, status) : returns CString
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageSize(obj, status) : returns CString
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageCreateDate(obj, status) : returns CString
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
sGetPageModifyDate(obj, status) : returns CString
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
obj: DboBaseObject *
status: DboState &
NewSymbolPinScalar(status, name, type, start, hotPoint, visible = 1) : returns DboSymbolPinScalar
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT

---

start: CPoint
hotPoint: CPoint
visible: int
NewSymbolPinScalar(status, name, type, start, hotPoint) : returns DboSymbolPinScalar
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
NewSymbolPinBus(status, name, type, start, hotPoint, visible = 1) : returns DboSymbolPinBus
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
visible: int
NewSymbolPinBus(status, name, type, start, hotPoint) : returns DboSymbolPinBus
Class : DboTitleBlockSymbol(DboSymbol):
Parameters:
status: DboState &
name: CString &
type: enum DboValue::PinTypeT
start: CPoint
hotPoint: CPoint
END class DboTitleBlockSymbol(DboSymbol):
DboTitleBlockSymbol_sGetPageCount(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlockSymbol_sGetPageNumber(obj, status) : returns CString