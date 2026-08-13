# Class: DboPortInstDisplayPropsIter(DboDisplayPropsIter):

Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetHotSpotY(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboPortInstBusMember_sGetPinPosition(obj, status) : returns int
Parameters:
obj: DboBaseObject *
status: DboState &
DboDisplayPropsIterToDboPortInstDisplayPropsIter(x) : returns DboPortInstDisplayPropsIter
Parameters:
x: DboDisplayPropsIter *
START class DboPortInstDisplayPropsIter(DboDisplayPropsIter):
Next(status) : returns DboBaseObject
Class : DboPortInstDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboPortInstDisplayPropsIter(DboDisplayPropsIter):
Parameters:
pObject: DboDisplayProp *&
NextProp(status) : returns DboDisplayProp
Class : DboPortInstDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &
NextPropEx(status) : returns DboDisplayProp
Class : DboPortInstDisplayPropsIter(DboDisplayPropsIter):
Parameters:
status: DboState &

---

END class DboPortInstDisplayPropsIter(DboDisplayPropsIter):
DboEffectivePropsIterToDboPortInstEffectivePropsIter(x) : returns DboPortInstEffectivePropsIter
Parameters:
x: DboEffectivePropsIter *
START class DboPortInstEffectivePropsIter(DboEffectivePropsIter):
NextEffectiveProp(Name, Value, nType, bEditable) : returns DboState
Class : DboPortInstEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
NextEffectiveProp(Name, Value, nType, bEditable, bDeletable) : returns DboState
Class : DboPortInstEffectivePropsIter(DboEffectivePropsIter):
Parameters:
Name: CString &
Value: CString &
nType: DboValue::ValueType &
bEditable: int &
bDeletable: int &
END class DboPortInstEffectivePropsIter(DboEffectivePropsIter):
DboGraphicInstanceToDboNetSymbolInstance(x) : returns DboNetSymbolInstance
Parameters:
x: DboGraphicInstance *
START class DboNetSymbolInstance(DboGraphicInstance):
GetSymbol(status) : returns DboSymbol
Class : DboNetSymbolInstance(DboGraphicInstance):
Parameters:
status: DboState &
GetHotSpot(status) : returns CPoint
Class : DboNetSymbolInstance(DboGraphicInstance):