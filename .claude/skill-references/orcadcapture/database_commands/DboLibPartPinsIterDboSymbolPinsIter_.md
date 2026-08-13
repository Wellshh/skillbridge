# Class: DboLibPartPinsIter(DboSymbolPinsIter):

obj: DboBaseObject *
status: DboState &
DboLibPart_sGetReferenceDesignator(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetPartValue(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetContentsLibName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetContentsViewName(obj, status) : returns CString
Parameters:
obj: DboBaseObject *
status: DboState &
DboLibPart_sGetContentsViewType(obj, status) : returns ViewTypeT
Parameters:
obj: DboBaseObject *
status: DboState &
DboSymbolPinsIterToDboLibPartPinsIter(x) : returns DboLibPartPinsIter
Parameters:
x: DboSymbolPinsIter *
START class DboLibPartPinsIter(DboSymbolPinsIter):
NextPin(status) : returns DboSymbolPin
Class : DboLibPartPinsIter(DboSymbolPinsIter):
Parameters:
status: DboState &
END class DboLibPartPinsIter(DboSymbolPinsIter):