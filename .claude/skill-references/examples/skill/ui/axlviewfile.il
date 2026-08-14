;; TESTS AXL VIEW FILE INTEFACE
;;	9/8/93
;;	uses /etc/passwd & /etc/hosts as view files
;;	also tests manually axlUIWExpose & axlUIWClose

alias ex axlUIWExpose
alias cl axlUIWClose

(setq view nil)

;; Base test
( defun msgnew ()
	(setq str "/etc/passwd")
	(setq view (axlUIViewFileCreate str "fxf title" t (40:40) '("E" "OUTER")))
)

;; try default positioning
( defun msgnew1 ()
	(setq str "/etc/passwd")
	(setq view (axlUIViewFileCreate str "fxf title" nil))
)

;; reuse tests --- needs msgnew or msgnew1 run already
( defun msgreuse ()
	(setq str "/etc/hosts")
	(axlUIViewFileReuse view str "reuse title" t)
)

;; view log file tests
( defun msglog ()
	(axlShell "set viewlog /etc/host")
	(setq view (axlUIViewFileCreate "" "fxf title" nil (40:20) '("E" "OUTER")))
)
