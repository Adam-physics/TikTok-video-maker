#!/bin/sh
# Re-download prototype images listed in images.tsv into prototype/img
cd "$(dirname "$0")/../prototype" && mkdir -p img && while IFS="$(printf "\t")" read u f; do curl -s -H "Accept: image/jpeg" "$u" -o "img/$f"; done < ../tools/images.tsv
