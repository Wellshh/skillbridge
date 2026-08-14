;; Acnsdesign.il
;;	Form interface for design constraints
;;

/*---------------------------------------------------------------------*/
/*-
#ifdef DOC_C
 NAME
	AcnsDesignDoc - design constraint UI form and AXL Interface
 SYNOPSIS
	This is the interface for the design constraint UI form. To
	add new items do the following:

	As of PSD15.1 this offers the same functionality as the
	Allegro cns design command
#endif
**/


; doing this prevents multiple instances of form from opening
unless(boundp('_AcDesignFw) _AcDesignFw = nil)

;----------------------------------------------------------------
;; GENERAL FORM PROGRAMMING METHOD
;; 		async form mode
;;
;; This is a good example on how to program a form.
;; 
procedure( AcnsDesignForm()
    prog( (fw position)	; need to do this since have a return

    ;; Good pratice
    ;; If form is open expose it and return
    fw = _AcDesignFw
    when( fw 
	axlUIWExpose(fw) 
	return(t)
    )

    position = '("CENTER")

    ;; no msg lines in form
    position = '("NE" "msglines" 1)

    ;; create a form handle, position form and set-up mode
    fw = axlFormCreate('_AcDesignFw "acns_design" position '_AcDesignCB t nil )

    ;; Set form fields to starting values
    fw->_change = t	; force apply to be disabled
    fw->_cnsDsnSep = "."
    fw->_cnsDsnValue = "value"

    _AcDesignTier(fw)
    _AcDesignRefresh(fw)

    ;; Last thing to do is display the form
    axlFormDisplay(fw)

    _AcDesignEvent()
    )
)
    
;----------------------------------------------------------------------
; Need to blank out fields that are not available in the current
; tier of Allegro. Removing this function will NOT enable editing
; or viewing these constraints since this is controlled by the Allegro
; database. This just implements the UI support.

procedure( _AcDesignTier(fw)
    (let (constraints formConstraints result hide fSuffixes field sep)

    fSuffixes = list( fw->_cnsDsnValue
                        "on" "off" "batch"
                        "textm" "textv" )

    sep = fw->_cnsDsnSep

    ; list of constraints in form
    foreach( item fw->fields
        result = _AcDesignMember(item sep fw->_cnsDsnValue)
        when(result
            formConstraints = cons(result formConstraints)
        )
    )

    ; list of constraints in allegro
    constraints = axlCNSDesignValueGet(nil t)

    ; list of contraints in form that is not enabled in Allegro db
    ; for this tier -- ignore sklint about member warning
    hide = setof(item formConstraints !member(item constraints))
    foreach( item hide
        foreach( suffix fSuffixes
            field = sprintf(nil "%s%s%s" item sep suffix)
            axlFormSetFieldVisible(fw field 0)
        )
    )
))

procedure( _AcDesignMember(item sep fType)
    (let (parsed )
    parsed = parseString(item sep)
    when( cadr( parsed) == fType
        car(parsed)
    )
))


;----------------------------------------------------------------
; The next three items support interactive command processing
;       We are told to done ourself so another cmd can start
procedure( _AcDesignDone(fw)
    when(fw && fw->_change
        ; hide form so user can access stop button
        axlUIWShow(fw 'hide)
        _AcDesignDoit(fw)
	fw->_change = nil       ; prevents double from axlEnterEvent
    )
    _AcDesignCancel(fw)
)

procedure( _AcDesignCancel(fw)
    when(fw
        axlFormClose(fw)
    )
)

; basically a dummy event processor so we can autodone the form
; in case the user starts another command. Maybe someday we can
; support selecting nets this way
;
; Autodone will always send in a done so check if done or cancel
; form should be called to save overhead of drc checking
;
; Use global form variable to avoid problem with form being closed
; via a form button which results in the DONE/CANCEL events being
; generated.

procedure( _AcDesignEvent()
    (let (event loop )

    loop = t
    while( loop
        event = axlEnterEvent('(PICK) "" nil)
        caseq(event->type
        (DONE
                _AcDesignDone(_AcDesignFw)
                loop = nil)
        (CANCEL
                _AcDesignCancel(_AcDesignFw)
                loop = nil)
        )
    )
))


procedure( _AcDesignAllSame(fw mode)
    (let (items field )

    items = axlCNSDesignModeGet(nil)
    ;; Give all fields default values
    foreach( item items
	field = strcat( get_pname(item) fw->_cnsDsnSep get_pname(mode)) 
        axlFormSetField(fw field t )
    )
    _AcDesignApplyGray(fw t)
))
    

; Update the fields to database values
procedure( _AcDesignRefresh(fw)
    (let (items modes field editable )

    items = axlCNSDesignModeGet('all)
    ;; Give all fields default values
    foreach( item items
	field = _cnsCreateModeField(fw item)
        axlFormSetField(fw field t )
    )

    ; grey out mode fields if in allegro studio (pcb)
    ;  buttons need to be made invisible since can't tell if they
    ;  are greyed
    editable = axlCNSDesignModeGet('editable)
    unless( editable
	modes = '(on off batch)
        foreach( mode modes
            axlFormSetFieldVisible(fw get_pname(mode) 0) )
    	foreach( item items
            foreach( mode modes
	    	field = _cnsCreateModeField(fw list(car(item) mode))
            	axlFormSetFieldEditable(fw field nil)
	    )
	)
	axlFormSetField(fw "modemsg" "  DRC mode control not available in this product.")
    )

    items = axlCNSDesignValueGet('all t)
    foreach( item items
	field = strcat( get_pname(car(item)) fw->_cnsDsnSep fw->_cnsDsnValue) 
        axlFormSetField(fw field cadr(item) )
    )


    _AcDesignApplyGray(fw nil)
))

; Gray test for the apply button depending if user has changed form
procedure( _AcDesignApplyGray(fw enable)
    unless(fw->_change == enable
	fw->_change = enable
        axlFormSetFieldEditable(fw "apply" enable )
    )
)

; Insure user value is correct
procedure( _AcDesignValidate(fw)
    (prog (result err newValue, constraint parsed)
	parsed = parseString(fw->curField fw->_cnsDsnSep)
	constraint = car(parsed)
	if(( cadr(parsed) == fw->_cnsDsnValue) then
	    result = axlCNSDesignValueCheck(constraint fw->curValue)
	    unless( result
                axlFormRestoreField(fw fw->curField)
		return()
	    )
	    newValue = car(result)	
	    err = cadr(result)
	    
            cond(
            (err == t
		axlFormSetField(fw fw->curField newValue)
		_AcDesignApplyGray(fw t)
                )
            (t
                ; because the error string may have "%" signs need
                ;       to do a default format
                axlUIWPrint(fw 'error "%s" err)
                axlFormRestoreField(fw fw->curField)
                )
            )

	else
	    _AcDesignApplyGray(fw t)
	)
))

;
; Since we don't do the change until the user hits done or apply.
; Here we just insure that any value fields are legal and we enable
; the apply button

; Return t if radio button is set
procedure( _AcDesignModeSet(fw prop mode)
        axlFormGetField(fw strcat( prop fw->_cnsDsnSep mode))
)

; Send user changes to database
procedure( _AcDesignDoit(fw)
    (let (items prop field value modeSet )

    ; send message to both form and Allegro main windo
    axlUIWPrint(nil 'info axlFormMsg(fw "drcstart"))
    axlCNSMapClear()

    ; check for value changes

    items = axlCNSDesignValueGet('all t)
    foreach( item items
	prop = car(item)
	field = strcat( get_pname(prop) fw->_cnsDsnSep fw->_cnsDsnValue) 
        value = axlFormGetField(fw field)
	unless( (value == cadr(item))
	    axlCNSDesignValueSet(prop value)
	)
    )

    items = axlCNSDesignModeGet('all)
    foreach( item items
	field = _cnsCreateModeField(fw item)
        value = axlFormGetField(fw field)

	; user has changed mode
	unless( value
	    prop = get_pname(car(item))
	    modeSet = exists( mode '("on" "off" "batch")
		    axlFormGetField(fw strcat( prop fw->_cnsDsnSep mode)))

	    ; exists returns the tail of the list, the 1st element is the one we want
	    modeSet = car(modeSet)
	    when( modeSet
	        axlCNSDesignModeSet(car(item) modeSet))
	)
    )

    axlCNSMapUpdate()
    axlUIWPrint(nil 'info axlFormMsg(fw "drcdone"))
))

procedure( _AcDesignCB(fw)

    case(fw->curField
    ("done"
	_AcDesignDone(fw)
	axlFinishEnterFun()
    )
    ("cancel"
	_AcDesignCancel(fw)
	axlCancelEnterFun()
    )
    ("apply"
	_AcDesignDoit(fw)
	_AcDesignApplyGray(fw nil)
    )
    ("on"
	_AcDesignAllSame(fw 'on)
    )
    ("off"
	_AcDesignAllSame(fw 'off)
	_AcDesignApplyGray(fw t)
    )
    ("batch"
	_AcDesignAllSame(fw 'batch)
    )
    (t
	_AcDesignValidate(fw)
    )
))

; create from a list field name <prop>.<mode>
procedure( _cnsCreateModeField(fw _arg)
	strcat( get_pname(car(_arg)) fw->_cnsDsnSep get_pname(cadr(_arg))) 
)
