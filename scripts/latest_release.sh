#!/bin/bash

REPO=$(git rev-parse --show-toplevel)
CWD=$REPO/scripts

# Set API_TOKEN= to enable header argument.
. "$CWD/common.sh"

OWNER=vkottler
REPO=yambs-sample

run_curl "$(latest_release_url $OWNER $REPO)" > "$CWD/output.json"
cat "$CWD/output.json"
