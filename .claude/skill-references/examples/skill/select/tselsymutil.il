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



; Utilities for selecting symbols

; tselectSymPinsByName - select symbol pins by refdes.pinnum string
(defun tselectSymPinsByName (symList "l")
    (let (symIns pinString (selectedPin nil))
	(foreach symIns symList
	    (setq pinString (buildString (list symIns->refdes "*") "."))
	    (when (axlAddSelectName "SYMBOL" pinString)
		(setq selectedPin t)))

	selectedPin))

; tselectSymPinsByDBID - select symbol pins using DBID
(defun tselectSymPinsByDBID (symList "l")
    (let (symIns (selectedPin nil))
	(foreach symIns symList
	    (when (axlAddSelectObject symIns->pins)
		(setq selectedPin t)))

	selectedPin))

; tselectSymChildren - select symbol children (non-pin)
(defun tselectSymChildren (symList "l")
    (let (symIns (selectedChild nil))
	(foreach symIns symList
	    (when (axlAddSelectObject symIns->children)
		(setq selectedChild t)))

	selectedChild))
