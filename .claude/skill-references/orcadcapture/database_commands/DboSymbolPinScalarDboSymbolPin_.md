# Class: DboSymbolPinScalar(DboSymbolPin):

DboSymbolPinToDboSymbolPinScalar(x) : returns DboSymbolPinScalar
Parameters:
x: DboSymbolPin *
START class DboSymbolPinScalar(DboSymbolPin):
GetObjectType() : returns ObjectTypeT
Class : DboSymbolPinScalar(DboSymbolPin):
Parameters:
END class DboSymbolPinScalar(DboSymbolPin):
DboSymbolPinToDboSymbolPinBus(x) : returns DboSymbolPinBus
Parameters:
x: DboSymbolPin *
START class DboSymbolPinBus(DboSymbolPin):
GetObjectType() : returns ObjectTypeT
Class : DboSymbolPinBus(DboSymbolPin):
Parameters:
SetPinName(name) : returns DboState
Class : DboSymbolPinBus(DboSymbolPin):
Parameters:
name: CString &
END class DboSymbolPinBus(DboSymbolPin):
DboDisplayPropsIterToDboSymbolPinDisplayPropsIter(x) : returns DboSymbolPinDisplayPropsIter
Parameters:
x: DboDisplayPropsIter *
START class DboSymbolPinDisplayPropsIter(DboDisplayPropsIter):
Next(status) : returns DboBaseObject
Class : DboSymbolPinDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &

---

GetKey(pObject) : returns unsigned long
Class : DboSymbolPinDisplayPropsIter(DboDisplayPropsIter):
Parameters:
pObject: DboDisplayProp *&
NextProp(status) : returns DboDisplayProp
Class : DboSymbolPinDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
NextPropEx(status) : returns DboDisplayProp
Class : DboSymbolPinDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
END class DboSymbolPinDisplayPropsIter(DboDisplayPropsIter):
START class DboFontAndRotation
GetFontID() : returns short
Class : DboFontAndRotation
Parameters:
GetRotation() : returns RotationT
Class : DboFontAndRotation
Parameters:
SetFontID(nFontID)
Class : DboFontAndRotation
Parameters:
nFontID: short
SetRotation(nRotation)
Class : DboFontAndRotation
Parameters:
nRotation: enum DboValue::RotationT
END class DboFontAndRotation
DboBaseObjectToDboDisplayProp(x) : returns DboDisplayProp