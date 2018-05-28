#!/usr/bin/env bash

src="${BASH_SOURCE[0]}"

while [ -h "$src" ]; do
  dir="$( cd -P "$( dirname "$src" )" && pwd )"
  src="$(readlink "$src")"
  [[ $src != /* ]] && src="$dir/$src"
done
dir="$( cd -P "$( dirname "$src" )" && pwd )"

cd $dir
python3.6 main.py
exit 0
