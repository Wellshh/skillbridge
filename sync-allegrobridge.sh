#!/usr/bin/env bash
# Copyright (c) 2025-2026 Bai Junyan and contributors.
# SPDX-License-Identifier: LGPL-3.0-or-later
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="$(dirname "$SRC")/allegrobridge-extract"
DIRS=(allegrobridge skillbridge tests scripts docs benchmark)
FILES=(mkdocs.yml conftest.py)

if [ ! -d "$DST/.git" ]; then
    echo "sync: $DST not found, skipping"
    exit 0
fi

if [ -n "$(git -C "$DST" status --porcelain)" ]; then
    echo "sync: $DST has uncommitted changes, refusing to sync" >&2
    exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git -C "$SRC" archive HEAD "${DIRS[@]}" "${FILES[@]}" | tar -x -C "$TMP"
rm -f "$TMP/allegrobridge/PLAN.md" "$TMP/skillbridge/server/SECRET.md"
find "$TMP" -name .DS_Store -delete

for dir in "${DIRS[@]}"; do
    rsync -a --delete "$TMP/$dir/" "$DST/$dir/"
done
# sync back
for f in "${FILES[@]}"; do
    cp "$TMP/$f" "$DST/$f"
done

git -C "$DST" add -A -- "${DIRS[@]}" "${FILES[@]}"
if git -C "$DST" diff --cached --quiet -- "${DIRS[@]}" "${FILES[@]}"; then
    echo "sync: allegrobridge-extract already up to date"
    exit 0
fi

hash="$(git -C "$SRC" log -1 --format='%h')"
subject="$(git -C "$SRC" log -1 --format='%s')"
changes="$(git -C "$DST" diff --cached --name-status -- "${DIRS[@]}" "${FILES[@]}")"

git -C "$DST" commit -q -m "chore(sync): from skillbridge@$hash: $subject"
echo "sync: mirrored skillbridge@$hash -> allegrobridge-extract"
echo "sync: synced files in this commit:"
echo "$changes" | awk '{if (NF >= 3) printf "  [%s] %s -> %s\n", $1, $2, $3; else printf "  [%s] %s\n", $1, $2}'
