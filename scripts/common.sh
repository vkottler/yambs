#!/bin/bash

CURL_ARGS=(curl -L)

add_header() {
	CURL_ARGS+=(-H "$1: $2")
}

add_header Accept application/vnd.github+json

API_VERSION=2022-11-28
add_header X-GitHub-Api-Version $API_VERSION

if [ -n "$API_TOKEN" ]; then
	add_header Authorization "Bearer $API_TOKEN"
fi

run_curl() {
	echo "${CURL_ARGS[@]}" "$@" >&2
	"${CURL_ARGS[@]}" "$@"
}

repo_api_url() {
	echo "https://api.github.com/repos/$OWNER/$REPO"
}

latest_release_url() {
	echo "$(repo_api_url "$1" "$2")/releases/latest"
}
