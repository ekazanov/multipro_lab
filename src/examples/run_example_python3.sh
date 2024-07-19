#! /bin/bash
# Author Evgeny Kazanov

if [[ $# -ne 1 ]]
then
    echo
    echo "Usage: ./run_example_python3.sh <example file name>"
    echo
    exit 1
fi

CUR_DIR=`pwd`
cd ..
PYTHON_BASE=`pwd`
cd $CUR_DIR

PYTHONPATH=$PYTHONPATH:$PYTHON_BASE

python3 $1
