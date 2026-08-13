# Class: DboVector(DboBaseObject):

status: DboState &
DboTitleBlock_sGetSourceLibName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboTitleBlock_sGetSourceSymbolName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboBaseObjectToDboVector(x) : returns DboVector
Parameters:
x: DboBaseObject *
START class DboVector(DboBaseObject):
GetObjectType() : returns ObjectTypeT
Class : DboVector(DboBaseObject):
Parameters:
GetOwner() : returns DboBaseObject
Class : DboVector(DboBaseObject):
Parameters:
GetContainingLib() : returns DboLib
Class : DboVector(DboBaseObject):
Parameters:
GetParentObj() : returns DboBaseObject
Class : DboVector(DboBaseObject):
Parameters:
END class DboVector(DboBaseObject):
DboVectorToDboBox(x) : returns DboBox
Parameters:
x: DboVector *