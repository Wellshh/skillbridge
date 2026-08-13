# Class: TBaseDboFlatNetNetOccurrencesIter(IterDefs):

DboFlatNet_sGetLineWidth(obj, status) : returns LineWidthT
Parameters:
obj: DboBaseObject *
status: DboState &
DboFlatNet_sGetLineStyle(obj, status) : returns LineStyleT
Parameters:
obj: DboBaseObject *
status: DboState &
START class TBaseDboFlatNetNetOccurrencesIter(IterDefs):
GetType() : returns int
Class : TBaseDboFlatNetNetOccurrencesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboFlatNetNetOccurrencesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboFlatNetNetOccurrencesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboFlatNetNetOccurrencesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboFlatNetNetOccurrencesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboFlatNetNetOccurrencesIter(IterDefs):
START class DboFlatNetNetOccurrencesIter(TBaseDboFlatNetNetOccurrencesIter):

---

NextNetOccurrence(status) : returns DboNetOccurrence
Class : DboFlatNetNetOccurrencesIter(TBaseDboFlatNetNetOccurrencesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboFlatNetNetOccurrencesIter(TBaseDboFlatNetNetOccurrencesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboFlatNetNetOccurrencesIter(TBaseDboFlatNetNetOccurrencesIter):
Parameters:
pObject: DboNetOccurrence *&
END class DboFlatNetNetOccurrencesIter(TBaseDboFlatNetNetOccurrencesIter):
START class TBaseDboFlatNetPortOccurrencesIter(IterDefs):
GetType() : returns int
Class : TBaseDboFlatNetPortOccurrencesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboFlatNetPortOccurrencesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboFlatNetPortOccurrencesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboFlatNetPortOccurrencesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboFlatNetPortOccurrencesIter(IterDefs):

---

Parameters:
status: DboState &
END class TBaseDboFlatNetPortOccurrencesIter(IterDefs):
START class DboFlatNetPortOccurrencesIter(TBaseDboFlatNetPortOccurrencesIter):
NextPortOccurrence(status) : returns DboPortOccurrence
Class : DboFlatNetPortOccurrencesIter(TBaseDboFlatNetPortOccurrencesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboFlatNetPortOccurrencesIter(TBaseDboFlatNetPortOccurrencesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboFlatNetPortOccurrencesIter(TBaseDboFlatNetPortOccurrencesIter):
Parameters:
pObject: DboPortOccurrence *&
END class DboFlatNetPortOccurrencesIter(TBaseDboFlatNetPortOccurrencesIter):
DboEffectivePropsIterToDboFlatNetEffectivePropsIter(x) : returns DboFlatNetEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboFlatNetEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboFlatNetEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboFlatNetEffectivePropsIter(DboEffectivePropsIter):

---

Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboFlatNetEffectivePropsIter(DboEffectivePropsIter):
START class TBaseDboFlatNetWiresIter(IterDefs):
GetType() : returns int
Class : TBaseDboFlatNetWiresIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboFlatNetWiresIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboFlatNetWiresIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboFlatNetWiresIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboFlatNetWiresIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboFlatNetWiresIter(IterDefs):
START class DboFlatNetWiresIter(TBaseDboSchematicNetWiresIter):
NextWire(status) : returns DboWire

---

Class : DboFlatNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboFlatNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
pObject: DboWire *&
Next(status) : returns DboBaseObject
Class : DboFlatNetWiresIter(TBaseDboSchematicNetWiresIter):
Parameters:
status: DboState &
END class DboFlatNetWiresIter(TBaseDboSchematicNetWiresIter):
START class TBaseDboFlatNetNetsIter(IterDefs):
GetType() : returns int
Class : TBaseDboFlatNetNetsIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboFlatNetNetsIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboFlatNetNetsIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboFlatNetNetsIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboFlatNetNetsIter(IterDefs):
Parameters:

---

status: DboState &
END class TBaseDboFlatNetNetsIter(IterDefs):
START class DboFlatNetNetsIter(TBaseDboSchematicNetNetsIter):
NextNet(status) : returns DboNet
Class : DboFlatNetNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns std::string
Class : DboFlatNetNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
pObject: DboNet *&
Next(status) : returns DboBaseObject
Class : DboFlatNetNetsIter(TBaseDboSchematicNetNetsIter):
Parameters:
status: DboState &
END class DboFlatNetNetsIter(TBaseDboSchematicNetNetsIter):
DbBasePropToDBProp(x) : returns DBProp
Parameters:
x: DbBaseProp *
START class DBProp(DbBaseProp):
GetName(Name) : returns DboState
Class : DBProp(DbBaseProp):
Parameters:
Name: CString &
GetNameID() : returns UINT
Class : DBProp(DbBaseProp):
Parameters:
GetType(status) : returns ValueType
Class : DBProp(DbBaseProp):

---

Parameters:
status: DboState &
GetPhysicalType(status) : returns PhysicalType
Class : DBProp(DbBaseProp):
Parameters:
status: DboState &
GetReadOnly(status) : returns int
Class : DBProp(DbBaseProp):
Parameters:
status: DboState &
GetValue(obj, value, bFromProp = 0) : returns DboState
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
value: DboValue &
bFromProp: int
GetValue(obj, value) : returns DboState
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
value: DboValue &
GetStringValue(obj, Value, bFromProp = 0) : returns DboState
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
Value: CString &
bFromProp: int
GetStringValue(obj, Value) : returns DboState
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
Value: CString &
GetFontValue(obj, font) : returns DboState

---

Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
font: LOGFONT &
GetIntValue(obj, status) : returns int
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetLongValue(obj, status) : returns unsigned long
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetTimeValue(obj, status) : returns time_t
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetBOOLValue(obj, status) : returns int
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetPinTypeValue(obj, status) : returns PinTypeT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetPrimitiveTypeValue(obj, status) : returns PrimitiveTypeT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &

---

GetViewTypeValue(obj, status) : returns ViewTypeT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetDisplayTypeValue(obj, status) : returns DisplayTypeT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetLineStyleValue(obj, status) : returns LineStyleT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetLineWidthValue(obj, status) : returns LineWidthT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetFillStyleValue(obj, status) : returns FillStyleT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetHatchStyleValue(obj, status) : returns HatchStyleT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetColorValue(obj, status) : returns ColorT
Class : DBProp(DbBaseProp):
Parameters:

---

obj: DboBaseObject *
status: DboState &
GetRotationValue(obj, status) : returns RotationT
Class : DBProp(DbBaseProp):
Parameters:
obj: DboBaseObject *
status: DboState &
GetEnumValue(val, status) : returns int
Class : DBProp(DbBaseProp):
Parameters:
val: CString const &
status: DboState &
IsOkayToIterate() : returns int
Class : DBProp(DbBaseProp):
Parameters:
IsEditable() : returns int
Class : DBProp(DbBaseProp):
Parameters:
IsDeletable() : returns int
Class : DBProp(DbBaseProp):
Parameters:
GetNext() : returns DBProp
Class : DBProp(DbBaseProp):
Parameters:
SetNext(pProp)
Class : DBProp(DbBaseProp):
Parameters:
pProp: DBProp *
END class DBProp(DbBaseProp):
DboSymbolToDboTitleBlockSymbol(x) : returns DboTitleBlockSymbol
Parameters: