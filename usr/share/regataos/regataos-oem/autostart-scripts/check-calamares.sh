#!/bin/bash

cd /

while :
do

# Check if the system has already been installed.
if [[ $(rpm -q calamares) != *"x86"* ]]; then
	rm -f "/usr/share/regataos/check-calamares.sh"
	rm -f "/home/visitante/.config/autostart-scripts/check-calamares.sh"
	break
fi

# Prepare KDE Plasma for post-installation setup.
if [[ $(rpm -q regataos-oem) != *"x86"* ]]; then
	mkdir -p "/home/visitante/.config"
	mkdir -p "/home/visitante/.config/autostart"
	mkdir -p "/home/visitante/.config/autostart-scripts"

	cp -f "/usr/share/regataos/regataos-oem/autostart/live-installer.desktop" "/home/visitante/.config/autostart/live-installer.desktop"
	cp -f "/usr/share/regataos/regataos-oem/autostart-scripts/check-calamares.sh" "/home/visitante/.config/autostart-scripts/check-calamares.sh"

	rm -f "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"
	cp -f "/usr/share/regataos/regataos-oem/plasma-org.kde.plasma.desktop-appletsrc" "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"

	rm -f "/home/visitante/.config/kdeglobals"
	cp -f "/etc/xdg/kdeglobals" "/home/visitante/.config/kdeglobals"

	# Check desktop
	user=$(users | awk '{print $1}')
	test -f "${XDG_CONFIG_HOME:-/home/$user/.config}/user-dirs.dirs" && source "${XDG_CONFIG_HOME:-/home/$user/.config}/user-dirs.dirs"
	desktop_dir="${XDG_DESKTOP_DIR:-/home/$user/Desktop}"
	desktop_folder="$(echo $desktop_dir | cut -d/ -f 3-)"
	desktop_dir="/home/$desktop_folder"
	echo "Desktop: $desktop_dir"

	if test -e "$desktop_dir/trash.desktop"; then
		cd "$desktop_dir/"
		rm -rf *.desktop
		xdotool key F5

	elif test -e "$desktop_dir/Home.desktop"; then
		cd "$desktop_dir/"
		rm -rf *.desktop
		xdotool key F5

	else
		if test -e "$desktop_dir/live-installer.desktop"; then
			cd "$desktop_dir/"
			rm -rf *.desktop
			xdotool key F5
		fi
	fi

	if [[ $user == *"visitante"* ]]; then
		ps -C calamares > /dev/null
		if [ $? = 0 ]
		then
			break
		else
			/usr/bin/live-installer start
		fi
	else
		break
	fi
fi

   sleep 1
done
