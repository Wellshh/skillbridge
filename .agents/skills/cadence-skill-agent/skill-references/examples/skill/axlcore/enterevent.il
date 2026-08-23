/*INDENT OFF*/
/*------------------------------------------------------------------------*/
/*-
 *	Cadence Design Systems
 * (c) 2013 Cadence Design Systems, Inc. All rights reserved.
 * This work may not be copied, modified, re-published, uploaded, 
 * executed, or distributed in any way, in any medium, whether in 
 * whole or in part, without prior written permission from Cadence 
 * Design Systems, Inc.
 *
 */
/*------------------------------------------------------------------------*/

; ExampleEvent: axlEnterEvent and using axlUI...Popup... to define a RMB popup
;	with EventMask can define mouse operations of interest. Example code
;	has pick and double pick. Another mask returns cursor movement.
;	Disables snap to object RMB via axlSnapDisableAtRMB
;	See axlEnterEvent for additional mask options.
;
; ExampleNoSnap same as above except 
;	Allows snap to object RMB via axlSnapEnableAtRMB


/*INDENT ON*/

procedure( EnterDone()
    printf("Done Func\n")
    axlCancelEnterFun()
)

procedure( EnterCancel()
    printf("Cancel Func\n")
    axlCancelEnterFun()
)


procedure( ExampleEvent()
   let( (eventMask event loop popUp)
    eventMask = '( PICK DBLPICK MOVE )
    eventMask = '( PICK DBLPICK )

    popUp = axlUIPopupDefine(nil
		 list(
		 list("Done" 'EnterDone)
		 list("MENU_SEPARATOR" nil)
		 list("Cancel" 'EnterCancel)
		 ))
    ; do no want Snap items on RMB
    axlSnapDisableAtRMB()
    axlUICmdPopupSet(popUp)

    loop = t
    while( loop
	event = axlEnterEvent(eventMask "Perform pick or popup" t)
	lastEvent = event
	; Event has members; objType, type, xy, xySnap, command, time

	printf("EVENT %L xy=%L snap=%L cmd=%L\n" event->type event->xy event->xySnap event->command )
	case(event->type
	('DONE ; cleanup
		loop = nil)
	('CANCEL ; cleanup
              loop = nil)
	)
    )
))

procedure( ExampleSnap()
   let( (eventMask event loop popUp)
    eventMask = '( PICK DBLPICK MOVE )
    eventMask = '( PICK DBLPICK )

    popUp = axlUIPopupDefine(nil
		 list(
		 list("Done" 'EnterDone)
		 list("Cancel" 'EnterCancel)
		 ))

    ; want Snap items on RMB
    axlSnapEnableAtRMB()
    axlUICmdPopupSet(popUp)

    loop = t
    while( loop
	event = axlEnterEvent(eventMask "Perform pick or popup" nil)
	lastEvent = event
	; Event has members; objType, type, xy, xySnap, command, time

	printf("EVENT %L xy=%L snap=%L cmd=%L\n" event->type event->xy event->xySnap event->command )
	case(event->type
	('DONE ; cleanup
		loop = nil)
	('CANCEL ; cleanup
              loop = nil)
	('PICK 
	   saveEvent = event)
	)
    )
))
