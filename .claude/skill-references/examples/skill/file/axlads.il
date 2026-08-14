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



;; TESTS AXL DM INTERFACE
;;	fxf 9/8/93
;;	needs no other files

alias fclose axlDMClose
alias flog axlDMOpenLog


;; test axlDMOpenLog and axlDMClose -- good values
(defun ads1 ()
	(setq logfile (axlDMOpenLog "foobar"))
	( fprintf logfile "a test write\n" )
	( axlDMClose logfile )
)


;; test axlDMOpenFile and axlDMClose -- good values
(defun ads2 ()
	(setq outfile (axlDMOpenFile "ALLEGRO_TEXT" "foobar" "w"))
	( fprintf outfile "a test write\n" )
	( axlDMClose outfile )
)

;; test axlDMGetFile -- see if get an overwrite confirmer (run ads2 or ads1 before)
(defun ads3 ()
	(setq outfile (axlDMGetFile "ALLEGRO_TEXT" "foobar" "w"))
)
