# Class: DboValidValuesIter

START class DboValidValuesIter

---

NextValue(name, status, NeedBundle = False) : returns int
Class : DboValidValuesIter
Parameters:
name: CString &
status: DboState &
NeedBundle: int
NextValue(name, status) : returns int
Class : DboValidValuesIter
Parameters:
name: CString &
status: DboState &
END class DboValidValuesIter
START class DboDefinition
END class DboDefinition
START class DboPointerException
what() : returns char
Class : DboPointerException
Parameters:
END class DboPointerException
START class DboNullPointerException(DboPointerException):
what() : returns char
Class : DboNullPointerException(DboPointerException):
Parameters:
END class DboNullPointerException(DboPointerException):
START class DboInvalidPointerAccessException(DboPointerException):
what() : returns char
Class : DboInvalidPointerAccessException(DboPointerException):