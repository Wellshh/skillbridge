;;; Copyright (c) 2025-2026 Bai Junyan and contributors.
;;; SPDX-License-Identifier: LGPL-3.0-or-later

(putd '__abpRouteSnapshot nil)
(defun __abpRouteSnapshot (net)
  (letseq ((routes (__abProjectRoutes net nil)))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'routes routes
          'route_count (length routes))))

(putd '__abpAddConnectRun nil)
(defun __abpAddConnectRun (net command)
  (letseq ((before (__abpRouteSnapshot net)) during)
    (axlShell command)
    (setq during (__abpRouteSnapshot net))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'before before
          'during during)))

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

(putd '__abpAddConnectActiveDrive nil)
(defun __abpAddConnectActiveDrive (net startX startY endX endY)
  (letseq ((driveCommand (lsprintf "pick %L %L; pick %L %L; done"
                           startX startY endX endY))
           during)
    (axlShell driveCommand)
    (setq during (__abpRouteSnapshot net))
    (list nil
          'command driveCommand
          'during during)))

(putd '__abpAddConnectDriven nil)
(defun __abpAddConnectDriven (net command startX startY endX endY)
  (letseq ((drivenCommand (lsprintf "%s; pick %L %L; pick %L %L; done"
                            command startX startY endX endY))
           (before (__abpRouteSnapshot net)) during)
    (axlShell drivenCommand)
    (setq during (__abpRouteSnapshot net))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'command drivenCommand
          'before before
          'during during)))

;;; These probes deliberately keep the command and every DBID inside Allegro.
;;; Python receives only projections, so axlShell's DBID invalidation is observable
;;; without leaking an address or reusing an object in a later RPC.
(putd '__abpAddConnectTransaction nil)
(defun __abpAddConnectTransaction (net command startX startY endX endY action)
  (letseq ((mark (axlDBTransactionStart))
           before during after)
    (unless mark
      (error "ADD_CONNECT_TRANSACTION_START_FAILED"))
    (unwindProtect
      (progn
        (setq before (__abpRouteSnapshot net))
        (axlShell (lsprintf "%s; pick %L %L; pick %L %L; done"
                           command startX startY endX endY))
        (setq during (__abpRouteSnapshot net))
        (cond
          ((equal action "commit")
           (unless (axlDBTransactionCommit mark)
             (error "ADD_CONNECT_TRANSACTION_COMMIT_FAILED"))
           (setq mark nil)
           (setq after (__abpRouteSnapshot net)))
          ((equal action "rollback")
           (unless (axlDBTransactionRollback mark)
             (error "ADD_CONNECT_TRANSACTION_ROLLBACK_FAILED"))
           (setq mark nil)
           (setq after (__abpRouteSnapshot net)))
          (t
           (setq after nil)))
        (list nil
              'allegro_version (axlVersion 'fullVersion)
              'action action
              'before before
              'during during
              'after after))
      (when mark
        (axlDBTransactionRollback mark)))))

(putd '__abpAddConnectDbidProbe nil)
(defun __abpAddConnectDbidProbe (net command startX startY endX endY)
  (letseq ((oldDesign (axlDBGetDesign))
           (oldNet (car oldDesign->nets))
           (oldDesignRefresh nil)
           (oldNetRefresh nil)
           (fresh nil))
    (axlShell (lsprintf "%s; pick %L %L; pick %L %L; done"
                       command startX startY endX endY))
    (setq oldDesignRefresh (not (null (axlDBRefreshId oldDesign))))
    (setq oldNetRefresh (and oldNet
                             (not (null (axlDBRefreshId oldNet)))))
    (setq fresh (axlDBGetDesign))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'old_design_refreshable oldDesignRefresh
          'old_net_refreshable oldNetRefresh
          'old_object_kind (type oldNet)
          'fresh_design_kind (type fresh)
          'fresh_routes (__abpRouteSnapshot net))))

(putd '__abpAddConnectPostDriven nil)
(defun __abpAddConnectPostDriven (net command startX startY endX endY)
  (letseq ((postCommand (lsprintf "%s; _pick %L %L; _pick %L %L; _done"
                                 command startX startY endX endY))
           before immediate)
    (setq before (__abpRouteSnapshot net))
    (axlShellPost postCommand)
    (setq immediate (__abpRouteSnapshot net))
    (list nil
          'allegro_version (axlVersion 'fullVersion)
          'command postCommand
          'before before
          'immediate immediate)))
