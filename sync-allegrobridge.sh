#!/usr/bin/env bash
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DST="$(dirname "$SRC")/allegrobridge-extract"
DIRS=(allegrobridge skillbridge tests scripts)

if [ ! -d "$DST/.git" ]; then
    echo "sync: $DST not found, skipping"
    exit 0
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

git -C "$SRC" archive HEAD "${DIRS[@]}" | tar -x -C "$TMP"
rm -f "$TMP/allegrobridge/PLAN.md" "$TMP/skillbridge/server/SECRET.md" "$TMP/tests/.DS_Store"

for dir in "${DIRS[@]}"; do
    rsync -a --delete "$TMP/$dir/" "$DST/$dir/"
done

git -C "$DST" add -A
if git -C "$DST" diff --cached --quiet; then
    echo "sync: allegrobridge-extract already up to date"
    exit 0
fi

hash="$(git -C "$SRC" log -1 --format='%h')"
subject="$(git -C "$SRC" log -1 --format='%s')"
git -C "$DST" commit -q -m "sync from skillbridge@$hash: $subject"
echo "sync: mirrored skillbridge@$hash -> allegrobridge-extract"
