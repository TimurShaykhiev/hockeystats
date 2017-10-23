#! /bin/bash

SCHEDULER_ROOT=/home/timur/sources/hockeystats

SCHEDULER_PATH=${SCHEDULER_ROOT}/scheduler.py
THIS_SCRIPT=${SCHEDULER_ROOT}/scheduler.sh
CRON_TASK_EVERY_DAY="0 12 \* \* \* ${THIS_SCRIPT}"
CRON_TASK_EVERY_HOUR="0 \* \* \* \* ${THIS_SCRIPT}"


source ${SCHEDULER_ROOT}/venv/bin/activate
python ${SCHEDULER_PATH}
if [ $? -eq 2 ] ; then
  # connection error, try again every hour
  crontab -l | sed -e "s|${CRON_TASK_EVERY_DAY}|${CRON_TASK_EVERY_HOUR}|g" | crontab -
else
  crontab -l | sed -e "s|${CRON_TASK_EVERY_HOUR}|${CRON_TASK_EVERY_DAY}|g" | crontab -
fi