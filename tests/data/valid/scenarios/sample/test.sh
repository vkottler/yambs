#!/bin/bash

set -e

"../../../../../venv$PYTHON_VERSION/bin/mbs" gen

cat_file() {
	echo "------ '$1' ------"
	cat "$1"
	echo "------------------"
}

cat_file build.ninja
cat_file ninja/all.ninja
