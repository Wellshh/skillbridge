;;	
; Demostration of an in-line defined form descirption.
; in-line form defintion
;	this avoids to maintain a seperate .form file from the Skill code
;
; This is supported for:
; 	axlFormCreate -- see stand_inline (first example)
;	axlMinistatusLoad -- see mini_inline (second example

;----------------------------------------------------------------
;----------------------------------------------------------------
;----------------------------------------------------------------
; 1) Standalone form -- 

; form handle
unless(boundp('_mil_fw) _mil_fw = nil)
;
;
; Rules:
;	- every non-blank line must have a tab character
;	- any quote must be escaped (e.g. use the backslash '\')
;	- any paraenthesis '()' must be escaped '\'
inLineForm = '("

	FILE_TYPE=FORM_DEFN VERSION=2
	FORM
	FIXED
	PORT 16 4
	HEADER \"In-Line Example\"

	TILE

	TEXT \"I did it!\"
	TLOC 6 2
	OPTIONS BOLD
	ENDTEXT

	FIELD checkbox
	FLOC 2 4
	CHECKLIST \"A checkbox\"
	ENDFIELD

	FIELD done
	FLOC 4 8
	MENUBUTTON \"OK\" 9 3
	ENDFIELD
	ENDTILE

	ENDFORM
")



procedure( stand_inline()
    let( (fw)
    fw = axlFormCreate('_mil_fw list("myform" inLineForm) 
		'("msgLines" 0) 'mil_CB t nil)
    axlFormDisplay(fw)
))

; END PUBLIC FUNCTIONS
;----------------------------------------------------------------
; Open form
procedure( mil_grid(t_name)
    let( (f)
    )
)
 
;----------------------------------------------------------------
;; Form callback with grid control
procedure( mil_CB(fw)
    prog(()
     unless((fw->doneState == 0)
	 axlFormClose(fw)
	 return(t)
     )
))
 

;----------------------------------------------------------------
;----------------------------------------------------------------
;----------------------------------------------------------------
; 2) Options panel in-line method -- axlMiniStatusLoad

unless(boundp('_mini_fw) _mini_fw = nil)

procedure( mini_inline()
    let( (fw)
    fw = axlMiniStatusLoad('_mini_fw list("mini_test" inLineForm) 'mini_inlineCB)
))

procedure( mini_inlineCB(fw)
     ; note cannot close the form
     printf("CURFIELD %L has value %L\n" fw->curField, fw->curValue)
)

;mini_inline()
