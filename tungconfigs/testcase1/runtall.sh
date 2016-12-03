#!/bin/bash
#note: first run "chmod a+x file.sh"
# ./tungconfigs/testcase1/runt1.sh & ./tungconfigs/testcase1/runt12.sh & ./tungconfigs/testcase1/runt13.sh
# set +x
./tungconfigs/testcase1/runt1.sh > /dev/null 2>&1 &
./tungconfigs/testcase1/runt12.sh > /dev/null 2>&1 &
./tungconfigs/testcase1/runt13.sh > /dev/null 2>&1 &