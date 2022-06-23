#!/bin/bash

cd /

while :
do

if [[ $(rpm -q regataos-oem) == *"x86"* ]]; then
	echo "In Live Mode..."
	break
else
	if test -e "/home/visitante"; then
		if [[ $(grep -r "visitante" "/etc/sysconfig/displaymanager" | cut -d'=' -f 2- | sed 's/"//g') != *"visitante"* ]]; then
			sed -i 's/DISPLAYMANAGER_AUTOLOGIN=""/DISPLAYMANAGER_AUTOLOGIN="visitante"/' /etc/sysconfig/displaymanager
		fi

		if [[ $(grep -r "users" "/usr/share/calamares/settings.conf" | awk '{print $2}') != *"users"* ]]; then
			tar xf /usr/share/regataos/regataos-oem/postinstall-settings.tar.xz -C /
		fi

	else
		if test ! -e "/usr/bin/calamares"; then
			sed -i 's/DISPLAYMANAGER_AUTOLOGIN="visitante"/DISPLAYMANAGER_AUTOLOGIN=""/' /etc/sysconfig/displaymanager
			rm -f /usr/share/regataos/regataos-oem-check.sh
			break
		fi
	fi
fi

   sleep 2
done
