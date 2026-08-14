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
;; axltextract.il - axl Extract family tests
;;

(defun dax_t1 ()
	(axlMsgPut "**Starting dax_t1")

	;; single output file, list of options including crosshatch
	(if (null (axlExtractToFile "geometry_baseview" "dax1.x"
	    '("crosshatch" "quiet" "debug"))) (axlMsgPut "extract failed"))
	(shell "extract -q -w test1 geometry_baseview dax1.xx")
	(shell "diff dax1.x dax1.xx")

	;; list of output names, list of options
	(if (null (axlExtractToFile "nbn_rep_view" '("dax2a.x" "dax2b.x")
	    '("quiet" "debug"))) (axlMsgPut "extract failed"))
	(shell "extract -q -w test1 nbn_rep_view dax2a.xx dax2b.xx")
	(shell "diff dax2a.x dax2a.xx")
	(shell "diff dax2b.x dax2b.xx")

	;; single output name, single option - not quiet
	(if (null (axlExtractToFile "net_name_view" "dax3.x" "short"))
	     (axlMsgPut "extract failed"))
	(shell "extract -s test1 net_name_view dax3.xx")

	;; nil output name, no option
	(if (null (axlExtractToFile "net_name_view" nil))
	     (axlMsgPut "extract failed"))

	t
)

(defun dax_t2 ()
	(axlMsgPut "**Starting dax_t2")

	(foreach n (axlExtractMap "net_name_view")
	    (printf "%s\n" (get n 'name)))
)

(defun dax_t3 ()
	(axlMsgPut "**Starting dax_t3")
    (let ((byReference (list nil 'nets nil)))
	(axlExtractMap "net_name_view"
	    (lambda (dbid netRef)
		(putprop netRef
		    (cons (get dbid 'name) (get netRef 'nets))
		    'nets)
		t)
	    byReference)
	(get byReference 'nets)))

(defun dax_t4 ()
	(axlMsgPut "**Starting dax_t4")
    (let ((byReference (list nil 'nets nil)) ret)
	(setq ret (axlExtractMap "net_name_view"
	    (lambda (dbid netRef)
		(putprop netRef
		    (cons (get dbid 'name) (get netRef 'nets))
		    'nets)
		(nequal (get dbid 'name) "SIG2"))
	    byReference))
	(printf "%L\n" (get byReference 'nets))
	ret))



(defun dax_test ()
	(dax_t1)
	(dax_t2)
	(dax_t3)
	(dax_t4)
)
