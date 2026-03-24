#!/usr/bin/env bash

state=$(dbus-send --session --print-reply=literal --dest=org.gnome.Pomodoro /org/gnome/Pomodoro org.freedesktop.DBus.Properties.Get string:org.gnome.Pomodoro string:State 2>/dev/null | awk '{print $2}') || state="stopped"

[[ -z "$state" || "$state" == "stopped" || "$state" == "idle" || "$state" == "null" ]] && state="stopped"

if [[ "$state" == "stopped" ]]; then
  printf '🍅 --\n'
  exit 0
fi

elapsed=$(dbus-send --session --print-reply=literal --dest=org.gnome.Pomodoro /org/gnome/Pomodoro org.freedesktop.DBus.Properties.Get string:org.gnome.Pomodoro string:Elapsed 2>/dev/null | awk '{print $3}') || exit 0
duration=$(dbus-send --session --print-reply=literal --dest=org.gnome.Pomodoro /org/gnome/Pomodoro org.freedesktop.DBus.Properties.Get string:org.gnome.Pomodoro string:StateDuration 2>/dev/null | awk '{print $3}') || exit 0

[[ -z "$elapsed" || -z "$duration" ]] && exit 0

elapsed_int=${elapsed%.*}
remaining=$((duration - elapsed_int))

[[ $remaining -le 0 ]] && exit 0

minutes=$((remaining / 60))
seconds=$((remaining % 60))

case "$state" in
  "pomodoro")
    icon="🍅"
    ;;
  "long-break"|"short-break")
    icon="☕"
    ;;
  *)
    icon="🍅"
    ;;
esac

printf '%s %02d:%02d\n' "$icon" "$minutes" "$seconds"
