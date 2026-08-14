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
	    (t (_do_swap (axlGetSelSet))))
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

    (_do_swap (axlGetSelSet))
    (axlCancelEnterFun)
)

(defun _compName (sym_inst "o")

    (cond
	(sym_inst->refdes sym_inst->refdes)
	(t (buildString (list "SYM:" sym_inst->name) " ")))
)

;
; routine to perform swap of components - calls axlSwapSymbols
; to actually swap the physical symbols
;
(defun _do_swap (swap_list)
    (when (greaterp (length swap_list) 1)
	(printf "I- Performing swap of %s and %s\n" 
		(_compName (car swap_list)) 
		(_compName (cadr swap_list)))

	; swap the components and then remove those components just
	; swapped from the selection set

	(axlSwapSymbols swap_list)))

; main routine for swap component
;
(defun axlSwapComponent ()

    (axlClearSelSet)
    (axlSetFindFilter ?enabled `("NOALL" "NAMEFORM" "SYMBOLS") 
		  ?onButtons `("SYMBOLS"))
    (axlOpenFindFilter)

    (let ((prevSelSet nil))

	; build the popup menu
	(_build_popup)

	(while (axlSelect ?multiDisable t)
(printf "%L\n" (axlGetSelSet))
	    (cond
		((null prevSelSet)
		    nil)
		((greaterp (length prevSelSet) 1)
		    (_do_swap prevSelSet))
		(t
		    (axlAddSelectObject prevSelSet)))

	    (setq prevSelSet (axlGetSelSet)))


        (axlCloseFindFilter)
	(axlClearSelSet)))

