#!/bin/bash

set -e

rm -rf build.ninja ninja

"../../../../../venv$PYTHON_VERSION/bin/mbs" gen

cat_file() {
	echo "------ '$1' ------"
	cat "$1"
	echo "------------------"
}

tree ninja
