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
