;;; allegro_server.il - Atomic execution against the open Allegro design.
;;;
;;; Input:  __abRunTransaction(command), where command is one SKILL expression.
;;; Output: The expression value after commit; an error after failed execution.
;;; Load:   load("/absolute/path/to/allegro_server.il")
;;;
;;; A transaction mark belongs only to one call.  Opening or saving a design
;;; inside command is unsupported because Allegro cancels active transactions.

(putd '__abOKToProceed nil)
(defun __abOKToProceed ()
  (axlOKToProceed))

(putd '__abTransactionStart nil)
(defun __abTransactionStart ()
  (axlDBTransactionStart))

(putd '__abTransactionCommit nil)
(defun __abTransactionCommit (mark)
  (axlDBTransactionCommit mark))

(putd '__abTransactionRollback nil)
(defun __abTransactionRollback (mark)
  (axlDBTransactionRollback mark))

(putd '__abRunTransaction nil)
(defun __abRunTransaction (command)
  (let (mark result commandError rollbackResult)
    (unless (__abOKToProceed)
      (error "BUSY_ACTIVE_COMMAND"))

    (setq mark (__abTransactionStart))
    (unless mark
      (error "TRANSACTION_START_FAILED"))

    (setq result (errsetstring command))
    (unless result
      ;; errset.errset is global and rollback may overwrite it.
      (setq commandError errset.errset)
      (setq rollbackResult (__abTransactionRollback mark))
      (if rollbackResult
          (putprop 'errset
                   (list "error" 0 t nil
                         (list "TRANSACTION_COMMAND_FAILED" commandError))
                   'errset)
          (putprop 'errset
                   (list "error" 0 t nil
                         (list "TRANSACTION_COMMAND_FAILED"
                               commandError
                               "TRANSACTION_ROLLBACK_FAILED"))
                   'errset))
      (err))

    (unless (__abTransactionCommit mark)
      (setq rollbackResult (__abTransactionRollback mark))
      (unless rollbackResult
        (error
          "TRANSACTION_COMMIT_FAILED; TRANSACTION_ROLLBACK_FAILED"))
      (error "TRANSACTION_COMMIT_FAILED"))

    (car result)))
