#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

if [ $# -eq 0 ] ; then
    echo "No git commit message supplied... Using [auto]."
	MSG="[auto]"
else
	MSG=$1
fi

git add .
git commit -m "$MSG" .
git pull && git push 
