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
