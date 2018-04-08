#!/usr/bin/env bash

catch_kill() {
  echo "Caught SIGKILL signal!"
  sleep 1
  trap - SIGKILL
  kill -KILL "$pid"
}

catch_term() {
  echo "Caught SIGTERM signal!"
  sleep 1
  trap - SIGTERM
  kill -TERM "$pid"
}

catch_quit() {
  echo "Caught SIGKILL signal!"
  sleep 1
  trap - SIGQUIT
  kill -QUIT "$pid"
}

catch_ctrlc() {
  echo "Caught ctrl+c!"
  sleep 1
  trap - SIGINT
  kill -INT "$pid"
}

trap catch_term SIGTERM
trap catch_kill SIGKILL
trap catch_quit SIGQUIT
trap catch_ctrlc SIGINT

echo "Script is running!"

pid=$$

while true
do
    echo "waiting for signals."
    sleep 0.2
done
