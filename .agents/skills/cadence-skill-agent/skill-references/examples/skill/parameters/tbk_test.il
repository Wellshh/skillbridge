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




;; test_textblock  - test attribute access of Textblock Attrs
;find all Textblock Attrs
  ;    print out all attributes of Textblock Parameter type

  (defun test_textblock (p)
    (pprint (setq dsn (axlGetParam "paramTextBlock:1")) p)
    (fprintf p "\n")
 ;   (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
      (fprintf p "\n")
;   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
  (fprintf p "Setting photoWidth to: ")
     (pprint (putprop dsn -2.0 'photoWidth) p)
    (fprintf p "\n")
    (fprintf p "Found photoWidth to be: ")	
    (pprint dsn->photoWidth p)
    (fprintf p "\n")
  (fprintf p "Setting Width to: ")
     (pprint (putprop dsn -2.0 'width) p)
    (fprintf p "\n")
    (fprintf p "Found Width to be: ")	
    (pprint dsn->width p)
    (fprintf p "\n")
    (fprintf p "Setting Name to: ")
     (pprint (putprop dsn "-1" 'name) p)
    (fprintf p "\n")
    (fprintf p "Expecting no change, found name to be: ")	
    (pprint dsn->name p)
    (fprintf p "\n")
    (fprintf p "Setting objtype to: ")
   (pprint (dsn->objtype="TextBlock") p)
    (fprintf p "\n")
     (fprintf p "Expecting nil, found objtype to be: ")	
   (pprint dsn->objtype p)	
    (fprintf p "\n")
     (pprint dsn->?? p)
  (fprintf p "\n") 
   (fprintf p "\n")
    (fprintf p "Setting textblock object,expecting nil, found to be: ")	
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Retrieving textblock object, found to be: ")	
    (pprint (setq dsn (axlGetParam "paramTextBlock:1")) p)
   (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
  ) ; defun test_textblock

 (defun test_textblock1 (p)
    (pprint (setq dsn (axlGetParam "paramTextBlock:1")) p)
    (fprintf p "\n")
 ;   (pprint dsn->? p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
      (fprintf p "\n")
  (fprintf p "Setting photoWidth to: ")
     (pprint (putprop dsn 5.0 'photoWidth) p)
    (fprintf p "\n")
    (fprintf p "Found photoWidth to be: ")	
    (pprint dsn->photoWidth p)
    (fprintf p "\n")
  (fprintf p "Setting Width to: ")
     (pprint (putprop dsn 3.0 'width) p)
    (fprintf p "\n")
    (fprintf p "Found Width to be: ")	
    (pprint dsn->width p)
   (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting textblock object, found to be: ")	
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Retrieving textblock object, found to be: ")	
    (pprint (setq dsn (axlGetParam "paramTextBlock:1")) p)
   (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
  ) ; defun test_textblock1

 (defun test_textblock2 (p)
    (pprint (setq dsn (axlGetParam "paramTextBlock:3")) p)
    (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
      (fprintf p "\n")
  (fprintf p "Setting Width to: ")
     (pprint (putprop dsn 3000000.0 'width) p)
    (fprintf p "\n")
    (fprintf p "Found Width to be: ")	
    (pprint dsn->width p)
   (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
    (fprintf p "\n")
    (fprintf p "Setting textblock object,expecting nil, found to be: ")	
   (pprint (axlSetParam dsn) p)	
    (fprintf p "\n")
    (fprintf p "Retrieving textblock object, found to be: ")	
    (pprint (setq dsn (axlGetParam "paramTextBlock:3")) p)
   (fprintf p "\n")
    (pprint dsn->?? p)
    (fprintf p "\n")
  ) ; defun test_textblock2

  
(defun axltxtblock_test ()
 (setq p outfile("bronze.txt", "a"))
 (setq _itemsperline 1)
 (fprintf p "\n\n*test_textblock:****************************************\n\n")
 (test_textblock p)
 (fprintf p "\n\n*test_textblock1:\n\n")
 (test_textblock1 p)
 (fprintf p "\n\n*test_textblock2:\n\n")
 (test_textblock2 p)
 (close p)
 ) ; defun axltxtblock_test

