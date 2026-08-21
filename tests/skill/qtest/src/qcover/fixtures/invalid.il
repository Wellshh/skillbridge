;;; invalid.il - Deliberately failing input for qcover cleanup tests.
;;;
;;; This file must make (load) THROW so qcover::load exercises its failure
;;; path (restore debugMode + reset in the unwindProtect cleanup) and the
;;; enclosing assertRaises records a Pass. The 17.2 reader is lenient about
;;; EOF structural defects: an unclosed '(' only *WARNING*s and auto-closes,
;;; so load returns t and the failure path never runs (a silent false-pass).
;;; A form that parses cleanly but signals an *Error* at eval time is the
;;; documented way to make load throw -- load propagates eval errors; loadi
;;; is the lenient variant that swallows them (sklangref/inputoutput.part01.md).
;;; (plus 1 "text") is a number+string type error of the class documented in
;;; sklanguser/chap9.md (*Error* plus: can't handle ...), caught by the
;;; catch t in qtest:::raised (proven by test_report_threshold_fails_for_missing_branch).

(plus 1 "text")
