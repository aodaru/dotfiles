#!/usr/bin/env bash

state=$(dbus-send --session --print-reply=literal --dest=io.github.focustimerhq.FocusTimer /io/github/focustimerhq/FocusTimer org.freedesktop.DBus.Properties.Get string:"io.github.focustimerhq.FocusTimer.Timer" string:"State" 2>/dev/null | awk '{print $2}')

[[ -z "$state" || "$state" == "stopped" || "$state" == "null" ]] && state="stopped"

if [[ "$state" == "stopped" ]]; then
  printf '🍅 --\n'
  exit 0
fi

remaining_micros=$(dbus-send --session --print-reply=literal --dest=io.github.focustimerhq.FocusTimer /io/github/focustimerhq/FocusTimer io.github.focustimerhq.FocusTimer.Timer.GetRemaining int64:-1 2>/dev/null | awk '{print $2}') || exit 0

[[ -z "$remaining_micros" || "$remaining_micros" -le 0 ]] && exit 0

remaining=$((remaining_micros / 1000000))

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
