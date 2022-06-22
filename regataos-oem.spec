Name: regataos-oem
Version: 7.4
Release: 0
Url: http://www.regataos.com.br/
Summary: OEM for Regata OS
Group: System/GUI/KDE
BuildRequires: xz
BuildRequires: desktop-file-utils
BuildRequires: update-desktop-files
BuildRequires: hicolor-icon-theme
BuildRequires: -post-build-checks
%{?systemd_requires}
BuildRequires: systemd
BuildRequires: grep
Requires: xz
Requires: calamares
Requires: calamares-branding-upstream
Requires: xdotool
Requires: regataos-base >= 22
Requires: zstd
Requires: libzstd1
Requires: libzstd1-32bit
Requires: python3-zstd
Provides: bind-libs
License: MIT
Source1: %{name}-%{version}.tar.xz
Source2: psettings.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-build

%description
This package activates Calamares in case of OEM installation of the Regata OS.

%build
mkdir -p %{buildroot}/opt/regataos-base
mkdir -p %{buildroot}/usr/share/regataos/regataos-oem

%install
install -Dm0644 %{SOURCE1} %{buildroot}/opt/regataos-base/%{name}-%{version}.tar.xz
install -Dm0644 %{SOURCE2} %{buildroot}/usr/share/regataos/regataos-oem/psettings.tar.xz

%post
if test -e /opt/regataos-base/%{name}-%{version}.tar.xz ; then
	tar xf /opt/regataos-base/%{name}-%{version}.tar.xz -C /
fi

cp -f /usr/share/regataos/regataos-oem/psettings.tar.xz \
  /usr/share/regataos/regataos-oem/postinstall-settings.tar.xz

systemctl enable regataos-oem.service
systemctl stop regataos-oem.service
systemctl enable regataos-oem-check.service
systemctl stop regataos-oem-check.service

%postun
systemctl enable regataos-oem.service
systemctl stop regataos-oem.service
systemctl enable regataos-oem-check.service
systemctl stop regataos-oem-check.service

kmsg=$(grep -r "loglevel=0" /etc/default/grub)
if [[ $kmsg != *"loglevel=0"* ]]; then
  if test -e /usr/share/regataos/nvidia-iso.txt ; then
    kmsg=$(grep -r "quiet splash" /etc/default/grub)
    if [[ $kmsg == *"quiet splash"* ]]; then
      sed -i 's/quiet splash/quiet splash ivrs_ioapic[32]=00:14.0 loglevel=0 rd.systemd.show_status=auto rd.udev.log_priority=0 vt.global_cursor_default=0 rd.driver.blacklist=nouveau modprobe.blacklist=nouveau/' /etc/default/grub
    else
      sed -i 's/quiet/quiet splash ivrs_ioapic[32]=00:14.0 loglevel=0 rd.systemd.show_status=auto rd.udev.log_priority=0 vt.global_cursor_default=0 rd.driver.blacklist=nouveau modprobe.blacklist=nouveau/' /etc/default/grub
      sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=""/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash ivrs_ioapic[32]=00:14.0 loglevel=0 rd.systemd.show_status=auto rd.udev.log_priority=0 vt.global_cursor_default=0 rd.driver.blacklist=nouveau modprobe.blacklist=nouveau"/' /etc/default/grub
    fi
  else
    kmsg=$(grep -r "quiet splash" /etc/default/grub)
    if [[ $kmsg == *"quiet splash"* ]]; then
      sed -i 's/quiet splash/quiet splash ivrs_ioapic[32]=00:14.0 loglevel=0 rd.systemd.show_status=auto rd.udev.log_priority=0 vt.global_cursor_default=0/' /etc/default/grub
    else
      sed -i 's/quiet/quiet splash ivrs_ioapic[32]=00:14.0 loglevel=0 rd.systemd.show_status=auto rd.udev.log_priority=0 vt.global_cursor_default=0/' /etc/default/grub
      sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=""/GRUB_CMDLINE_LINUX_DEFAULT="quiet splash ivrs_ioapic[32]=00:14.0 loglevel=0 rd.systemd.show_status=auto rd.udev.log_priority=0 vt.global_cursor_default=0"/' /etc/default/grub
    fi
  fi
fi

sed -i 's/GRUB_TIMEOUT=10/GRUB_TIMEOUT=3/' /etc/default/grub

# Fix GRUB2 info
#Fix GRUB_DISTRIBUTOR
regataos_version=22
regataos_codename=Discovery

sed -i 's/\[ ISO \]//' /etc/default/grub
GRUB_DISTRIBUTOR=$(grep -r GRUB_DISTRIBUTOR /etc/default/grub | cut -d'"' -f 2- | cut -d'"' -f -1 | head -2 | tail -1)

if [ -z $GRUB_DISTRIBUTOR ];then
  echo 'GRUB_DISTRIBUTOR="Regata OS $regataos_version $regataos_codename"' >> /etc/default/grub
else
  sed -i "s/$GRUB_DISTRIBUTOR/Regata OS $regataos_version $regataos_codename/" /etc/default/grub
fi

#Fix GRUB_GFXMODE
GRUB_GFXMODE=$(grep -r GRUB_GFXMODE /etc/default/grub | cut -d'=' -f 2- | head -2 | tail -1)
NEW_RESOLUTION=$(sudo -H env DISPLAY=:0 xdpyinfo | grep 'dimensions:' | awk '{print $2}')
sed -i "s/$GRUB_GFXMODE/$NEW_RESOLUTION/" /etc/default/grub

#Add Regata OS theme for GRUB2
GRUB_THEME=$(grep -r GRUB_THEME /etc/default/grub | cut -d'=' -f 2-)
sed -i "s,$GRUB_THEME,/boot/grub2/themes/regataos/theme.txt," /etc/default/grub

grub2-mkconfig -o /boot/grub2/grub.cfg

# Fix Plymouth
#Select the appropriate Plymouth theme
detect_efi=$(/usr/sbin/efibootmgr)

if [[ $detect_efi == *"not supported"* ]]; then
  echo "EFI not supported"
  sudo plymouth-set-default-theme openSUSE
else
  sudo plymouth-set-default-theme bgrt
fi

if test -e /usr/share/applications/calamares.desktop ; then
	rm -f /usr/share/applications/calamares.desktop
fi

# Fix Calamares for pos-install
mkdir -p /home/visitante/.config/autostart/
cp -f /usr/share/regataos/regataos-oem/autostart/live-installer.desktop /home/visitante/.config/autostart/live-installer.desktop

sed -i 's/DISPLAYMANAGER_AUTOLOGIN=""/DISPLAYMANAGER_AUTOLOGIN="visitante"/' /etc/sysconfig/displaymanager
tar xf /usr/share/regataos/regataos-oem/postinstall-settings.tar.xz -C /

# Fix KDE Plasma for pos-install
mkdir -p "/home/visitante/.config"
mkdir -p "/home/visitante/.config/autostart"
mkdir -p "/home/visitante/.config/autostart-scripts"

cp -f "/usr/share/regataos/regataos-oem/autostart/live-installer.desktop" "/home/visitante/.config/autostart/live-installer.desktop"
cp -f "/usr/share/regataos/regataos-oem/autostart-scripts/check-calamares.sh" "/home/visitante/.config/autostart-scripts/check-calamares.sh"

rm -f "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"
cp -f "/usr/share/regataos/regataos-oem/plasma-org.kde.plasma.desktop-appletsrc" "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"
chmod 777 "/home/visitante/.config/plasma-org.kde.plasma.desktop-appletsrc"

rm -f "/home/visitante/.config/kdeglobals"
cp -f "/etc/xdg/kdeglobals" "/home/visitante/.config/kdeglobals"
chmod 777 "/home/visitante/.config/kdeglobals"

# Prepare Wine-GCS
wine_version="$(cat /opt/regataos-wine/wine-gcs-version.txt | cut -d/ -f 4 | sed 's/wine-gcs-//')"
if test ! -e "/opt/regataos-wine/wine-gcs-$wine_version"; then
  #Extract files
  tar xf /opt/regataos-wine/wine-gcs-$wine_version-x86_64.tar.xz -C /opt/regataos-wine/

  #Clear
  rm -f "/opt/regataos-wine/wine-gcs-$wine_version-x86_64.tar.xz"
fi

# Fix kernel name in grub
kernel_version=$(uname -r)
kernel_fixed_version1=$(uname -r | sed 's/\./\\./g')
kernel_fixed_version2=$(uname -r | cut -d"-" -f -1)
check_kernel_version=$(grep -r "with Linux $kernel_version" /boot/grub2/grub.cfg)
if [[ $check_kernel_version == *"with Linux $kernel_version"* ]]; then
  sed -i "s/with Linux $kernel_fixed_version1/with Linux $kernel_fixed_version2/g" "/boot/grub2/grub.cfg"
fi

# Enable KDE Plasma boot with systemd only if the system is installed.
echo "systemdBoot=false" > "/etc/xdg/startkderc"

%clean

%files
%defattr(-,root,root)
/opt/regataos-base
/opt/regataos-base/%{name}-%{version}.tar.xz
/usr/share/regataos/regataos-oem
/usr/share/regataos/regataos-oem/psettings.tar.xz

%changelog
