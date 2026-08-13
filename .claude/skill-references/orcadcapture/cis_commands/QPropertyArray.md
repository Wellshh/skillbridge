# Class: QPropertyArray

START class QPropertyArray
Set(Name, Value = "") : returns int
Class : QPropertyArray
Parameters:
Name: CString const &
Value: CString const &
Set(Name) : returns int
Class : QPropertyArray
Parameters:
Name: CString const &
Set(Index, Value) : returns int
Class : QPropertyArray
Parameters:
Index: int
Value: CString const &
Remove(Name)
Class : QPropertyArray
Parameters:

---

Name: CString const &
RemoveAll()
Class : QPropertyArray
Parameters:
ClearAll()
Class : QPropertyArray
Parameters:
NameExists(Name) : returns int
Class : QPropertyArray
Parameters:
Name: CString const &
GetValue(Name) : returns CString
Class : QPropertyArray
Parameters:
Name: CString const &
GetValue(Index) : returns CString
Class : QPropertyArray
Parameters:
Index: int const
GetName(Index) : returns CString
Class : QPropertyArray
Parameters:
Index: int const
GetNames(PropNames)
Class : QPropertyArray
Parameters:
PropNames: CStringArray &
GetValues(PropValues)
Class : QPropertyArray
Parameters:
PropValues: CStringArray &

---

GetSize() : returns int
Class : QPropertyArray
Parameters:
Save(pFile)
Class : QPropertyArray
Parameters:
pFile: CFile *
Read(pFile)
Class : QPropertyArray
Parameters:
pFile: CFile *
GetNamesToValueIndicesMap(PropNames, ValueIndices)
Class : QPropertyArray
Parameters:
PropNames: CStringArray &
ValueIndices: CStringArray &
END class QPropertyArray
START class CPartProp(QPropertyArray):
Clear()
Class : CPartProp(QPropertyArray):
Parameters:
RemoveAll()
Class : CPartProp(QPropertyArray):
Parameters:
AddProp(PropName, PropValue, PropType = NO_TYPE)
Class : CPartProp(QPropertyArray):
Parameters:
PropName: CString const &
PropValue: CString const &
PropType: int
AddProp(PropName, PropValue)