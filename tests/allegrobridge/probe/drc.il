;;; Copyright (c) 2025-2026 Bai Junyan and contributors.
;;; SPDX-License-Identifier: LGPL-3.0-or-later

(putd '__abpDrcObjectSchema nil)
(defun __abpDrcObjectSchema (object)
  (let ((properties object->??) attributes)
    (while properties
      (letseq ((name (car properties))
               (value (cadr properties)))
        (setq attributes
              (cons
                (list nil
                      'name (sprintf nil "%s" name)
                      'runtime_type (sprintf nil "%L" (type value))
                      'value (sprintf nil "%L" value))
                attributes)))
      (setq properties (cddr properties)))
    (reverse attributes)))

(putd '__abpDrcObjectReference nil)
(defun __abpDrcObjectReference (object)
  (let ((kind object->objType))
    (cond
      ((equal kind "component")
       (list nil 'reference_type "ComponentRef" 'refdes object->name))
      ((equal kind "symbol")
       (list nil 'reference_type "ComponentRef" 'refdes object->refdes))
      ((equal kind "net")
       (list nil 'reference_type "NetRef" 'name object->name))
      ((equal kind "pin")
       (letseq ((component object->component)
                (symbol object->parent)
                (refdes
                  (if component component->name
                    (when symbol symbol->refdes))))
         (list nil 'reference_type "PinRef"
               'refdes refdes 'number object->number)))
      (t (list nil 'reference_type "Kind" 'kind kind)))))

(putd '__abpDrcNetReference nil)
(defun __abpDrcNetReference (object)
  (let (net)
    (cond
      ((equal object->objType "net")
       (list nil 'reference_type "NetRef" 'name object->name))
      ((member 'net object->?)
       (setq net object->net)
       (when net
         (list nil 'reference_type "NetRef"
               'name (if (stringp net) net net->name)))))))

(putd '__abpDrcParent nil)
(defun __abpDrcParent (object)
  (when (member 'parent object->?) object->parent))

(putd '__abpDrcSnapshot nil)
(defun __abpDrcSnapshot ()
  (letseq ((design (axlDBRefreshId (axlDBGetDesign)))
           markers markerFingerprints)
    (foreach marker design->drcs
      (setq markers
            (cons
              (list marker->type marker->name marker->source marker->layer)
              markers))
      (setq markerFingerprints
            (cons
              (list marker->type marker->name marker->source marker->layer
                    marker->actual marker->expected marker->xy marker->bBox)
              markerFingerprints)))
    (list nil
          'drc_enable (axlDBControl 'drcEnable)
          'drc_state (sprintf nil "%L" design->drcState)
          'reported_count (axlDRCGetCount)
          'drcs_length (length design->drcs)
          'markers (reverse markers)
          'marker_fingerprints (reverse markerFingerprints))))

(putd '__abpDrcStatus nil)
(defun __abpDrcStatus ()
  (letseq ((design (axlDBRefreshId (axlDBGetDesign))))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'drc_enable (axlDBControl 'drcEnable)
          'drc_state (sprintf nil "%L" design->drcState)
          'reported_count (axlDRCGetCount))))

(putd '__abpDrcSchema nil)
(defun __abpDrcSchema ()
  (letseq ((design (axlDBRefreshId (axlDBGetDesign)))
           current waived)
    (foreach marker design->drcs
      (setq current
            (cons
              (list nil
                    'signature
                      (list marker->type marker->name marker->source marker->layer)
                    'attributes (__abpDrcObjectSchema marker))
              current)))
    (foreach marker design->waived
      (setq waived
            (cons
              (list nil
                    'signature
                      (list marker->type marker->name marker->source marker->layer)
                    'attributes (__abpDrcObjectSchema marker))
              waived)))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'reported_count (axlDRCGetCount)
          'design_state (sprintf nil "%L" design->drcState)
          'drc_enable (axlDBControl 'drcEnable)
          'drcs_length (length design->drcs)
          'waived_length (length design->waived)
          'current (reverse current)
          'waived (reverse waived))))

(putd '__abpDrcViolations nil)
(defun __abpDrcViolations ()
  (letseq ((design (axlDBRefreshId (axlDBGetDesign)))
           markers)
    (foreach marker design->drcs
      (let ((violations marker->violations) samples (sampleIndex 0))
        (while (and violations (lessp sampleIndex 2))
          (letseq ((object (car violations))
                   (objectReference (__abpDrcObjectReference object))
                   (cursor (__abpDrcParent object))
                   parents
                   (depth 0))
            (while (and cursor (lessp depth 4))
              (let ((cursorReference (__abpDrcObjectReference cursor)))
                (setq parents
                      (cons
                        (list nil
                              'id (sprintf nil "parent_%d" depth)
                              'obj_type cursor->objType
                              'schema (__abpDrcObjectSchema cursor)
                              'stable_ref cursorReference
                              'net_ref (__abpDrcNetReference cursor))
                        parents))
                (if (or
                      (equal cursor->objType "design")
                      (not (equal cursorReference->reference_type "Kind")))
                    (setq cursor nil)
                    (setq cursor (__abpDrcParent cursor))))
              (setq depth (plus depth 1)))
            (setq samples
                  (cons
                    (list nil
                          'id (sprintf nil "object_%d" sampleIndex)
                          'obj_type object->objType
                          'schema (__abpDrcObjectSchema object)
                          'stable_ref objectReference
                          'net_ref (__abpDrcNetReference object)
                          'parents (reverse parents))
                    samples)))
          (setq violations (cdr violations))
          (setq sampleIndex (plus sampleIndex 1)))
        (setq markers
              (cons
                (list nil
                      'signature
                        (list marker->type marker->name marker->source marker->layer)
                      'violations (reverse samples))
                markers))))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'reported_count (axlDRCGetCount)
          'markers (reverse markers))))

(putd '__abpDrcUpdate nil)
(defun __abpDrcUpdate ()
  (letseq ((originalEnable (axlDBControl 'drcEnable))
           before disabled afterUpdate afterRestore updateResult)
    (setq before (__abpDrcSnapshot))
    (unwindProtect
      (progn
        (axlDBControl 'drcEnable nil)
        (setq disabled (__abpDrcSnapshot))
        (setq updateResult (axlDRCUpdate nil))
        (setq afterUpdate (__abpDrcSnapshot)))
      (progn
        (axlDBControl 'drcEnable originalEnable)
        (setq afterRestore (__abpDrcSnapshot))))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'original_drc_enable originalEnable
          'update_result updateResult
          'before before
          'disabled disabled
          'after_update afterUpdate
          'after_restore afterRestore)))

(putd '__abpDrcStableKeys nil)
(defun __abpDrcStableKeys ()
  (letseq ((design (axlDBRefreshId (axlDBGetDesign)))
           component pin net)
    (foreach candidate design->components
      (when (and (null component) candidate->name)
        (setq component candidate))
      (when (and (null pin) candidate->name candidate->pins)
        (setq component candidate)
        (setq pin (car candidate->pins))))
    (foreach candidate design->nets
      (when (and (null net) candidate->name)
        (setq net candidate)))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'component (when component (list nil 'refdes component->name))
          'net (when net (list nil 'name net->name))
          'pin (when pin
                 (list nil 'refdes component->name 'number pin->number)))))

(putd '__abpDrcFindItem nil)
(defun __abpDrcFindItem (kind refdes name number)
  (letseq ((design (axlDBRefreshId (axlDBGetDesign)))
           target)
    (cond
      ((equal kind "component")
       (foreach candidate design->components
         (when (equal candidate->name refdes)
           (setq target candidate))))
      ((equal kind "net")
       (foreach candidate design->nets
         (when (equal candidate->name name)
           (setq target candidate))))
      ((equal kind "pin")
       (foreach component design->components
         (when (equal component->name refdes)
           (foreach candidate component->pins
             (when (equal candidate->number number)
               (setq target candidate)))))))
    target))

(putd '__abpDrcStableInput nil)
(defun __abpDrcStableInput (kind refdes name number)
  (cond
    ((equal kind "component") (list nil 'refdes refdes))
    ((equal kind "net") (list nil 'name name))
    (t (list nil 'refdes refdes 'number number))))

(putd '__abpDrcItem nil)
(defun __abpDrcItem (kind refdes name number)
  (letseq ((target (__abpDrcFindItem kind refdes name number))
           (stableInput (__abpDrcStableInput kind refdes name number)))
    (if target
        (letseq ((beforeDesign (axlDBRefreshId (axlDBGetDesign)))
                 (before
                   (list nil
                         'reported_count (axlDRCGetCount)
                         'drc_state (sprintf nil "%L" beforeDesign->drcState)))
                 (count (axlDRCItem nil target))
                 (markers (axlDRCItem t target))
                 projected
                 (afterDesign (axlDBRefreshId (axlDBGetDesign))))
          (foreach marker markers
            (setq projected
                  (cons
                    (list nil
                          'type marker->type
                          'name marker->name
                          'source marker->source
                          'layer marker->layer
                          'actual marker->actual
                          'expected marker->expected
                          'xy marker->xy
                          'bBox marker->bBox
                          'attributes (__abpDrcObjectSchema marker))
                    projected)))
          (list nil
                'status "found"
                'kind kind
                'stable_input stableInput
                'count count
                'marker_list_length (length markers)
                'markers (reverse projected)
                'before before
                'after
                  (list nil
                        'reported_count (axlDRCGetCount)
                        'drc_state (sprintf nil "%L" afterDesign->drcState))
                'ending_drc_enable (axlDBControl 'drcEnable)))
        (let (countResult countError listResult listError)
          (setq countResult (errset (axlDRCItem nil target)))
          (unless countResult
            (setq countError (sprintf nil "%L" errset.errset)))
          (setq listResult (errset (axlDRCItem t target)))
          (unless listResult
            (setq listError (sprintf nil "%L" errset.errset)))
          (list nil
                'status "missing"
                'kind kind
                'stable_input stableInput
                'count_result (when countResult (car countResult))
                'count_error countError
                'list_result (when listResult (sprintf nil "%L" (car listResult)))
                'list_error listError
                'ending_drc_enable (axlDBControl 'drcEnable))))))

(putd '__abpDrcFault nil)
(defun __abpDrcFault ()
  (letseq ((old (axlDBControl 'drcEnable)))
    (unwindProtect
      (progn
        (axlDBControl 'drcEnable nil)
        (axlDRCUpdate nil)
        (error "DRC_CLEANUP_PROBE_ERROR"))
      (axlDBControl 'drcEnable old))))

(putd '__abpDrcTransactionRollback nil)
(defun __abpDrcTransactionRollback ()
  (letseq ((originalEnable (axlDBControl 'drcEnable))
           before mark terminalAttempted operationResult operationError during
           rollbackResult afterRollback afterCleanup status)
    (setq before (__abpDrcSnapshot))
    (unwindProtect
      (progn
        (setq mark (axlDBTransactionStart))
        (when mark
          (setq operationResult (errset (axlDRCUpdate nil)))
          (unless operationResult
            (setq operationError (sprintf nil "%L" errset.errset)))
          (setq during (__abpDrcSnapshot))
          (setq terminalAttempted t)
          (setq rollbackResult (axlDBTransactionRollback mark))
          (setq afterRollback (__abpDrcSnapshot))))
      (progn
        (when (and mark (null terminalAttempted))
          (setq terminalAttempted t)
          (errset (axlDBTransactionRollback mark)))
        (axlDBControl 'drcEnable originalEnable)
        (setq afterCleanup (__abpDrcSnapshot))))
    (cond
      ((null mark) (setq status "start_failed"))
      ((null operationResult) (setq status "operation_failed"))
      ((null rollbackResult) (setq status "rollback_failed"))
      (t (setq status "completed")))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'status status
          'operation_result (when operationResult (car operationResult))
          'operation_error operationError
          'rollback_result rollbackResult
          'before before
          'during during
          'after_rollback afterRollback
          'after_cleanup afterCleanup)))

(putd '__abpDrcCouplingPhase nil)
(defun __abpDrcCouplingPhase (refdes)
  (list nil
        'component (car (__abProjectComponents refdes nil))
        'drc (__abpDrcSnapshot)))

(putd '__abpDrcDatabaseCoupling nil)
(defun __abpDrcDatabaseCoupling (sourceRefdes targetRefdes)
  (letseq ((originalEnable (axlDBControl 'drcEnable))
           baselineResult baselineError target before mark terminalAttempted
           operationResult operationError moveResult updateResult during
           rollbackResult afterRollback afterCleanup status)
    (unwindProtect
      (progn
        (setq baselineResult (errset (axlDRCUpdate nil)))
        (unless baselineResult
          (setq baselineError (sprintf nil "%L" errset.errset)))
        (when baselineResult
          (setq target (car (__abProjectComponents targetRefdes nil)))
          (setq before (__abpDrcCouplingPhase sourceRefdes))
          (setq mark (axlDBTransactionStart))
          (when mark
            (setq operationResult
                  (errset
                    (progn
                      (setq moveResult
                            (__abMoveComponent
                              sourceRefdes
                              (get target 'x)
                              (get target 'y)
                              (get target 'rotation)))
                      (setq updateResult (axlDRCUpdate nil))
                      (setq during (__abpDrcCouplingPhase sourceRefdes)))))
            (unless operationResult
              (setq operationError (sprintf nil "%L" errset.errset)))
            (setq terminalAttempted t)
            (setq rollbackResult (axlDBTransactionRollback mark))
            (setq afterRollback (__abpDrcCouplingPhase sourceRefdes)))))
      (progn
        (when (and mark (null terminalAttempted))
          (setq terminalAttempted t)
          (errset (axlDBTransactionRollback mark)))
        (axlDBControl 'drcEnable originalEnable)
        (setq afterCleanup (__abpDrcCouplingPhase sourceRefdes))))
    (cond
      ((null baselineResult) (setq status "baseline_failed"))
      ((null mark) (setq status "start_failed"))
      ((null operationResult) (setq status "operation_failed"))
      ((null rollbackResult) (setq status "rollback_failed"))
      (t (setq status "completed")))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'status status
          'source_refdes sourceRefdes
          'target_refdes targetRefdes
          'original_drc_enable originalEnable
          'baseline_result (when baselineResult (car baselineResult))
          'baseline_error baselineError
          'move_result moveResult
          'update_result updateResult
          'operation_error operationError
          'rollback_result rollbackResult
          'before before
          'during during
          'after_rollback afterRollback
          'after_cleanup afterCleanup)))

(putd '__abpDrcItemCandidates nil)
(defun __abpDrcItemCandidates (refdes)
  (letseq ((design (axlDBRefreshId (axlDBGetDesign)))
           source pinRef netRef result)
    (foreach component design->components
      (when (equal component->name refdes)
        (setq source component)))
    (when source
      (setq result (cons (list nil 'kind "component" 'refdes refdes) result))
      (foreach pin source->pins
        (when (null pinRef)
          (setq pinRef
                (list nil 'kind "pin" 'refdes refdes 'number pin->number)))
        (when (null netRef)
          (letseq ((netObject pin->net)
                   (netName (when netObject
                              (if (stringp netObject)
                                  then netObject
                                  else netObject->name))))
            (when (and netName (not (equal netName "")))
              (setq netRef (list nil 'kind "net" 'name netName))))))
      (when pinRef
        (setq result (cons pinRef result)))
      (when netRef
        (setq result (cons netRef result))))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'candidates (reverse result))))

(putd '__abpDrcItemTransactionScenario nil)
(defun __abpDrcItemTransactionScenario
       (mode kind refdes name number sourceRefdes targetRefdes)
  (letseq ((originalEnable (axlDBControl 'drcEnable))
           baselineResult baselineError source target item before mark
           terminalAttempted operationResult operationError afterMove itemResult during
           terminalResult afterTerminal cleanupResult cleanupError afterCleanup status)
    (unwindProtect
      (progn
        (setq baselineResult (errset (axlDRCUpdate nil)))
        (unless baselineResult
          (setq baselineError (sprintf nil "%L" errset.errset)))
        (when baselineResult
          (setq source (car (__abProjectComponents sourceRefdes nil)))
          (setq target (car (__abProjectComponents targetRefdes nil)))
          (setq before (__abpDrcCouplingPhase sourceRefdes))
          (axlDBControl 'drcEnable nil)
          (setq mark (axlDBTransactionStart))
          (when mark
            (setq operationResult
                  (errset
                    (progn
                      (__abMoveComponent
                        sourceRefdes
                        (get target 'x)
                        (get target 'y)
                        (get target 'rotation))
                      (setq afterMove (__abpDrcCouplingPhase sourceRefdes))
                      (axlDBControl 'drcEnable t)
                      (setq item (__abpDrcFindItem kind refdes name number))
                      (unless item
                        (error "DRC_ITEM_NOT_FOUND"))
                      (setq itemResult (axlDRCItem t item))
                      (setq during (__abpDrcCouplingPhase sourceRefdes))
                      (when (equal mode "error")
                        (error "DRC_ITEM_PROBE_ERROR")))))
            (unless operationResult
              (setq operationError (sprintf nil "%L" errset.errset)))
            (setq terminalAttempted t)
            (setq terminalResult
                  (if (and (equal mode "commit") operationResult)
                      then (axlDBTransactionCommit mark)
                      else (axlDBTransactionRollback mark)))
            (setq afterTerminal (__abpDrcCouplingPhase sourceRefdes)))))
      (progn
        (when (and mark
                   (or (null terminalAttempted) (null terminalResult)))
          (setq terminalAttempted t)
          (errset (axlDBTransactionRollback mark)))
        (when (and (equal mode "commit") terminalResult)
          (setq cleanupResult
                (errset
                  (progn
                    (__abMoveComponent
                      sourceRefdes
                      (get source 'x)
                      (get source 'y)
                      (get source 'rotation))
                    (axlDRCUpdate nil))))
          (unless cleanupResult
            (setq cleanupError (sprintf nil "%L" errset.errset))))
        (axlDBControl 'drcEnable originalEnable)
        (setq afterCleanup (__abpDrcCouplingPhase sourceRefdes))))
    (cond
      ((null baselineResult) (setq status "baseline_failed"))
      ((null mark) (setq status "start_failed"))
      ((null item) (setq status "item_missing"))
      ((and (equal mode "error") operationResult)
       (setq status "expected_error_missing"))
      ((and (not (equal mode "error")) (null operationResult))
       (setq status "operation_failed"))
      ((null terminalResult) (setq status "terminal_failed"))
      ((and (equal mode "commit") (null cleanupResult))
       (setq status "cleanup_failed"))
      (t (setq status "completed")))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'mode mode
          'status status
          'original_drc_enable originalEnable
          'baseline_result (when baselineResult (car baselineResult))
          'baseline_error baselineError
          'item_marker_count (length itemResult)
          'operation_error operationError
          'terminal_result terminalResult
          'cleanup_error cleanupError
          'before before
          'after_move afterMove
          'during during
          'after_terminal afterTerminal
          'after_cleanup afterCleanup)))
