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

(putd '__abSavepointResult nil)
(defun __abSavepointResult (index status field value)
  (list nil 'index index 'status status field value))

(putd '__abAbortSavepointBatch nil)
(defun __abAbortSavepointBatch (outerMark reason)
  (if (__abTransactionRollback outerMark)
      (putprop 'errset
               (list "error" 0 t nil reason)
               'errset)
      (putprop 'errset
               (list "error" 0 t nil
                     (append reason (list "SAVEPOINT_BATCH_ROLLBACK_FAILED")))
               'errset))
  (err))

(putd '__abRunSavepointBatch nil)
(defun __abRunSavepointBatch (commands)
  (let (outerMark innerMark result commandError rollbackResult results index)
    (unless (__abOKToProceed)
      (error "BUSY_ACTIVE_COMMAND"))

    (setq outerMark (__abTransactionStart))
    (unless outerMark
      (error "SAVEPOINT_BATCH_START_FAILED"))

    (setq index 0)
    (foreach command commands
      (setq innerMark (__abTransactionStart))
      (unless innerMark
        (__abAbortSavepointBatch outerMark (list "SAVEPOINT_START_FAILED")))

      (setq result (errsetstring command))
      (if result
          (if (__abTransactionCommit innerMark)
              (setq results
                    (cons (__abSavepointResult
                            index "success" 'value (car result))
                          results))
              (progn
                (setq rollbackResult (__abTransactionRollback innerMark))
                (unless rollbackResult
                  (__abAbortSavepointBatch
                    outerMark
                    (list "SAVEPOINT_COMMIT_FAILED" "SAVEPOINT_ROLLBACK_FAILED")))
                (setq results
                      (cons (__abSavepointResult
                              index "failure" 'error
                              "SAVEPOINT_COMMIT_FAILED")
                            results))))
          (progn
            (setq commandError errset.errset)
            (setq rollbackResult (__abTransactionRollback innerMark))
            (unless rollbackResult
              (__abAbortSavepointBatch
                outerMark
                (list "SAVEPOINT_COMMAND_FAILED"
                      commandError
                      "SAVEPOINT_ROLLBACK_FAILED")))
            (setq results
                  (cons (__abSavepointResult
                          index "failure" 'error
                          (sprintf nil "SAVEPOINT_COMMAND_FAILED: %L"
                                   commandError))
                        results))))
      (setq index (add1 index)))

    (unless (__abTransactionCommit outerMark)
      (setq rollbackResult (__abTransactionRollback outerMark))
      (if rollbackResult
          (error "SAVEPOINT_BATCH_COMMIT_FAILED")
          (error
            "SAVEPOINT_BATCH_COMMIT_FAILED; SAVEPOINT_BATCH_ROLLBACK_FAILED")))

    (reverse results)))

(putd '__abRunDryTransaction nil)
(defun __abRunDryTransaction (command)
  (let (mark result commandError rollbackResult)
    (unless (__abOKToProceed)
      (error "BUSY_ACTIVE_COMMAND"))

    (setq mark (__abTransactionStart))
    (unless mark
      (error "DRY_RUN_START_FAILED"))

    (setq result (errsetstring command))
    (unless result
      (setq commandError errset.errset)
      (setq rollbackResult (__abTransactionRollback mark))
      (if rollbackResult
          (putprop 'errset
                   (list "error" 0 t nil
                         (list "DRY_RUN_COMMAND_FAILED" commandError))
                   'errset)
          (putprop 'errset
                   (list "error" 0 t nil
                         (list "DRY_RUN_COMMAND_FAILED"
                               commandError
                               "DRY_RUN_ROLLBACK_FAILED"))
                   'errset))
      (err))

    (unless (__abTransactionRollback mark)
      (error "DRY_RUN_ROLLBACK_FAILED"))

    (car result)))
