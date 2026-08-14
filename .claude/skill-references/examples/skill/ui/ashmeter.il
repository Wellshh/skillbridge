
; Demonstration of axlMeterCreate with callback function plus
;	user specified form file to add addition button
; also requires form file ashmeter.form in same directory
axlCmdRegister("metertest" 'ash_meterform)

procedure(ash_meterform()
  let( (meterfile)
  
   ;; Custom meter form file.
   meterfile = "ashmeter"
  
   ;; Create the meter display with a user defined callback function.
   axlMeterCreate("Test Meter Form" "Info1 line" t meterfile "" '_ashMeterCallback )
))

; mhandle is the form handle -- see documentation in axlFormCreate
procedure(_ashMeterCallback(mhandle)
  let( ()
    axlMsgPut("-- formhandle is %L" mhandle->??)
    
    (case mhandle->curField
    ("info"
        axlMsgPut("-- User selected the Info button.")
    )
    )
))
