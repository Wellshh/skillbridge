;###############################################################################
;                                                                              #
;                      Command: cline2shape                                    #
;                   Skill File: cline2shape.il                                 #
;               How To Execute: Command> cline2shape                           #
;                                                                              #
;  DISCLAIMER:                                                                 #
;       The user of this command assumes all responsibility and does not       #
;       hold Cadence Design Systems nor the author of this code for any        #
;       unwarranted results or problems due to the use of this code.           #
;                                                                              #
;       This is non-supported code and the user may modify it as needed.       #
;                                                                              #
;###############################################################################

; demostrates
;	1) style for an interactive command
;	2) use of the database tranasction APIs
;	3) two styles of undo/redo support
; Added undo support

;  Know Bug: Sometimes the program will not convert all cline segments but it 
;            will DELETE all segments.  Use at your OWN discretion!
;            Select Cancel or Undo before exiting the command to restore  
;            to original Clines.




axlCmdRegister("cline2shape" 'LCB_cline_to_shape ?cmdType "interactive"
 ?doneCmd 'LCB_Done ?cancelCmd 'LCB_Cancel ?undo t)
axlCmdRegister("cline2shape2" 'LCB_cline_to_shape2 ?cmdType "interactive"
 ?doneCmd 'LCB_Done ?cancelCmd 'LCB_Cancel ?undo t)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; This shows undo where all of the conversions that this user does while
; in the command a undone as a single operation.
;	To convert an existing command to support undo this method is
;	typically easier.

procedure(LCB_cline_to_shape()
let( (lclines layer polydbid )

  LCB_Setup()

  ; cannot have a global transaction if we want undo to roll back each operation
  LCB_mark = axlDBTransactionStart()

  LCBnotDone = t
  while( LCBnotDone
      lclines = axlGetSelSet(axlSelect(?prompt "Select Clines to convert to a shape."))

      foreach( clinedbid lclines
            layer = clinedbid->layer
            polydbid = axlPolyFromDB(clinedbid ?endCapType "ROUND")

            axlDeleteObject(clinedbid)

            unless( axlDBCreateShape(car(polydbid) t layer)  
                axlUIWPrint(nil "ERROR: Failed to create Shape from Cline.")
            )
            when( cadr(polydbid) 
                axlDBCreateShape(cadr(polydbid) t layer) 
            )
     )

     ; marks are only required if undo is using rolling back all database changes
     ; when command is active. When undoing each conversion this is not needed
     ; nor is Oops functional.
     when(LCB_mark axlDBTransactionMark(LCB_mark))
  )
  LCB_Done() ; just in case
))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; This shows undo where each conversion is supported as seperate undo operation
; in the command a undone as a single operation.
;	To convert an existing command to support undo this method is
;	typically easier.

procedure(LCB_cline_to_shape2()
let( (lclines layer polydbid doMark )

  LCB_Setup()

  ; cannot have a global transaction if we want undo to roll back each operation

  LCBnotDone = t
  doMark = 'undoMark

  while(LCBnotDone
      lclines = axlGetSelSet(axlSelect(?prompt "Select Clines to convert to a shape."))

      ; need to do a start/commit for each operation if we want undo to 
      ; rollback each change. This mostly disables Oops
      ;	  don't want to start a transaction unless we have work to do or it will
      ;   do a unneeded undoMark. 
      when(lclines 
          LCB_mark = axlDBTransactionStart(doMark)
      )

      foreach( clinedbid lclines
            layer = clinedbid->layer
            polydbid = axlPolyFromDB(clinedbid ?endCapType "ROUND")

            axlDeleteObject(clinedbid)

            unless( axlDBCreateShape(car(polydbid) t layer) 
                axlUIWPrint(nil "ERROR: Failed to create Shape from Cline.")
            )
            when( cadr(polydbid) 
                axlDBCreateShape(cadr(polydbid) t layer) 
            )
     )

     ; marks are only required if undo is using rolling back all database changes
     ; when command is active. When undoing each conversion this is not needed
     ; nor is Oops functional.
     when(LCB_mark axlDBTransactionCommit(LCB_mark))
     LCB_mark = nil
  )
  LCB_Done() ; just in case
))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;; support APIs

procedure(LCB_Setup()
let( (popup)
  axlSetFindFilter(?enabled list("noall" "clines") 
                  ?onButtons list("noall" "clines"))

  popup = axlUIPopupDefine( nil (list
    (list "Done" 'LCB_Done)
    (list "Oop" 'LCB_Oops)
    (list "Cancel" 'LCB_Cancel)
     ))

  ; Snapping is not required by this command but this shows the ability
  ; to add the snap sub-menu to the Right Mouse Popup menu
  axlSnapEnableAtRMB()

  axlUIPopupSet(popup)
  LCB_mark = nil
))

procedure(LCB_Oops()
  when(LCB_mark
    if(! axlDBTransactionOops(LCB_mark) then
      axlUIWPrint(nil "-- Nothing Left To oops. --")
    else
      axlUIWPrint(nil "-- Replacing Clines. --")
    )
  )
  axlClearSelSet()
)

procedure(LCB_Cancel()
  axlUIWPrint(nil "** Cancelled Program. **")
  when( LCB_mark axlDBTransactionRollback(LCB_mark))
  LCB_mark = nil
  LCBnotDone = nil
  axlClearSelSet()
  axlCancelEnterFun()
)


procedure(LCB_Done()
  when( LCB_mark axlDBTransactionCommit(LCB_mark))
  LCB_mark = nil
  LCBnotDone = nil
  axlCancelEnterFun()
)
