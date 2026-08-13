# Class: DboDesignUpdateOccurrenceBlockerManager

START class DboDesignUpdateOccurrenceBlockerManager
Release(bDoMarkModified = False)
Class : DboDesignUpdateOccurrenceBlockerManager
Parameters:
bDoMarkModified: bool
Release()
Class : DboDesignUpdateOccurrenceBlockerManager
Parameters:
END class DboDesignUpdateOccurrenceBlockerManager
START class TBaseDboDesignOccurrencesIter(IterDefs):
GetType() : returns int
Class : TBaseDboDesignOccurrencesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboDesignOccurrencesIter(IterDefs):
Parameters:
Next(status) : returns DboBaseObject
Class : TBaseDboDesignOccurrencesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboDesignOccurrencesIter(IterDefs):

---

Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboDesignOccurrencesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboDesignOccurrencesIter(IterDefs):
START class DboDesignOccurrencesIter(TBaseDboDesignOccurrencesIter):
NextOccurrence(status) : returns DboInstOccurrence
Class : DboDesignOccurrencesIter(TBaseDboDesignOccurrencesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboDesignOccurrencesIter(TBaseDboDesignOccurrencesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboDesignOccurrencesIter(TBaseDboDesignOccurrencesIter):
Parameters:
pObject: DboInstOccurrence *&
END class DboDesignOccurrencesIter(TBaseDboDesignOccurrencesIter):
START class TBaseDboDesignSchematicOccurrencesIter(IterDefs):
GetType() : returns int
Class : TBaseDboDesignSchematicOccurrencesIter(IterDefs):
Parameters:
GetSource() : returns DboBaseObject
Class : TBaseDboDesignSchematicOccurrencesIter(IterDefs):
Parameters:

---

Next(status) : returns DboBaseObject
Class : TBaseDboDesignSchematicOccurrencesIter(IterDefs):
Parameters:
status: DboState &
SetFlag(flag, status)
Class : TBaseDboDesignSchematicOccurrencesIter(IterDefs):
Parameters:
flag: UINT
status: DboState &
Sort(status)
Class : TBaseDboDesignSchematicOccurrencesIter(IterDefs):
Parameters:
status: DboState &
END class TBaseDboDesignSchematicOccurrencesIter(IterDefs):
START class DboDesignSchematicOccurrencesIter(TBaseDboDesignOccurrencesIter):
HasOccurrences() : returns int
Class : DboDesignSchematicOccurrencesIter(TBaseDboDesignOccurrencesIter):
Parameters:
NextSchematicOccurrence(status) : returns DboInstOccurrence
Class : DboDesignSchematicOccurrencesIter(TBaseDboDesignOccurrencesIter):
Parameters:
status: DboState &
Next(status) : returns DboBaseObject
Class : DboDesignSchematicOccurrencesIter(TBaseDboDesignOccurrencesIter):
Parameters:
status: DboState &
GetKey(pObject) : returns unsigned long
Class : DboDesignSchematicOccurrencesIter(TBaseDboDesignOccurrencesIter):
Parameters:
pObject: DboInstOccurrence *&
END class DboDesignSchematicOccurrencesIter(TBaseDboDesignOccurrencesIter):