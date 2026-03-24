#!/usr/bin/env bash

state=$(dbus-send --session --print-reply=literal --dest=org.gnome.Pomodoro /org/gnome/Pomodoro org.freedesktop.DBus.Properties.Get string:org.gnome.Pomodoro string:State 2>/dev/null | awk '{print $2}')

if [[ -z "$state" || "$state" == "null" || "$state" == "stopped" || "$state" == "idle" ]]; then
  gnome-pomodoro --start
else
  gnome-pomodoro --pause-resume
fi
