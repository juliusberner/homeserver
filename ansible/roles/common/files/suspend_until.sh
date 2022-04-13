#!/bin/bash
# Auto suspend and wake-up script
# see https://askubuntu.com/questions/61708/automatically-sleep-and-wake-up-at-specific-times
#
# Takes a 24hour time HH:MM as its argument
# Example:
# suspend_until 9:30
# suspend_until 18:45

# ------------------------------------------------------
# suspend option (see "man rtcwake")
MODE=off

# check whether specified time is today or tomorrow
DESIRED=$((`date +%s -d "$1"`))
NOW=$((`date +%s`))
if [ $DESIRED -lt $NOW ]; then
  DESIRED=$((`date +%s -d "$1"` + 24*60*60))
fi

# kill already running rtcwake
sudo killall rtcwake

# set wakeup time
sudo rtcwake -l -m $MODE -t $DESIRED &

# feedback
echo "Suspending..."

# give rtcwake some time to make its stuff
sleep 2

# then suspend (N.B. usually do not require this bit)
# sudo pm-suspend

# any commands you want to launch after wakeup can be placed here (note that sudo may have expired)

# wake up with monitor enabled (N.B. change "on" for "off" if the monitor should be be disabled on wake)
# xset dpms force on

echo "Waking up..."
