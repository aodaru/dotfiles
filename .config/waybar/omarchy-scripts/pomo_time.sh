#!/usr/bin/env bash

# Check if focus-timer process is running
if ! pgrep -x focus-timer > /dev/null 2>&1; then
  printf '🍅 --\n'
  exit 0
fi

state=$(dbus-send --session --print-reply=literal --dest=io.github.focustimerhq.FocusTimer /io/github/focustimerhq/FocusTimer org.freedesktop.DBus.Properties.Get string:"io.github.focustimerhq.FocusTimer.Timer" string:"State" 2>/dev/null | awk '{print $2}')

[[ -z "$state" || "$state" == "stopped" || "$state" == "null" ]] && state="stopped"

if [[ "$state" == "stopped" ]]; then
  printf '🍅 --\n'
  exit 0
fi

# Check if timer has finished (cycle completed)
is_finished=$(dbus-send --session --print-reply=literal --dest=io.github.focustimerhq.FocusTimer /io/github/focustimerhq/FocusTimer io.github.focustimerhq.FocusTimer.Timer.IsFinished 2>/dev/null | awk '{print $2}')

if [[ "$is_finished" == "true" ]]; then
  printf '🍅 --\n'
  exit 0
fi

remaining_micros=$(dbus-send --session --print-reply=literal --dest=io.github.focustimerhq.FocusTimer /io/github/focustimerhq/FocusTimer io.github.focustimerhq.FocusTimer.Timer.GetRemaining int64:-1 2>/dev/null | awk '{print $2}') || exit 0

[[ -z "$remaining_micros" || "$remaining_micros" -le 0 ]] && exit 0

remaining=$((remaining_micros / 1000000))

if [[ $remaining -le 0 ]]; then
  printf '🍅 00:00\n'
  exit 0
fi

minutes=$((remaining / 60))
seconds=$((remaining % 60))

case "$state" in
  "pomodoro")
    icon="🍅"
    ;;
  "long-break" | "short-break")
    icon="☕"
    ;;
  *)
    icon="🍅"
    ;;
esac

printf '%s %02d:%02d\n' "$icon" "$minutes" "$seconds"
