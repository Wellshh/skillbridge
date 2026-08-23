;  demostrates method for using axlUIWTimerAdd and Form Progress control
;  requires form file timer_example.form

procedure( timer()
     ; set up a continuous timer using the main window
     timerId = axlUIWTimerAdd(nil 2000 nil 'timerCB)
     timerId->yourData =  "My data"
     t
)

procedure( timerOne()
     ; set up a one shot timer
     timerId = axlUIWTimerAdd(nil 2000 t 'timerCB)
     timerId->yourData =  "One shot"
     t
)

procedure( timerCB( window timerId elapsedTime)
      printf("Timer CB- %L \"%s\" %d\n" window timerId->yourData elapsedTime)
)

;--------------------------------------------------------------------------------

; shows how to use axlUIWTimerAdd with a form's PROGRESS control
unless(boundp('timerFw) timerFw = nil)

procedure( timerFormCB(fw)
   case(fw->curField
	("close"
		axlUIWTimerRemove(fw->_timerId)
		axlFormClose(fw))
   )
)

procedure( timerCBForForm( window timerId elapsedTime)
      timerId->_cnt = timerId->_cnt +1
      axlFormSetField(timerId->_fw "count" timerId->_cnt)
      ; step progress meter
      axlFormSetField(timerId->_fw "progress" nil)
)

procedure( timerForm()
    let((fw)
     fw = axlFormCreate( 'timerFw "timer_example" '("C" "INNER" "MSGLINES" 0) 'timerFormCB
			nil)
     timerId = axlUIWTimerAdd(nil 2000 nil 'timerCBForForm)
     timerId->_fw = fw
     timerId->_cnt = 0
     fw->_timerId = timerId

     axlFormSetField(fw "progress" '(5 100 1))
     axlFormDisplay(fw)
))
