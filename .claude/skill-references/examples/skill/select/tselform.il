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



(setq tselAutoFormPass nil)

;; tselTestAutoForm - test if auto filter form works
;	Used with tselautoform.scr
(defun tselTestAutoForm ()
    (setq tselAutoFormPass nil)
    (axlCloseFindFilter)
    (cond
	((axlFindFilterIsOpen)
	    (printf "tselTestAutoForm: could not close find filter form\n")
	    nil)
	(t
	    ;mix case in AUTOFORM to test this feature
	    (axlSetFindFilter ?enabled '("NOALL" "AuToForm" "ALLTYPES") 
		      ?onButtons "ALL")
	    (axlAddSelectPoint)

	    ; form should be closed now
	    (when (axlFindFilterIsOpen)
		(setq tselAutoFormPass nil))

	    ;reset AUTOFORM and make sure it does not open
	    (axlSetFindFilter ?enabled "NOAUTOFORM")
	    (when (axlAutoOpenFindFilter)
		(setq tselAutoFormPass nil))

	    (tselEchoResults "Selset Auto Filter Form" tselAutoFormPass))))

;callback for tselTestAutoForm
(defun tselTestAutoForm_callback ()
    (cond
	((axlFindFilterIsOpen)
	    (setq tselAutoFormPass t))
	(t
	    (setq tselAutoFormPass nil)))
    (axlCancelEnterFun)
    t)

;; tselTestOnButtons - Test that we can interactively clear find filter bits.
; 	Test that setting find filter ?enabled does not affect
;	interactively cleared onButtons.
;	used with tselonbutton.scr
(defun tselTestOnButtons ()
    (let (testPass findFilter)
	(axlSetFindFilter ?enabled '("NOALL" "ALLTYPES")
			  ?onButtons "ALL")
	(axlOpenFindFilter)
	(axlAddSelectPoint)

	(cond
	    ; Test that we can interactively clear find filter bits.
	    ((setq findFilter (axlGetFindFilter t))
		(printf "tselTestOnButtons: onButtons not Cleared\n %L\n"
			findFilter))

	    ((null (axlSetFindFilter ?enabled "ALL"))
		(printf "tselTestOnButtons: Failed to Set Find Filter\n"))

	    ; Test that setting find filter ?enabled does not affect 
	    ;    interactively cleared onButtons
	    ((setq findFilter (axlGetFindFilter t))
		(printf "tselTestOnButtons: ?enabled changed onButtons\n %L\n"
			findFilter))
	    (t (setq testPass t)))

	(axlCloseFindFilter)
	(tselEchoResults "SelSet Form onButton Interactive Clear" testPass)))
