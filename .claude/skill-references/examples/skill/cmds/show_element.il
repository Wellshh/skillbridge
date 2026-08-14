
; This demostrates the following:
;	 - use of right mouse popups (RMB)
;	 - simple selection
;	 - use of the findfilter

defun( ShowElement ()
   mypopup = axlUIPopupDefine(nil, list(list("Done" 'axlFinishEnterFun)
list("Cancel" 'axlCancelEnterFun)))
   axlUIPopupSet(mypopup)
   axlSetFindFilter(?enabled, '("NOALL", "ALLTYPES", "NAMEFORM")
?onButtons "ALLTYPES")
   while(axlSelect(), axlShowObject(axlGetSelSet()))
)

axlCmdRegister("myshow" 'ShowElement ?cmdType "interactive")

