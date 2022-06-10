#!/bin/bash

cd /

while :
do

# Prepare KDE Plasma for post-installation setup.
function prepare_plasma() {
	mkdir -p "/home/visitante/.config"
	mkdir -p "/home/visitante/.config/autostart"
	mkdir -p "/home/visitante/.config/autostart-scripts"

	cp -f "/usr/share/regataos/regataos-oem/autostart/live-installer.desktop" "/home/visitante/.config/autostart/live-installer.desktop"
	cp -f "/usr/share/regataos/regataos-oem/autostart-scripts/check-calamares.sh" "/home/visitante/.config/autostart-scripts/check-calamares.sh"

	rm -f "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"
	cp -f "/usr/share/regataos/regataos-oem/plasma-org.kde.plasma.desktop-appletsrc" "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"

	rm -f "/home/visitante/.config/kdeglobals"
	cp -f "/etc/xdg/kdeglobals" "/home/visitante/.config/kdeglobals"
}

if [[ $(rpm -q regataos-oem) == *"x86"* ]]; then
    echo "In Live Mode..."
else
    if test -e "/home/visitante"; then
		if [[ $(rpm -q calamares) == *"x86"* ]]; then
			echo "In post-installation..."

			if test ! -e "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"; then
				prepare_plasma

			elif [[ $(grep -r "org.kde.panel" "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc" | cut -d'=' -f 2-) == *"org.kde.panel"* ]]; then
				prepare_plasma

			else
				if [ $(wc -l "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc" | awk '{print $1}') -ne 26 ]; then
					prepare_plasma
				fi
			fi

			if [[ $(grep -r "visitante" "/etc/sysconfig/displaymanager" | cut -d'=' -f 2- | sed 's/"//g') != *"visitante"* ]]; then
				sed -i 's/DISPLAYMANAGER_AUTOLOGIN=""/DISPLAYMANAGER_AUTOLOGIN="visitante"/' /etc/sysconfig/displaymanager
			fi

			if [[ $(grep -r "users" "/usr/share/calamares/settings.conf" | awk '{print $2}') != *"users"* ]]; then
				tar xf /usr/share/regataos/regataos-oem/postinstall-settings.tar.xz -C /
			fi

		else
			if test ! -e "/usr/bin/calamares"; then
				sed -i 's/DISPLAYMANAGER_AUTOLOGIN="visitante"/DISPLAYMANAGER_AUTOLOGIN=""/' /etc/sysconfig/displaymanager
				sed -i 's/visitante/#visitante/' /etc/sudoers

				echo "Calamares installer is not installed. The Regata OS appears to be installed, goodbye!"
				rm -f "/usr/share/regataos/regataos-oem.sh"
				break
			fi
		fi

    else
		if test ! -e "/usr/bin/calamares"; then
			sed -i 's/DISPLAYMANAGER_AUTOLOGIN="visitante"/DISPLAYMANAGER_AUTOLOGIN=""/' /etc/sysconfig/displaymanager
			sed -i 's/visitante/#visitante/' /etc/sudoers

			echo "Directory /home/visitante not found. The Regata OS appears to be installed, goodbye!"
			rm -f "/usr/share/regataos/regataos-oem.sh"
			break
		fi
    fi
fi

   sleep 2
done
