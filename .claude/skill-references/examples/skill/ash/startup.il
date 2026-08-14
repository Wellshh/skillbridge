; $Header: startup.il,v 1.1 02/03/07 10:09:27 ccc $

(foreach file (rexMatchList "\\.il$" (getDirFiles "."))
  (unless (or (equal file "startup.il") (equal file "sstartup.il"))
    (load file)))
