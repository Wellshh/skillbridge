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
;; axltdesign.il - axl Design family tests
;;

(defun dsgn_t1 ()
	(axlMsgPut "**Starting dsgn_t1")

	(axlRenameDesign "trename")
	(axlMsgPut "*rename= %s" (axlCurrentDesign))

	(axlRenameDesign "trename2")
	(axlMsgPut "*save default, nocheck - trename2")
	(axlSaveDesign ?mode "nocheck")

	(axlMsgPut "*save trename3, no args")
	(axlSaveDesign ?design "trename3")

	(axlMsgPut "*save nil name, no args - enter trename4")
	(axlSaveDesign ?design nil)

	(axlMsgPut "*save default, no args - trename2")
	(axlSaveDesign)
)

(defun dsgn_t2 ()
	(axlMsgPut "**Starting dsgn_t2")

	(axlDBCreateVia "via" 2.0:7.0)
	(axlMsgPut "*open test1, no args - should reject the confirm")
	(axlOpenDesign ?design "test1")		;reject confirmation

	(axlDBCreateVia "via" 2.0:7.0)
	(axlMsgPut "*open test1, no args - don't reject the confirm")
	(axlOpenDesign ?design "test1")

	(axlDBCreateVia "via" 2.0:7.0)
	(axlMsgPut "*open test1, wf args - don't reject the confirm")
	(axlOpenDesign ?design "test1" ?mode "wf")

	(axlMsgPut "*open no name, no args - enter foo")
	(axlOpenDesign)

	(axlMsgPut "*kill design")
	(axlKillDesign)
)

(defun dsgn_test ()
	(dsgn_t1)
	(dsgn_t2)
)
