;;; Copyright (c) 2025-2026 Bai Junyan and contributors.
;;; SPDX-License-Identifier: LGPL-3.0-or-later

(putd '__abpRouteSnapshot nil)
(defun __abpRouteSnapshot (net)
  (letseq ((routes (__abProjectRoutes net nil)))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'routes routes
          'route_count (length routes))))

(putd '__abpAddConnectBlocking nil)
(defun __abpAddConnectBlocking (net command)
  (letseq ((before (__abpRouteSnapshot net)) mark terminalAttempted
           during afterRollback afterCleanup status)
    (unwindProtect
      (progn
        (setq mark (axlDBTransactionStart))
        (when mark
          (axlShell command)
          (setq during (__abpRouteSnapshot net))
          (setq terminalAttempted t)
          (axlDBTransactionRollback mark)
          (setq afterRollback (__abpRouteSnapshot net))))
      (progn
        (when (and mark (null terminalAttempted))
          (setq terminalAttempted t)
          (errset (axlDBTransactionRollback mark)))
        (setq afterCleanup (__abpRouteSnapshot net))))
    (cond
      ((null mark) (setq status "start_failed"))
      (t (setq status "completed")))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'status status
          'before before
          'during during
          'after_rollback afterRollback
          'after_cleanup afterCleanup)))

(putd '__abpAddConnectPost nil)
(defun __abpAddConnectPost (net command)
  (letseq ((before (__abpRouteSnapshot net))
           (returned (axlShellPost command))
           (immediate (__abpRouteSnapshot net)))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'before before
          'immediate immediate
          'shell_return returned)))

(setq __abpProbeMark nil)

(putd '__abpAddConnectCleanup nil)
(defun __abpAddConnectCleanup (net)
  (let (afterCleanup)
    (when __abpProbeMark
      (errset (axlDBTransactionRollback __abpProbeMark))
      (setq __abpProbeMark nil))
    (setq afterCleanup (__abpRouteSnapshot net))
    (list nil 'after_cleanup afterCleanup)))

(putd '__abpAddConnectLaunch nil)
(defun __abpAddConnectLaunch (net command)
  (letseq ((before (__abpRouteSnapshot net)) mid status)
    (setq __abpProbeMark (axlDBTransactionStart))
    (cond
      (__abpProbeMark
        (axlShell command)
        (setq mid (__abpRouteSnapshot net))
        (setq status "completed"))
      (t (setq status "start_failed")))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'status status
          'before before
          'mid mid)))

(putd '__abpAddConnectActiveDrive nil)
(defun __abpAddConnectActiveDrive (net startX startY endX endY)
  (letseq ((driveCommand (lsprintf "pick %L %L; pick %L %L; done"
                           startX startY endX endY))
           during afterRollback rolledBack)
    (unwindProtect
      (progn
        (axlShell driveCommand)
        (setq during (__abpRouteSnapshot net)))
      (when __abpProbeMark
        (setq rolledBack (errset (axlDBTransactionRollback __abpProbeMark)))
        (setq __abpProbeMark nil)))
    (setq afterRollback (__abpRouteSnapshot net))
    (list nil
          'command driveCommand
          'during during
          'after_rollback afterRollback
          'rolled_back (if rolledBack t nil))))

(putd '__abpAddConnectDriven nil)
(defun __abpAddConnectDriven (net command startX startY endX endY)
  (letseq ((drivenCommand (lsprintf "%s; pick %L %L; pick %L %L; done"
                            command startX startY endX endY))
           (before (__abpRouteSnapshot net)) mark terminalAttempted
           during afterRollback afterCleanup status)
    (unwindProtect
      (progn
        (setq mark (axlDBTransactionStart))
        (when mark
          (axlShell drivenCommand)
          (setq during (__abpRouteSnapshot net))
          (setq terminalAttempted t)
          (axlDBTransactionRollback mark)
          (setq afterRollback (__abpRouteSnapshot net))))
      (progn
        (when (and mark (null terminalAttempted))
          (setq terminalAttempted t)
          (errset (axlDBTransactionRollback mark)))
        (setq afterCleanup (__abpRouteSnapshot net))))
    (cond
      ((null mark) (setq status "start_failed"))
      (t (setq status "completed")))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'status status
          'command drivenCommand
          'before before
          'during during
          'after_rollback afterRollback
          'after_cleanup afterCleanup)))
