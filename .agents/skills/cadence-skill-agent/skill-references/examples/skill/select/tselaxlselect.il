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



;; tselaxlSelect - test axlSelect functionality
(defun tselaxlSelect ()
    (let ((testPass t) testDone count cmdData)
	(axlClearSelSet)
	(axlSetFindFilter ?enabled '("NOALL" "ALLTYPES" "NAMEFORM")
			  ?onButtons "ALLTYPES")
				
	(axlOpenFindFilter)
	(_tselMakeListFiles)

	(while (null testDone)
	    (cond
		((axlSelect)
		    (printf "tselaxlSelect: Found %L Objects\n" 
			    (axlGetSelSetCount))
		    (mapc 'ashPrintObjData (axlGetSelSet)))

		((greaterp 0 (setq count (axlGetSelSetCount)))
		    (printf "tselaxlSelect: Nil axlSelect, %L Objects in set\n"
			    count)
		    (mapc 'ashPrintObjData (axlGetSelSet))
		    (setq testPass nil)
		    (setq testDone t))

		((eq (axlUIGetUserData)->doneState 'done)
		    (printf "tselaxlSelect:  \"Done\" Aborted axlSelect\n"))

		((eq (axlUIGetUserData)->doneState 'cancel)
		    (printf "tselaxlSelect:  \"Cancel\" Aborted axlSelect\n")
		    (setq testDone t))

		(t 
		    (printf "tselaxlSelect:  Unknown axlSelect abort\n")
		    (setq testPass nil)
		    (setq testDone t))))

	(_tselDeleteListFiles)
	(tselEchoResults "Selset axlSelect Test" testPass)))

(defun _tselMakeListFiles ()
    (_tselMakeListFile "./net.lst" '("SIG108" "SIG100"))
    (_tselMakeListFile "./refdes.lst" '("C25" "c26")))

(defun _tselMakeListFile (fileName nameList)
    (let (listFile)
	(cond
	    ((null (setq listFile (outfile fileName)))
		(printf "_tselMakeListFiles:  Could not open %L\n" fileName))
	    (t
		(foreach name nameList
		    (fprintf listFile "%s\n" name))
		(close listFile)))) 
    t)

(defun _tselDeleteListFiles ()
    (deleteFile "./net.lst")
    (deleteFile "./refdes.lst"))

