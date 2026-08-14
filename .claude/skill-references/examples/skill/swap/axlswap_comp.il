;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ; file.cc --
 ;
 ; Author --
 ;	Cadence Design Systems
 ;
 ; Function --
 ;	
 ; Copyright, 1993, Cadence Design Systems, Inc.
 ; No part of this file may be reproduced, stored in a retrieval system,
 ; or transmitted in any form or by any means --- electronic, mechanical,
 ; photocopying, recording, or otherwise --- without prior written permission
 ; of Cadence Design Systems, Inc.
 ;
 ; WARRANTY:
 ; NONE. NONE. NONE.
 ; Use all material in this code at your own risk.  Cadence Design Systems 
 ; makes no claims about any material in this archive.  These examples may
 ; not function or may only function in specific instances. We'd like to hear 
 ; what you think of our approach to this, and how we can improve it.
 ;
 ; RESTRICTIONS:
 ; All software contained within this archive is in the public domain or
 ; the author has given us permission for redistribution.  Some packages
 ; have explicit copyrights and notices concerning their redistribution.
 ; Please carefully read all documentation with any package on this tape.
 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
 ; file.cc --
 ;
 ; Author --
 ;	Cadence Design Systems
 ;
 ; Function --
 ;	
 ; Copyright, 1993, Cadence Design Systems, Inc.
 ; No part of this file may be reproduced, stored in a retrieval system,
 ; or transmitted in any form or by any means --- electronic, mechanical,
 ; photocopying, recording, or otherwise --- without prior written permission
 ; of Cadence Design Systems, Inc.
 ;
 ; WARRANTY:
 ; NONE. NONE. NONE.
 ; Use all material in this code at your own risk.  Cadence Design Systems 
 ; makes no claims about any material in this archive.  These examples may
 ; not function or may only function in specific instances. We'd like to hear 
 ; what you think of our approach to this, and how we can improve it.
 ;
 ; RESTRICTIONS:
 ; All software contained within this archive is in the public domain or
 ; the author has given us permission for redistribution.  Some packages
 ; have explicit copyrights and notices concerning their redistribution.
 ; Please carefully read all documentation with any package on this tape.
 ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;



(setq form_file "swap_component.form")
;
; build the popup menu
;
(defun _build_popup ()

    (let (user_data swap_pop)

    	(setq userdata (axlUIGetUserData))
	(setq swap_pop (axlUIPopupDefine userdata->popupId
			(list (list "Swap" '_swapCB))))
	(axlUIPopupSet swap_pop)
    )
)

;
; callback for swap button; only attempt swap if at least two components
; have been selected
;
(defun _swapCB ()

	; swap components if at least two components have been 
	; selected

    	(cond
	    ((lessp (axlGetSelSetCount) 2)
		(printf "Must select two components before swapping"))
	    (t (_do_swap (axlGetSelSet) form)))
)

;
; callback for cancel button.
;
(defun _cancel_cmd ()

    (axlCancelEnterFun)
)

;
; callback for done button; if two components have been selected, 
; swap before exiting command.
;
(defun _done_cmd ()

    (_do_swap (axlGetSelSet) form)
    (axlCancelEnterFun)
)

(defun _compName (sym_inst "o")

    (cond
	(sym_inst->refdes sym_inst->refdes)
	(t (buildString (list "SYM:" sym_inst->name) " ")))
)

;
; adds currently selected component to list of components
; 
(defun _set_form_name_fields (form)

    (let ((selSet (axlGetSelSet)))
	(case (length selSet)
	    (0
		(axlFormSetField form "comp1" "")
		(axlFormSetField form "comp2" ""))
	    (1
		(axlFormSetField form "comp1" (_compName (car selSet)))
		(axlFormSetField form "comp2" ""))
	    (2
		(axlFormSetField form "comp1" (_compName (car selSet)))
		(axlFormSetField form "comp2" (_compName (cadr selSet)))))))


;
; routine to perform swap of components - calls axlSwapSymbols
; to actually swap the physical symbols
;
(defun _do_swap (swap_list form)
    (when (greaterp (length swap_list) 1)
	(printf "I- Performing swap of %s and %s\n" 
		(_compName (car swap_list)) 
		(_compName (cadr swap_list)))

	; swap the components and then remove those components just
	; swapped from the selection set

	(axlSwapSymbols swap_list)
	(axlClearSelSet)

	(axlFormSetField form "comp1" "")
	(axlFormSetField form "comp2" "")
    )
)

(defun _select_comp_by_name (refdes)
    (cond
	((null (axlAddSelectName "SYMBOL" refdes))
	    (printf "E- Component %s not found\n" refdes)
	    nil)
	(t t)))

;
; callback routine used by form
;
(defun _swap_callback (form)
    (case form->curField
	("comp1" 
	    (let (selSet)
		(setq selSet (axlGetSelSet))
		(axlClearSelSet)
		(cond
		    ((null (_select_comp_by_name form->curValue))
			(axlAddSelectObject selSet))
		    (t
			(when (greaterp (length selSet) 1)
			    (axlAddSelectObject (cadr selSet)))))
		(_set_form_name_fields form)))
	("comp2" 
	    (let (selSet)
		(setq selSet (axlGetSelSet))
		(when (greaterp (length selSet) 1)
		    (axlSubSelectObject (cadr selSet)))
		(when (null (_select_comp_by_name form->curValue))
		    (axlAddSelectObject (cadr selSet)))
		(_set_form_name_fields form))))
)

;
; main routine for swap component
;
(defun axlSwapComponent ()

    (axlClearSelSet)
    (axlSetFindFilter ?enabled `("NOALL" "SYMBOLS") ?onButtons `("SYMBOLS"))

    (let (form point prevSelSet newSelection)

	; build the popup menu, then create and display form

	(_build_popup)

	(setq form (axlMiniStatusLoad (gensym) form_file 
				  `_swap_callback t))

	; while not cancel or done, allow user to select components

	(while (setq point (axlEnterPoint ?prompts 
					  `("Select component to swap")))
	    (setq prevSelSet (axlGetSelSet))
	    (cond
		((greaterp (length prevSelSet) 1)
		    (axlSingleSelectPoint point)
		    (setq newSelection (axlGetSelSet))
		    (printf "%L\n" newSelection)
		    (_do_swap prevSelSet form)
		    ;axlSingleSelectObject due to temp swap side effect
		    ; it clears the selection set
		    (axlSingleSelectObject newSelection)
		    (_set_form_name_fields form))
		(t 
		    (axlAddSelectPoint point)
		    (_set_form_name_fields form))))

	(axlClearSelSet)))

