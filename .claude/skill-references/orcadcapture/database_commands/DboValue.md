# Class: DboValue

START class DboValue
GetString(Value) : returns DboState
Class : DboValue
Parameters:
Value: CString &
GetInt(status) : returns int
Class : DboValue
Parameters:

---

status: DboState &
GetLong(status) : returns unsigned long
Class : DboValue
Parameters:
status: DboState &
GetTime(status) : returns time_t
Class : DboValue
Parameters:
status: DboState &
GetBool(status) : returns int
Class : DboValue
Parameters:
status: DboState &
GetColor(status) : returns COLORREF
Class : DboValue
Parameters:
status: DboState &
GetFont(logfont) : returns DboState
Class : DboValue
Parameters:
logfont: LOGFONT &
GetEnumeration(status) : returns int
Class : DboValue
Parameters:
status: DboState &
sGetEnumeration(vType, strVal, status) : returns int
Class : DboValue
Parameters:
vType: enum DboValue::ValueType
strVal: CString const &
status: DboState &
sGetValue(vType, enumValue, status) : returns CString

---

Class : DboValue
Parameters:
vType: enum DboValue::ValueType
enumValue: int
status: DboState &
GetType(status) : returns ValueType
Class : DboValue
Parameters:
status: DboState &
GetLogicalType(status) : returns ValueType
Class : DboValue
Parameters:
status: DboState &
GetPhysicalType(type, status) : returns PhysicalType
Class : DboValue
Parameters:
type: enum DboValue::ValueType
status: DboState &
GetLogicalTypeName(type, Type) : returns DboState
Class : DboValue
Parameters:
type: enum DboValue::ValueType
Type: CString &
GetCountValidValues(type, status) : returns int
Class : DboValue
Parameters:
type: enum DboValue::ValueType
status: DboState &
NewValidValuesIter(type, status) : returns DboValidValuesIter
Class : DboValue
Parameters:
type: enum DboValue::ValueType
status: DboState &

---

SetString(val) : returns DboState
Class : DboValue
Parameters:
val: char *
SetFilePath(val) : returns DboState
Class : DboValue
Parameters:
val: char *
SetBOOL(val) : returns DboState
Class : DboValue
Parameters:
val: int
SetInt(val) : returns DboState
Class : DboValue
Parameters:
val: int
SetLong(val) : returns DboState
Class : DboValue
Parameters:
val: unsigned long
SetTime(val) : returns DboState
Class : DboValue
Parameters:
val: time_t
SetColor(color) : returns DboState
Class : DboValue
Parameters:
color: enum DboValue::ColorT
SetPinType(pinType) : returns DboState
Class : DboValue
Parameters:
pinType: enum DboValue::PinTypeT

---

SetPrimitiveType(primitiveType) : returns DboState
Class : DboValue
Parameters:
primitiveType: enum DboValue::PrimitiveTypeT
SetViewType(viewType) : returns DboState
Class : DboValue
Parameters:
viewType: enum DboValue::ViewTypeT
SetLineStyle(lineStyle) : returns DboState
Class : DboValue
Parameters:
lineStyle: enum DboValue::LineStyleT
SetLineWidth(lineWidth) : returns DboState
Class : DboValue
Parameters:
lineWidth: enum DboValue::LineWidthT
SetFillStyle(fillStyle) : returns DboState
Class : DboValue
Parameters:
fillStyle: enum DboValue::FillStyleT
SetHatchStyle(hatchStyle) : returns DboState
Class : DboValue
Parameters:
hatchStyle: enum DboValue::HatchStyleT
SetRotation(rotation) : returns DboState
Class : DboValue
Parameters:
rotation: enum DboValue::RotationT
SetDisplayType(displayType) : returns DboState
Class : DboValue
Parameters:
displayType: enum DboValue::DisplayTypeT

---

SetValue(val) : returns DboState
Class : DboValue
Parameters:
val: DboValue &
END class DboValue
DboValue_sGetEnumeration(vType, strVal, status) : returns int
Parameters:
vType: enum DboValue::ValueType
strVal: CString const &
status: DboState &
DboValue_sGetValue(vType, enumValue, status) : returns CString
Parameters:
vType: enum DboValue::ValueType
enumValue: int
status: DboState &
DboValue_GetPhysicalType(type, status) : returns PhysicalType
Parameters:
type: enum DboValue::ValueType
status: DboState &
DboValue_GetLogicalTypeName(type, Type) : returns DboState
Parameters:
type: enum DboValue::ValueType
Type: CString &
DboValue_GetCountValidValues(type, status) : returns int
Parameters:
type: enum DboValue::ValueType
status: DboState &
DboValue_NewValidValuesIter(type, status) : returns DboValidValuesIter
Parameters:
type: enum DboValue::ValueType
status: DboState &
START class DboValidValuesIter