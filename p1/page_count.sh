#!/bin/sh
tail -c 1024 "$1" | tr '<>' '\n' | grep ^page\ w= | tail -n 1 | tr ' ' '\n' | grep ^id=
