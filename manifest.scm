;; bramble-os --- an opinionated framework
;;
;; SPDX-FileCopyrightText: 2024 antlers <antlers@illucid.net>
;;
;; SPDX-License-Identifier: GPL-3.0-or-later

(use-modules (gnu packages license)
             (guix profiles))

(packages->manifest
  (list reuse))
