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



;; tselUpdateTest - test that the selection set contents update correctly
;;	through edit commands and sel set manipulation
(defun tselUpdateTest ()
    (let (testPass)
	(cond
    	    ((null (tselAddRemoveAdd)) nil)
	    ((null (tselSwapSymTest)) nil)
            (t (axlClearSelSet) (setq testPass t)))
 	(tselEchoResults "Selset Edit Cmd Integrity Test" testPass)))

;; tselAddRemoveAdd - test selection set integrity after removing and re-adding
;;	the same objects.
(defun tselAddRemoveAdd ()
   (let (oldCount newCount (success nil))
	(axlClearSelSet)
	(cond 
	    ((null (axlSetFindFilter ?enabled '("NOALL" "SYMBOLS")
				     ?onButtons "ALL"))
		(printf "tselAddRemoveAdd:  Failed to set find filter.\n"))
	    ((null (axlAddSelectAll))
		(printf "tselAddRemoveAdd:  Failed to select objects.\n"))
	    ((equal 0 (setq oldCount (axlGetSelSetCount)))
		(printf "tselAddRemoveAdd:  Zero select count 1.\n"))
	    ((null (axlSubSelectAll))
		(printf "tselAddRemoveAdd:  Failed to deselect objects.\n"))
	    ((null (axlAddSelectAll))
		(printf "tselAddRemoveAdd:  Failed to reselect objects.\n"))
	    ((equal 0 (setq newCount (axlGetSelSetCount)))
		(printf "tselAddRemoveAdd:  Zero select count 2.\n"))
	    ((nequal oldCount newCount)
		(printf "tselAddRemoveAdd:  OldCount(%d) != newCount(%d).\n"
			oldCount newCount))
	    (t (setq success t)))

	success)
)

(defun tselSwapAndReadd (refdes)
    (cond
	((null (ashSwapSymbols (axlGetSelSet)))
	    (printf "tselSwapSymTest:  Failed to swap symbols.\n")
	    nil)
	(t 
	    (axlAddSelectName "SYMBOL" refdes)
	    t)))


;; tselSwapSymTest - Test selection set integrity after edit command
(defun tselSwapSymTest ()
   (let (oldCount newCount (success nil))
	(axlClearSelSet)
	(cond 
	    ((null (axlSetFindFilter ?enabled '("NOALL" "SYMBOLS")
				     ?onButtons "ALL"))
		(printf "tselSwapSymTest:  Failed to set find filter.\n"))
	    ((null (axlAddSelectName "SYMBOL" '("j1b" "j1c")))
		(printf "tselSwapSymTest:  Failed to select symbols.\n"))
	    ((nequal 2 (setq oldCount (axlGetSelSetCount)))
		(printf "tselSwapSymTest: Old select count(%d) != 2.\n" oldCount))
	    ((null (tselSwapAndReadd "j1b"))
		(printf "tselSwapSymTest:  Failed to swap and readd symbols.\n"))
	    ((nequal 2 (setq newCount (axlGetSelSetCount)))
		(printf "tselSwapSymTest: New select count(%d) != 1.\n" newCount))
	    (t (setq success t)))

	success)
)
