#!/usr/bin/env bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TASK_FILE="$SCRIPT_DIR/.active_task"

focus-timer --reset

if [[ -f "$TASK_FILE" ]]; then
  task_id=$(cat "$TASK_FILE")
  if [[ -n "$task_id" ]]; then
    task "$task_id" stop 2>/dev/null
  fi
  rm -f "$TASK_FILE"
fi
