#!/bin/sh

userresources=$HOME/.Xresources
usermodmap=$HOME/.Xmodmap
sysresources=/etc/X11/xinit/.Xresources
sysmodmap=/etc/X11/xinit/.Xmodmap

# merge in defaults and keymaps

if [ -f $sysresources ]; then
    xrdb -merge $sysresources
fi

if [ -f $sysmodmap ]; then
    xmodmap $sysmodmap
fi

if [ -f "$userresources" ]; then
    xrdb -merge "$userresources"
fi

if [ -f "$usermodmap" ]; then
    xmodmap "$usermodmap"
fi

# start some nice programs

if [ -d /etc/X11/xinit/xinitrc.d ] ; then
 for f in /etc/X11/xinit/xinitrc.d/?*.sh ; do
  [ -x "$f" ] && . "$f"
 done
 unset f
fi

# Multiple Screen
dp=`xrandr | grep ' connected' | grep -v 'eDP-1' | grep 'DP-1' | awk '{print $1}'`

if [ "$dp" = "DP-1" ]; then
    xrandr --output eDP-1 --mode 1366x768 --pos 1366x0 --rotate normal --output HDMI-1 --off --output DP-1 --primary --mode 1366x768 --pos 0x0 --rotate normal --output HDMI-2 --off
else
    xrandr --output eDP-1 --primary --mode 1366x768 --pos 1366x0 --rotate normal --output HDMI-1 --off --output DP-1 --off
fi

# Composer
picom &
# Network
nm-applet &
# Keyboard Layout
teclado=`lsusb | grep 04d9:0024 | awk {'print $6'}`
if [ "$teclado" = "04d9:0024" ]; then
    setxkbmap us altgr-intl &
else
    setxkbmap -layout latam,latam &
fi
# Automount Devices
udiskie -t &
# Java Fonts
xsettingsd &
# Wallpaper
feh --bg-scale ~/Pictures/Wallpapers/archbg.png &
# Overlay Bar
xob-pulse-py | xob -s pulse &
xob-brightness-js | xob -s brightness &
blueman-applet &
