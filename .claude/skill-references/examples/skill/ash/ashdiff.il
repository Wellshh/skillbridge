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


(defun ashDiffObjList (listA listB)
    (let (shortList longList diffList shortL longL (shortCount 1) (longCount 1))
	(cond
	    ((greaterp (length listA) (length listB))
		(setq shortL "B")
		(setq longL "A")
		(setq longList listA)
		(setq shortList listB))
	    (t
		(setq shortL "A")
		(setq longL "B")
		(setq shortList listA)
		(setq longList listB)))
    
	(while longList
	    (cond
		((eq (car shortList) (car longList))
		    (setq shortCount (plus shortCount 1))
		    (setq shortList (cdr shortList)))
		((equal (car shortList) (car longList))
		    (printf "%s%L/%s%L \"equal\" but not \"eq\"\n\t"
			    shortL shortCount longL longCount)
		    (ashPrintObjData (car shortList))
		    (setq shortCount (plus shortCount 1))
		    (setq shortList (cdr shortList)))
		(t
		    (printf "%s%L/%s%L\t" shortL shortCount longL longCount)
		    (ashPrintObjData (car longList))))

	    (setq longList (cdr longList))
	    (setq longCount (plus longCount 1)))

	(when shortList
	    (printf "list%s Remainder\n" shortL)
	    (ashPrintObjList shortList))
	t))
