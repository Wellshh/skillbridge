# Class: CRefDes

LinkDataBasePart()
LinkPartNumber(aPartNumber)
Parameters:
aPartNumber: char const *
SetAutomationFlag(value)
Parameters:
value: int
SetPartPresent()
SetPartNotPresent()
SetCisFieldLength(aLength)
Parameters:
aLength: int
START class CRefDes
Clone() : returns CRefDes
Class : CRefDes
Parameters:
GetPrefix() : returns CString
Class : CRefDes
Parameters:
GetNumber() : returns int
Class : CRefDes
Parameters:
GetSuffix() : returns CString
Class : CRefDes
Parameters:
GetRefDes() : returns CString
Class : CRefDes
Parameters:

---

GetRef() : returns CString
Class : CRefDes
Parameters:
IsDefined() : returns int
Class : CRefDes
Parameters:
IsMultiPkg() : returns int
Class : CRefDes
Parameters:
CompareNoCase(rVal, CompareExact = 0) : returns int
Class : CRefDes
Parameters:
rVal: CRefDes const &
CompareExact: int
CompareNoCase(rVal) : returns int
Class : CRefDes
Parameters:
rVal: CRefDes const &
MakeUpper()
Class : CRefDes
Parameters:
END class CRefDes
START class CRefDesArray
Add(Str, NoRepeats = 0)
Class : CRefDesArray
Parameters:
Str: CRefDes const &
NoRepeats: int
Add(Str)
Class : CRefDesArray