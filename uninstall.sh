#!/bin/bash

TARGET=/var/lib/daliborpymail
WHOAMI=$(whoami)

function dieOnFail(){
  if [ ! $1 -eq 0 ];
  then
    echo $2
    exit 1
  fi
}

if [ ! "$WHOAMI" = 'root' ];
then
  dieOnFail 1 "Please run this as root"
fi

rm -rf $TARGET 
dieOnFail $? "Unable to delete ${TARGET}"

rm /usr/bin/pymailer
dieOnFail $? "Unable to remove link /usr/bin/pymailerclient"

rm /usr/bin/pymailerclientf
dieOnFail $? "Unable to remove link /usr/bin/pymailerclient"

rm /usr/bin/pymailerclient
dieOnFail $? "Unable to remove link /usr/bin/pymailerclient"

echo "All done!"
exit 0
