#!/bin/bash

cd /

while :
do

ps -C calamares > /dev/null
if [ $? = 0 ]
then
    echo "The Calamares installer is running..."
else
    systemctl poweroff
fi

   sleep 2
done
