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




;; 
(defun ashSelect (procFuncs "g")
    "Select Allegro objects and call user provided function"

    (let ((selDone nil) cmdTconc cmdList selSet)
	(setq cmdTconc (BuildProcList nil procFuncs))

	(cond
	    ((and cmdTconc (setq cmdList (car cmdTconc)))
		(axlSetFindFilter ?enabled '("NOALL" "ALLTYPES" "NAMEFORM") 
				  ?onButtons "ALLTYPES")

		(while (axlSelect)
		    (cond
			((setq selSet (axlGetSelSet))
			    (printf "ashSelect: %L\n" selSet)
			    (mapc 'errsetstring cmdList))
			(t
			    (println "ashSelect:  No Elements Found"))))

	    (t nil))))


(defun BuildProcList (procList funcs)
    (cond
	((null funcs)
	    procList)
	((stringp funcs)
	    (tconc procList (buildString (list "(" funcs " selSet" ")") " ")))
	((listp funcs)
	    (BuildProcList (BuildProcList procList (car funcs)) (cdr funcs)))
	(t nil)))


(defun _ashSelectDebug () (ashSelect "_axlDebugObjList"))

