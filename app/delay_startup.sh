#!/bin/bash

#while true;do
#sleep 20
#  nc -z pg 5432
#  if [[ ${?} == 0 ]]
#  then
#    echo "OK" && break
#  fi  
#done

python manage.py runserver 0.0.0.0:8000
