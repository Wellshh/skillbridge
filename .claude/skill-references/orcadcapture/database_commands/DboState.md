# Class: DboState

19 Appendix B: Database Commands List
Refer to Database class hierarchy to understand how to find out all commands available on an object
type, including the commands available through class inheritance.
START class DboState
Succeeded() : returns int
Class : DboState
Parameters:
Failed() : returns int
Class : DboState
Parameters:
Severity() : returns int
Class : DboState
Parameters:
OK() : returns int
Class : DboState
Parameters:
Code() : returns int
Class : DboState
Parameters:
Message(msg)
Class : DboState
Parameters:
msg: CString &
GetExtendedText() : returns CString
Class : DboState
Parameters:
WriteToSessionLog(str)

---

Class : DboState
Parameters:
str: CString const &
WriteToStatusBar(str)
Class : DboState
Parameters:
str: CString const &
GetOptionString(lOptionName, defaultValue) : returns CString
Class : DboState
Parameters:
lOptionName: CString const &
defaultValue: CString const &
END class DboState
DboState_WriteToSessionLog(str)
Parameters:
str: CString const &
DboState_WriteToStatusBar(str)
Parameters:
str: CString const &
DboState_GetOptionString(lOptionName, defaultValue) : returns CString
Parameters:
lOptionName: CString const &
defaultValue: CString const &
START class DboValue
GetString(Value) : returns DboState
Class : DboValue
Parameters:
Value: CString &
GetInt(status) : returns int
Class : DboValue
Parameters: