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
  dieOnFail 1 "Please run installation as root"
fi

if [ "$(which pip)" = "" ];
then 
  dieOnFail 1 "Please install python pip"
fi

git clone https://github.com/dalibor91/pymail.git $TARGET 

dieOnFail $? "Unable to clone repository to ${TARGET}"


cd "$TARGET/pymail"

pip install -f python-requirements.txt

dieOnFail $? "Unable to install python requirements"

ln -s "${PWD}/pymail.py" /usr/bin/pymailer
dieOnFail $? "Unable to link ${PWD}/pymail.py"


ln -s "${TARGET}/pymailclient/fsend.py" /usr/bin/pymailerclientf
dieOnFail $? "Unable to link ${TARGET}/pymailclient/fsend.py"

ln -s "${TARGET}/pymailclient/send.py" /usr/bin/pymailerclient
dieOnFail $? "Unable to link ${TARGET}/pymailclient/send.py"


echo "All done!"
exit 0
