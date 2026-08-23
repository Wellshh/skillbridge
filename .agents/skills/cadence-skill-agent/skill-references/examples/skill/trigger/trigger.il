;; Demostration of Allegro Database Trigger use. 
;; This is available starting in Allegro 14.1

;; CALLBACKS
procedure( triggerOpen( t_open)
	let( (brd existing)
	brd = car(t_open)
	existing = cadr(t_open)
	if( existing then
	   existing = "Existing"
	else
	   existing = "New"
	)
	printf("SKILLCB Open %s database %s\n" existing brd)
	t
))

procedure( triggerOpen2( t_open)
	printf("SKILLCB Open 2! database %L\n" t_open)
	t
)

procedure( triggerClose( l_name )
	printf("SKILLCB Good Bye! %s\n" l_name) 
	t
)

procedure( triggerSave( l_save)
	let( (old new)

	old = car(l_save)
	new = cadr(l_save)
	printf("SKILLCB Saving database FROM %s TO %s\n" old new)
	t
))


procedure(myexit(t_exit)
    printf("Exit-TRIGGER err = %L\n" t_exit)
)
procedure(mymenu(t_open)
    printf("Menu-TRIGGER menu = %L\n" t_open)
)

procedure(myxprobe(items)
    ; 1st item is mode (highlight or dehighlight)
    ; 2nd item is list of dbids
    printf("XProbe-TRIGGER %L = %L\n" car(items) cadr(items))
)

;procedure(myselect(items)
    ;printf("P-TRIGGER %L = %L\n" car(items) cadr(items))
;)


;; SET/CLEAR FUNCTIONS
procedure( triggerSet( )

    ;; echo available triggers
    ;axlTriggerSet nil nil

    ;; try bad trigger name
    ;axlTriggerSet 'foo nil

    ;axlTriggerSet 'open 'fakefunction

    axlTriggerSet('open 'triggerOpen)
    axlTriggerSet('save 'triggerSave)

    ; try registering same function again
    ;axlTriggerSet('open 'triggerOpen)

    ; try registering same function again
    ;axlTriggerSet('open 'triggerOpen2)

    axlTriggerSet('close 'triggerClose)

    axlTriggerSet('exit 'myexit)
    axlTriggerSet('menu 'mymenu)
    axlTriggerSet('xprobe 'myxprobe)
    ;axlTriggerSet('select 'myselect)

    axlTriggerPrint()
)

procedure( triggerClear( )

    ;; echo available triggers
    ;axlTriggerClear nil nil
    ;axlTriggerClear 'clear 'foo
    ;axlTriggerClear 'open 'foo

    axlTriggerClear('open 'triggerOpen)
    axlTriggerClear('save 'triggerSave)
    axlTriggerPrint()
)


