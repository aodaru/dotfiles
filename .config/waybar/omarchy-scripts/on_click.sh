#!/usr/bin/env bash

state=$(dbus-send --session --print-reply=literal --dest=io.github.focustimerhq.FocusTimer /io/github/focustimerhq/FocusTimer org.freedesktop.DBus.Properties.Get string:"io.github.focustimerhq.FocusTimer.Timer" string:"State" 2>/dev/null | awk '{print $2}')

if [[ -z "$state" || "$state" == "null" || "$state" == "stopped" ]]; then
  focus-timer --start
else
  focus-timer --start-pause-resume
fi
