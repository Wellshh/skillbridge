;;; allegro_server.il - Atomic execution against the open Allegro design.
;;;
;;; Input:  __abRunTransaction(command), where command is one SKILL expression.
;;; Output: The expression value after commit; an error after failed execution.
;;; Load:   load("/absolute/path/to/allegro_server.il")
;;;
;;; A transaction mark belongs only to one call.  Opening or saving a design
;;; inside command is unsupported because Allegro cancels active transactions.

(putd '__abFreshDesign nil)
(defun __abFreshDesign ()
  (axlDBRefreshId (axlDBGetDesign)))

(putd '__abTransformSymbol nil)
(defun __abTransformSymbol (symbol delta angle)
  (axlTransformObject symbol ?move delta ?angle angle))

(putd '__abRefreshSymbol nil)
(defun __abRefreshSymbol (symbol)
  (axlDBRefreshId symbol))

(putd '__abProjectBoard nil)
(defun __abProjectBoard ()
  (letseq ((design (__abFreshDesign))
           (units (axlDBGetDesignUnits)))
    (list nil
          'path (axlGetDrawingName)
          'units (car units)
          'component_count (length design->components)
          'symbol_count (length design->symbols)
          'net_count (length design->nets))))

(putd '__abProjectComponent nil)
(defun __abProjectComponent (component @key (symbolOverride nil))
  (let ((symbol (if symbolOverride then symbolOverride else component->symbol)))
    (list nil
          'refdes component->name
          'device_type component->deviceType
          'package component->package
          'component_class component->class
          'placement (if symbol then "placed" else "unplaced")
          'x (when symbol (car symbol->xy))
          'y (when symbol (cadr symbol->xy))
          'rotation (when symbol symbol->rotation))))

(putd '__abProjectComponents nil)
(defun __abProjectComponents (refdes includeUnplaced)
  (letseq ((design (__abFreshDesign))
           (components design->components)
           result)
    (foreach component components
      (when (and (or (null refdes)
                     (equal refdes component->name))
                 (or includeUnplaced component->symbol))
        (setq result (cons (__abProjectComponent component) result))))
    (reverse result)))

(putd '__abMoveComponent nil)
(defun __abMoveComponent (refdes x y rotation)
  (letseq ((design (__abFreshDesign))
           (component nil)
           symbol currentXY delta angle transformed)
    (foreach candidate design->components
      (when (equal refdes candidate->name)
        (setq component candidate)))
    (unless component
      (error (sprintf nil "COMPONENT_NOT_FOUND: %L" refdes)))
    (setq symbol component->symbol)
    (unless symbol
      (error (sprintf nil "COMPONENT_UNPLACED: %L" refdes)))
    (setq currentXY symbol->xy)
    (setq delta (list (difference x (car currentXY))
                      (difference y (cadr currentXY))))
    (setq angle (if rotation
                    (difference rotation symbol->rotation)
                    0.0))
    (setq transformed (__abTransformSymbol symbol delta angle))
    (unless transformed
      (error (sprintf nil "COMPONENT_TRANSFORM_FAILED: %L" refdes)))
    (setq symbol (__abRefreshSymbol symbol))
    (unless symbol
      (error (sprintf nil "COMPONENT_REFRESH_FAILED: %L" refdes)))
    (__abProjectComponent component ?symbolOverride symbol)))

(putd '__abProjectNet nil)
(defun __abProjectNet (net)
  (list nil
        'name net->name
        'branch_count net->nBranches
        'unconnected_count net->unconnected
        'unplaced_pin_count net->unplaced))

(putd '__abProjectNets nil)
(defun __abProjectNets (name)
  (letseq ((design (__abFreshDesign))
           result)
    (foreach net design->nets
      (when (or (null name)
                (equal name net->name))
        (setq result (cons (__abProjectNet net) result))))
    (reverse result)))

(putd '__abProjectLayer nil)
(defun __abProjectLayer (layer)
  (list nil
        'name (strcat layer->parentName "/" layer->name)
        'class_name layer->parentName
        'subclass layer->name
        'number layer->number))

(putd '__abProjectLayers nil)
(defun __abProjectLayers (name etchOnly)
  (let (result)
    (foreach className (axlClasses)
      (when (or (null etchOnly)
                (equal className "ETCH"))
        (foreach subclass (axlSubclasses className)
          (letseq ((qualifiedName (strcat className "/" subclass))
                   (layer (axlLayerGet qualifiedName)))
            (when (or (null name)
                      (equal name qualifiedName))
              (setq result (cons (__abProjectLayer layer) result)))))))
    (reverse result)))

(putd '__abProjectPin nil)
(defun __abProjectPin (component pin)
  (letseq ((symbol component->symbol)
           (netObject pin->net)
           (netName (when (and netObject
                               (not (stringp netObject))
                               (not (equal netObject->name "")))
                      netObject->name))
           (span (when symbol pin->startEnd)))
    (list nil
          'refdes component->name
          'number pin->number
          'net netName
          'padstack pin->name
          'placement (if symbol then "placed" else "unplaced")
          'x (when symbol (car pin->xy))
          'y (when symbol (cadr pin->xy))
          'rotation (when symbol pin->rotation)
          'start_layer (when span (car span))
          'end_layer (when span (cadr span)))))

(putd '__abProjectPins nil)
(defun __abProjectPins (refdes number net)
  (letseq ((design (__abFreshDesign))
           result)
    (foreach component design->components
      (when (or (null refdes)
                (equal refdes component->name))
        (foreach pin component->pins
          (let ((projected (__abProjectPin component pin)))
            (when (and (or (null number)
                           (equal number pin->number))
                       (or (null net)
                           (equal net (get projected 'net))))
              (setq result (cons projected result)))))))
    (reverse result)))

(putd '__abProjectPadstack nil)
(defun __abProjectPadstack (padstack)
  (let ((span padstack->startEnd))
    (list nil
          'name padstack->name
          'type padstack->type
          'usage padstack->usage
          'start_layer (when span (car span))
          'end_layer (when span (cadr span)))))

(putd '__abProjectPadstacks nil)
(defun __abProjectPadstacks (name)
  (letseq ((design (__abFreshDesign))
           result)
    (foreach padstack design->padstacks
      (when (or (null name)
                (equal name padstack->name))
        (setq result (cons (__abProjectPadstack padstack) result))))
    (reverse result)))

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
