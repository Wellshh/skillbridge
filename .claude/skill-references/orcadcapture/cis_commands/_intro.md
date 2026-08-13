# Appendix C: CIS Commands List

size: int
CISGetColor(R, G, B) : returns unsigned long
Parameters:
R: int
G: int
B: int
SetCISRowColor(color) : returns char
Parameters:
color: unsigned long
SetCISTextColor(color) : returns char
Parameters:
color: unsigned long
AddCISCriteria(pFieldName, pValue, TextColor, RowColor) : returns char
Parameters:
pFieldName: char const *
pValue: char const *
TextColor: unsigned long
RowColor: unsigned long
ClearCISCriteria()
ClearCISColor()
SetCISMultiValuedField(aFieldName) : returns char
Parameters:
aFieldName: char const *
ClearMultiValuedField()
GetPartManagerView() : returns CPmgrListView
SelectGroup(pGroupName, pName, aRefDes)
Parameters:
pGroupName: char const *
pName: char const *
aRefDes: char const *