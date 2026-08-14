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



;; Test execute path for AXL select functions when selset no initialized
;  This must be the first test after allegro has been brought up
;  The results of this test are less important than not crashing because the
;  selection set has not been initialized.

(defun tsetPreInitTest ()
    (let (testPass)
	(cond
	    ((axlGetFindFilter)
		nil)
	    ((axlOpenFindFilter)
		nil)
	    ((axlAutoOpenFindFilter)
		nil)
	    ((axlFindFilterIsOpen)
		nil)
	    ((axlCloseFindFilter)
		nil)

	    ((axlGetSelSet)
		nil)
	    ((axlGetSelSetCount)
		nil)

	    ((axlAddSelectPoint '(100 100))
		nil)
	    ((axlSingleSelectPoint '(100 100))
		nil)
	    ((axlSubSelectPoint '(100 100))
		nil)

	    ((axlAddSelectBox '((100 100) (200 200)))
		nil)
	    ((axlSingleSelectBox '((100 100) (200 200)))
		nil)
	    ((axlSubSelectBox '((100 100) (200 200)))
		nil)

	    ((axlAddSelectAll)
		nil)
	    ((axlSubSelectAll)
		nil)

	    ((axlAddSelectName "NET" "*")
		nil)
	    ((axlSingleSelectName "NET" "*")
		nil)
	    ((axlSubSelectName "NET" "*")
		nil)

	    ((axlAddSelectObject nil)
		nil)
	    ((axlSingleSelectObject nil)
		nil)
	    ((axlSubSelectObject nil)
		nil)
    	    (t (setq testPass t)))

	(tselEchoResults "Selset Preinit Test" testPass)))
